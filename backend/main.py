import random
import ollama
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from models import GameAction, GameResponse, PlayerState, RollResult
from game_data import CLASSES_DATA

app = FastAPI(title="Neon Grid RPG Backend - Ollama Dynamic Expansion")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Tracks current location/context descriptions per player session
CURRENT_SESSIONS = {}

@app.on_event("startup")
async def warmup_ollama():
    """Preloads the Qwen model into VRAM on server start to avoid cold-start delays."""
    try:
        ollama.generate(model="qwen2.5:3b", prompt="", keep_alive="10m")
        print("🤖 AI Game Master (qwen2.5:3b) loaded into memory successfully.")
    except Exception as e:
        print(f"⚠️ Ollama warmup skipped (is the app running?): {e}")

@app.get("/api/classes")
async def get_classes():
    return CLASSES_DATA

@app.post("/api/start")
async def start_game(player_state: PlayerState):
    role = player_state.role
    class_info = CLASSES_DATA.get(role, CLASSES_DATA["Netrunner"])
    start_key = class_info.get("start_scenario", "net_start")
    
    # Grab the hardcoded opening scenario to ensure instant, zero-lag game start
    scenario = class_info["scenarios"][start_key].copy()
    CURRENT_SESSIONS[player_state.name] = {
        "last_narrative": scenario["narrative"],
        "location": class_info["location"]
    }
    
    return {
        "system_log": f"OPERATIVE LOGGED IN: [CLASS: {role.upper()}]",
        "story": scenario
    }

@app.post("/api/action", response_model=GameResponse)
async def process_action(data: GameAction):
    try:
        player = data.player_state
        current_rep = player.reputation.copy()

        # 1. Determine stat check type and resolve D20 math securely in Python
        upper_action = data.action.upper()
        stat_name = "COMBAT"
        base_dc = 12

        if any(kw in upper_action for kw in ["HACK", "BYPASS", "TRACE", "DECK", "GRID"]):
            stat_name = "HACKING"
            base_dc = 13
        elif any(kw in upper_action for kw in ["TECH", "BUILD", "RIG", "HOTWIRE", "TORCH"]):
            stat_name = "TECH"
            base_dc = 13
        elif any(kw in upper_action for kw in ["SHOOT", "KNIFE", "SLIDE", "ASSAULT", "FIGHT", "KILL"]):
            stat_name = "COMBAT"
            base_dc = 12

        # Reputation modifier: Every 10 rep points shifts effective DC by 1
        rep_modifier = current_rep.get("underground", 0) // 10
        effective_dc = max(5, base_dc - rep_modifier)

        modifier = player.stats.get(stat_name, 0)
        d20_roll = random.randint(1, 20)
        total = d20_roll + modifier
        success = total >= effective_dc

        roll_info = RollResult(
            stat_used=stat_name,
            d20_roll=d20_roll,
            modifier=modifier,
            rep_modifier=rep_modifier,
            total=total,
            dc=base_dc,
            effective_dc=effective_dc,
            success=success,
        )

        # 2. Prepare context for Ollama AI Game Master with strict schema guidelines
        session_data = CURRENT_SESSIONS.get(
            player.name,
            {"last_narrative": "Game start", "location": player.location},
        )

        system_prompt = """
        You are the AI Game Master for a gritty cyberpunk RPG set in futuristic Thessaloniki, Greece.
        The player just performed an action and rolled a dice check. 
        Your job is to write a vivid, immersive narrative response (2-4 sentences) describing the immediate outcome.
        
        CRITICAL NARRATIVE & STAT RULES:
        1. Reflect the player's faction standings in the narrative (e.g., if they have low reputation with corporates or the underground, mention how hostile elements are actively hunting them down).
        2. Set "hp_change" based on how dangerous the situation is (negative for damage, positive for recovery).
        3. You MUST populate "suggested_actions" with a list of 3 distinct, actionable choices for the player's next turn (unless "is_game_over" is true).
        4. If HP drops to 0 or below, set "is_game_over" to True.
        """

        user_prompt = f"""
        Player State: {player.model_dump_json()}
        Previous Narrative Context: {session_data['last_narrative']}
        Action Taken: "{data.action}"
        Roll Outcome: {'SUCCESS' if success else 'FAILURE'} (Rolled {total} vs DC {effective_dc})
        Recent History: {data.history[-4:]}
        """

        # 3. Call local Ollama model enforcing Pydantic GameResponse Schema
        response = ollama.chat(
            model="qwen2.5:3b",  # High-speed, lightweight model
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            format=GameResponse.model_json_schema(),
            keep_alive="10m",
            options={
                "temperature": 0.7,
                "num_ctx": 1024,      # Reduces memory overhead for speed
                "num_predict": 250,   # Caps token generation for fast response
            },
        )

        # Parse AI text back into validated Pydantic model
        ai_response = GameResponse.model_validate_json(response.message.content)

        # 4. Reputation-Modified Health Logic (Python Math Overlay)
        raw_hp_change = ai_response.hp_change
        if current_rep:
            worst_rep = min(current_rep.values())
            best_rep = max(current_rep.values())

            if raw_hp_change < 0:
                if worst_rep <= -30:
                    raw_hp_change = int(raw_hp_change * 1.3)  # +30% damage if hostile
                elif best_rep >= 30:
                    raw_hp_change = int(raw_hp_change * 0.8)  # -20% damage if allied
            elif raw_hp_change > 0:
                if best_rep >= 30:
                    raw_hp_change = int(raw_hp_change * 1.2)  # +20% healing if allied

        ai_response.hp_change = raw_hp_change

        # 5. Guarantee Next Options: Fallback if Ollama returns an empty list
        if not ai_response.is_game_over and (
            not ai_response.suggested_actions
            or len(ai_response.suggested_actions) == 0
        ):
            ai_response.suggested_actions = [
                "Press forward deeper into the sector",
                "Scan the surrounding environment for digital traces",
                "Retreat to a safe zone and reassess",
            ]

        # Attach our calculated secure roll result and ensure consistency
        ai_response.roll = roll_info

        # Update session memory
        CURRENT_SESSIONS[player.name] = {
            "last_narrative": ai_response.narrative,
            "location": ai_response.new_location or player.location,
        }

        # Sync reputation state updates dictionary
        for faction, change in ai_response.reputation_change.items():
            if faction in current_rep:
                current_rep[faction] = max(-100, min(100, current_rep[faction] + change))
        ai_response.updated_reputation = current_rep

        return ai_response

    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=500, detail=f"Ollama Game Master Error: {str(e)}"
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)