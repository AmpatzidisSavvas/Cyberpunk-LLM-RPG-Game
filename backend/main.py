import re
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

# Tracks current stage, location, origin theme, and shown options per player session
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
        "stage": 1,
        "scenario_key": start_key,
        "last_narrative": scenario["narrative"],
        "location": class_info["location"],
        "origin_theme": class_info.get("origin_theme", ""),
        "used_options": set(scenario.get("suggested_actions", [])),
    }

    return {
        "system_log": f"OPERATIVE LOGGED IN: [CLASS: {role.upper()}]",
        "story": scenario,
    }


@app.post("/api/action", response_model=GameResponse)
async def process_action(data: GameAction):
    try:
        player = data.player_state
        current_rep = player.reputation.copy()
        class_info = CLASSES_DATA.get(player.role, CLASSES_DATA["Netrunner"])

        session_data = CURRENT_SESSIONS.get(
            player.name,
            {
                "stage": 2,
                "scenario_key": None,
                "last_narrative": "Game start",
                "location": player.location,
                "origin_theme": class_info.get("origin_theme", ""),
                "used_options": set(),
            },
        )
        used_options = session_data.setdefault("used_options", set())
        used_options.add(data.action)

        # =====================================================================
        # STAGE 1: HANDCRAFTED CLASS ORIGIN RESOLUTION (DETERMINISTIC)
        # =====================================================================
        if session_data.get("stage") == 1:
            scenarios = class_info["scenarios"]
            current_scen = scenarios.get(session_data["scenario_key"], {})
            action_target = current_scen.get("action_map", {}).get(data.action)

            if action_target:
                roll_info = None
                if isinstance(action_target, dict):
                    stat_name = action_target.get("stat", "COMBAT")
                    base_dc = action_target.get("dc", 12)
                    target_faction = action_target.get("faction", "underground")

                    rep_modifier = current_rep.get(target_faction, 0) // 10
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
                    next_key = (
                        action_target["success"] if success else action_target["fail"]
                    )
                else:
                    next_key = action_target

                next_scen = scenarios[next_key]
                rep_changes = next_scen.get("reputation_change", {})
                for faction, val in rep_changes.items():
                    if faction in current_rep:
                        current_rep[faction] = max(
                            -100, min(100, current_rep[faction] + val)
                        )

                next_actions = next_scen.get("suggested_actions", [])
                used_options.update(next_actions)

                # Transition session to Stage 2 (Dynamic AI Sandbox)
                CURRENT_SESSIONS[player.name] = {
                    "stage": 2,
                    "scenario_key": next_key,
                    "last_narrative": next_scen["narrative"],
                    "location": next_scen.get(
                        "new_location", session_data["location"]
                    ),
                    "origin_theme": session_data["origin_theme"],
                    "used_options": used_options,
                }

                return GameResponse(
                    narrative=next_scen["narrative"],
                    hp_change=next_scen.get("hp_change", 0),
                    eddies_change=next_scen.get("eddies_change", 0),
                    reputation_change=rep_changes,
                    new_items=next_scen.get("new_items", []),
                    lost_items=next_scen.get("lost_items", []),
                    suggested_actions=next_actions,
                    new_location=next_scen.get(
                        "new_location", session_data["location"]
                    ),
                    is_game_over=next_scen.get("is_game_over", False),
                    roll=roll_info,
                    updated_reputation=current_rep,
                )

        # =====================================================================
        # STAGE 2+: GENERATIVE OLLAMA SANDBOX + FACTION & HEALTH SCALING
        # =====================================================================
        upper_action = data.action.upper()
        stat_name = "COMBAT"
        base_dc = 12

        if any(
            kw in upper_action
            for kw in ["HACK", "BYPASS", "TRACE", "DECK", "GRID", "DECRYPT", "SIPHON", "SPOOF"]
        ):
            stat_name = "HACKING"
            base_dc = 13
        elif any(
            kw in upper_action
            for kw in ["TECH", "BUILD", "RIG", "HOTWIRE", "TORCH", "REPAIR", "SALVAGE", "MODIFY"]
        ):
            stat_name = "TECH"
            base_dc = 13
        elif any(
            kw in upper_action
            for kw in ["SHOOT", "KNIFE", "SLIDE", "ASSAULT", "FIGHT", "KILL", "AMBUSH", "SUPPRESS"]
        ):
            stat_name = "COMBAT"
            base_dc = 12

        # Identify the primary faction involved based on action context
        target_faction = "underground"
        if any(
            kw in upper_action
            for kw in ["CORP", "ARASAKA", "MILITECH", "PLAZA", "EXEC", "VAULT", "BIDDER"]
        ):
            target_faction = "corporates"
        elif any(
            kw in upper_action
            for kw in ["NETWATCH", "POLICE", "NCPD", "TOWER", "LAW", "AGENT", "RELAY"]
        ):
            target_faction = "law_enforcement"
        elif any(
            kw in upper_action
            for kw in ["SCAV", "GANG", "STREET", "LADADIKA", "MARKET", "FIXER", "VARDAR"]
        ):
            target_faction = "underground"

        # Reputation modifier: Every 10 rep points shifts effective DC by 1
        faction_rep_score = current_rep.get(target_faction, 0)
        rep_modifier = faction_rep_score // 10
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

        system_prompt = f"""
        You are the master AI Game Master for a gritty, high-tech low-life cyberpunk RPG set in futuristic Thessaloniki, Greece. 
        The player has just executed an action involving the '{target_faction}' faction, and a Python-side dice check has resolved ({'SUCCESS' if success else 'FAILURE'}). 
        Write a vivid, immersive narrative response (2-4 sentences) describing the immediate outcome, heavily factoring in how the player's current standing with '{target_faction}' (Standing: {faction_rep_score}) influences the world's reaction.

        ATMOSPHERE & CLASS ARC GUIDELINES:
        - CLASS STORY ARC: Keep the plot anchored to the player's class origin theme: {session_data['origin_theme']}
        - Ground the narrative in futuristic Thessaloniki's distinct geography (e.g., Pier 6 docks, Ladadika alleys, Rotunda vaults, Aristotelous Plaza, Ano Poli heights, Westside ghettos, Eastside rednecks territories).
        - Maintain a dark cyberpunk tone blending corporate dystopia with Hellenic street grit.

        CRITICAL MECHANICAL & JSON RULES:
        1. FACTION REPUTATION: Reflect the player's standings in the narrative. If standing with '{target_faction}' is low (< -30), hostile hit squads or countermeasures actively punish them. If high (> 30), allies provide tactical support.
        2. STAT ADJUSTMENTS: Set "hp_change" (negative for damage, positive for recovery) and "eddies_change" proportionally. Update "reputation_change" dictionary with fitting point adjustments for the factions involved (e.g., {{ "{target_faction}": -10 }}) based on success or failure.
        3. INVENTORY & LOCATION: Update "new_items", "lost_items", or "new_location" if districts change.
        4. NEXT ACTIONS (NO REPEATS): Populate "suggested_actions" with exactly 3 BRAND NEW, distinct choices that move the plot forward. Never repeat previous actions.
        5. GAME OVER: If HP drops to 0 or below, set "is_game_over" to True.
        6. PLAIN TEXT ONLY: Never use HTML tags (such as <p>, </p>, or <br>) or Markdown formatting inside the "narrative" field.
        """

        recent_seen = list(used_options)[-8:]
        user_prompt = f"""
        Player State: {player.model_dump_json()}
        Current Location: {session_data['location']}
        Previous Narrative Context: {session_data['last_narrative']}
        Action Just Taken: "{data.action}"
        Target Faction Context: {target_faction} (Reputation: {faction_rep_score})
        Roll Outcome: {'SUCCESS' if success else 'FAILURE'} (Rolled {total} vs DC {effective_dc})

        BANNED / ALREADY USED ACTIONS (DO NOT REPEAT OR PARAPHRASE THESE):
        {recent_seen}

        Advance the story in 2-4 sentences and generate 3 fresh, situation-specific choices for the next turn.
        """

        response = ollama.chat(
            model="qwen2.5:3b",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            format=GameResponse.model_json_schema(),
            keep_alive="10m",
            options={
                "temperature": 0.78,
                "repeat_penalty": 1.15,
                "num_ctx": 1536,
                "num_predict": 260,
            },
        )

        ai_response = GameResponse.model_validate_json(response.message.content)

        # Strip any accidental HTML tags (like <p>, </p>, <br>) from the narrative
        ai_response.narrative = re.sub(r"<[^>]+>", "", ai_response.narrative).strip()

        # Context-Aware Reputation & Health Scaling Math Overlay
        raw_hp_change = ai_response.hp_change
        if raw_hp_change < 0:
            if faction_rep_score <= -30:
                raw_hp_change = int(raw_hp_change * 1.35)  # +35% damage if hostile
            elif faction_rep_score >= 30:
                raw_hp_change = int(raw_hp_change * 0.75)  # -25% damage if allied
        elif raw_hp_change > 0:
            if faction_rep_score >= 30:
                raw_hp_change = int(raw_hp_change * 1.25)  # +25% healing if allied

        ai_response.hp_change = raw_hp_change

        # Ensure the target faction gets a reputation shift if the AI omitted it
        if target_faction not in ai_response.reputation_change:
            ai_response.reputation_change[target_faction] = 10 if success else -15

        # Anti-Repetition & Empty-List Safeguard
        if not ai_response.is_game_over:
            seen_lower = {opt.strip().lower() for opt in used_options}
            seen_lower.update(h.strip().lower() for h in data.history)

            unique_suggestions = []
            for action in ai_response.suggested_actions:
                cleaned = action.strip()
                if cleaned and cleaned.lower() not in seen_lower:
                    unique_suggestions.append(cleaned)
                    seen_lower.add(cleaned.lower())

            if len(unique_suggestions) < 3:
                loc_short = (
                    ai_response.new_location or session_data["location"]
                ).split("-")[-1].strip()
                fallback_pool = [
                    f"Infiltrate deeper into {loc_short}",
                    f"Tap into a local terminal in {loc_short}",
                    "Contact an underground fixer for intel",
                    "Rig a makeshift trap and hold position",
                    "Slip into the shadows and flank the perimeter",
                    "Negotiate with nearby street operatives",
                ]
                random.shuffle(fallback_pool)
                for fb in fallback_pool:
                    if len(unique_suggestions) >= 3:
                        break
                    if fb.lower() not in seen_lower:
                        unique_suggestions.append(fb)
                        seen_lower.add(fb.lower())

            ai_response.suggested_actions = unique_suggestions[:3]
            used_options.update(ai_response.suggested_actions)

        ai_response.roll = roll_info

        # Update session memory
        CURRENT_SESSIONS[player.name] = {
            "stage": session_data.get("stage", 2) + 1,
            "scenario_key": None,
            "last_narrative": ai_response.narrative,
            "location": ai_response.new_location or session_data["location"],
            "origin_theme": session_data["origin_theme"],
            "used_options": used_options,
        }

        # Sync reputation state updates dictionary safely
        for faction, change in ai_response.reputation_change.items():
            if faction in current_rep:
                current_rep[faction] = max(
                    -100, min(100, current_rep[faction] + change)
                )
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
