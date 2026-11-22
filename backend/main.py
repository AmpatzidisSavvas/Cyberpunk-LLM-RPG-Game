import re
import random
from typing import List, Optional
import ollama
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from models import (
    AIGameOutput,
    GameAction,
    GameResponse,
    MapNodeId,
    PlayerState,
    RollResult,
    StoryPin,
)
from game_data import CLASSES_DATA

app = FastAPI(title="Neon Grid RPG Backend - Storyline Places Edition")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

CURRENT_SESSIONS = {}

VALID_NODES = {
    "pier6",
    "westside",
    "ladadika",
    "venizelou",
    "aristotelous",
    "ano_poli",
    "rotunda",
    "white_tower",
    "eastside",
}


def _infer_node_from_text(text: str, fallback: MapNodeId = "venizelou") -> MapNodeId:
    lower = text.lower()
    if any(k in lower for k in ["pier 6", "aegean", "harbor", "port", "sub-cable"]):
        return "pier6"
    if any(k in lower for k in ["westside", "ghetto", "vardar"]):
        return "westside"
    if any(k in lower for k in ["ladadika"]):
        return "ladadika"
    if any(k in lower for k in ["ano poli", "heptapyrgion", "rampart", "siege"]):
        return "ano_poli"
    if any(k in lower for k in ["rotunda", "catacomb"]):
        return "rotunda"
    if any(k in lower for k in ["white tower", "waterfront", "tower"]):
        return "white_tower"
    if any(k in lower for k in ["eastside", "redneck", "industrial"]):
        return "eastside"
    if any(k in lower for k in ["aristotelous", "plaza", "checkpoint"]):
        return "aristotelous"
    if any(k in lower for k in ["venizelou", "egnatia", "metro", "roman"]):
        return "venizelou"
    return fallback


def _merge_story_pins(
    existing_pins: List[StoryPin],
    new_pin: Optional[StoryPin] = None,
    resolved_node_id: Optional[str] = None,
) -> List[StoryPin]:
    pins_by_node: dict[str, StoryPin] = {
        p.node_id: p.model_copy() for p in existing_pins
    }

    if resolved_node_id and resolved_node_id in pins_by_node:
        pins_by_node[resolved_node_id].status = "resolved"

    if new_pin and new_pin.node_id in VALID_NODES:
        pins_by_node[new_pin.node_id] = new_pin.model_copy()

    return list(pins_by_node.values())


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
    starting_reputation = class_info.get(
        "reputation",
        {"corporates": 0, "underground": 0, "law_enforcement": 0},
    ).copy()

    start_node: MapNodeId = class_info.get("current_node_id", "venizelou")
    initial_pins = [StoryPin(**p) for p in class_info.get("story_pins", [])]

    scenario = class_info["scenarios"][start_key].copy()
    scenario["current_node_id"] = scenario.get("current_node_id", start_node)
    scenario["story_pins"] = [p.model_dump() for p in initial_pins]

    CURRENT_SESSIONS[player_state.name] = {
        "stage": 1,
        "scenario_key": start_key,
        "last_narrative": scenario["narrative"],
        "location": class_info["location"],
        "current_node_id": start_node,
        "story_pins": initial_pins,
        "origin_theme": class_info.get("origin_theme", ""),
        "used_options": set(scenario.get("suggested_actions", [])),
    }

    return {
        "system_log": f"OPERATIVE LOGGED IN: [CLASS: {role.upper()}]",
        "reputation": starting_reputation,
        "current_node_id": start_node,
        "story_pins": [p.model_dump() for p in initial_pins],
        "story": scenario,
    }


@app.post("/api/action", response_model=GameResponse)
async def process_action(data: GameAction):
    try:
        player = data.player_state
        current_rep = player.reputation.copy()
        class_info = CLASSES_DATA.get(player.role, CLASSES_DATA["Netrunner"])

        default_pins = (
            player.story_pins
            if player.story_pins
            else [StoryPin(**p) for p in class_info.get("story_pins", [])]
        )
        default_node: MapNodeId = player.current_node_id or class_info.get(
            "current_node_id", "venizelou"
        )

        session_data = CURRENT_SESSIONS.get(
            player.name,
            {
                "stage": 2,
                "scenario_key": None,
                "last_narrative": "Game start",
                "location": player.location,
                "current_node_id": default_node,
                "story_pins": default_pins,
                "origin_theme": class_info.get("origin_theme", ""),
                "used_options": set(),
            },
        )
        current_node: MapNodeId = session_data.get("current_node_id", default_node)
        current_pins: List[StoryPin] = session_data.get("story_pins", default_pins)
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

                next_loc = next_scen.get("new_location", session_data["location"])
                next_node: MapNodeId = next_scen.get(
                    "current_node_id",
                    _infer_node_from_text(next_loc, fallback=current_node),
                )
                raw_new_pin = next_scen.get("new_pin")
                new_pin_obj = StoryPin(**raw_new_pin) if raw_new_pin else None
                merged_pins = _merge_story_pins(
                    current_pins,
                    new_pin=new_pin_obj,
                    resolved_node_id=next_scen.get("resolved_node_id"),
                )

                next_actions = next_scen.get("suggested_actions", [])
                used_options.update(next_actions)

                CURRENT_SESSIONS[player.name] = {
                    "stage": 2,
                    "scenario_key": next_key,
                    "last_narrative": next_scen["narrative"],
                    "location": next_loc,
                    "current_node_id": next_node,
                    "story_pins": merged_pins,
                    "origin_theme": session_data["origin_theme"],
                    "used_options": used_options,
                }

                return GameResponse(
                    narrative=next_scen["narrative"],
                    hp_change=next_scen.get("hp_change", 0),
                    eddies_change=next_scen.get("eddies_change", 0),
                    reputation_change=rep_changes,
                    current_node_id=next_node,
                    story_pins=merged_pins,
                    suggested_actions=next_actions,
                    new_location=next_loc,
                    is_game_over=next_scen.get("is_game_over", False),
                    roll=roll_info,
                    updated_reputation=current_rep,
                )

        # =====================================================================
        # STAGE 2+: GENERATIVE OLLAMA SANDBOX + STORYLINE PLACE TRACKING
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

        active_pins_text = [
            f"[{p.node_id} | {p.status}] {p.title}: {p.objective}"
            for p in current_pins
            if p.status != "resolved"
        ]

        system_prompt = f"""
        You are the master AI Game Master for a gritty, high-tech low-life cyberpunk RPG set in futuristic Thessaloniki, Greece. 
        The player has just executed an action involving the '{target_faction}' faction, and a Python-side dice check has resolved ({'SUCCESS' if success else 'FAILURE'}). 
        Write a vivid, immersive narrative response (2-4 sentences) describing the immediate outcome, heavily factoring in how the player's current standing with '{target_faction}' (Standing: {faction_rep_score}) influences the world's reaction.

        ATMOSPHERE & CLASS ARC GUIDELINES:
        - CLASS STORY ARC: Keep the plot anchored to the player's class origin theme: {session_data['origin_theme']}
        - ACTIVE STORYLINE PINS: {active_pins_text}
        - Ground the narrative in futuristic Thessaloniki's distinct geography:
          "pier6" (Pier 6 docks), "westside" (Westside ghettos), "ladadika" (Ladadika alleys), "venizelou" (Venizelou/Egnatia metro ruins), "aristotelous" (Aristotelous Plaza), "ano_poli" (Ano Poli ramparts), "rotunda" (Rotunda vaults), "white_tower" (White Tower waterfront), "eastside" (Eastside industrial sprawl).
        - Maintain a dark cyberpunk tone blending corporate dystopia with Hellenic street grit.

        CRITICAL MECHANICAL & JSON RULES:
        1. FACTION REPUTATION: Reflect the player's standings in the narrative. If standing with '{target_faction}' is low (< -30), hostile hit squads or countermeasures actively punish them. If high (> 30), allies provide tactical support.
        2. STAT ADJUSTMENTS: Set "hp_change" (negative for damage, positive for recovery) and "eddies_change" proportionally. Update "reputation_change" dictionary with fitting point adjustments for the factions involved (e.g., {{ "{target_faction}": -10 }}) based on success or failure.
        3. STORYLINE PLACES & PINS: Set "current_node_id" to the exact sector ID where the player is now located (one of: "pier6", "westside", "ladadika", "venizelou", "aristotelous", "ano_poli", "rotunda", "white_tower", "eastside") and update "new_location" to match. Optionally set "new_pin" (with node_id, title, objective, action_text, status="active") if a new storyline beat opens in a sector, or "resolved_node_id" if a sector lead is completed.
        4. NEXT ACTIONS (NO REPEATS): Populate "suggested_actions" with exactly 3 BRAND NEW, distinct choices that move the plot forward. Never repeat previous actions.
        5. GAME OVER: If HP drops to 0 or below, set "is_game_over" to True.
        6. PLAIN TEXT ONLY: Never use HTML tags (such as <p>, </p>, or <br>) or Markdown formatting inside the "narrative" field.
        """

        recent_seen = list(used_options)[-8:]
        user_prompt = f"""
        Player State: {player.model_dump_json()}
        Current Storyline Place: {current_node} ({session_data['location']})
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
            format=AIGameOutput.model_json_schema(),
            keep_alive="10m",
            options={
                "temperature": 0.78,
                "repeat_penalty": 1.15,
                "num_ctx": 1536,
                "num_predict": 280,
            },
        )

        ai_output = AIGameOutput.model_validate_json(response.message.content)
        narrative = re.sub(r"<[^>]+>", "", ai_output.narrative).strip()

        raw_hp_change = ai_output.hp_change
        if raw_hp_change < 0:
            if faction_rep_score <= -30:
                raw_hp_change = int(raw_hp_change * 1.35)
            elif faction_rep_score >= 30:
                raw_hp_change = int(raw_hp_change * 0.75)
        elif raw_hp_change > 0:
            if faction_rep_score >= 30:
                raw_hp_change = int(raw_hp_change * 1.25)

        rep_changes = dict(ai_output.reputation_change)
        if target_faction not in rep_changes:
            rep_changes[target_faction] = 10 if success else -15

        if ai_output.new_location:
            inferred_from_loc = _infer_node_from_text(
                ai_output.new_location, fallback=current_node
            )
            next_node: MapNodeId = (
                inferred_from_loc
                if inferred_from_loc != current_node
                else (
                    ai_output.current_node_id
                    if ai_output.current_node_id in VALID_NODES
                    else inferred_from_loc
                )
            )
        else:
            next_node = (
                ai_output.current_node_id
                if ai_output.current_node_id in VALID_NODES
                else _infer_node_from_text(
                    f"{data.action} {narrative}", fallback=current_node
                )
            )

        merged_pins = _merge_story_pins(
            current_pins,
            new_pin=ai_output.new_pin,
            resolved_node_id=ai_output.resolved_node_id,
        )

        suggested_actions = list(ai_output.suggested_actions)
        if not ai_output.is_game_over:
            seen_lower = {opt.strip().lower() for opt in used_options}
            seen_lower.update(h.strip().lower() for h in data.history)

            unique_suggestions = []
            for action in suggested_actions:
                cleaned = action.strip()
                if cleaned and cleaned.lower() not in seen_lower:
                    unique_suggestions.append(cleaned)
                    seen_lower.add(cleaned.lower())

            if len(unique_suggestions) < 3:
                loc_short = (
                    ai_output.new_location or session_data["location"]
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

            suggested_actions = unique_suggestions[:3]
            used_options.update(suggested_actions)

        next_location = ai_output.new_location or session_data["location"]

        CURRENT_SESSIONS[player.name] = {
            "stage": session_data.get("stage", 2) + 1,
            "scenario_key": None,
            "last_narrative": narrative,
            "location": next_location,
            "current_node_id": next_node,
            "story_pins": merged_pins,
            "origin_theme": session_data["origin_theme"],
            "used_options": used_options,
        }

        for faction, change in rep_changes.items():
            if faction in current_rep:
                current_rep[faction] = max(
                    -100, min(100, current_rep[faction] + change)
                )

        return GameResponse(
            narrative=narrative,
            hp_change=raw_hp_change,
            eddies_change=ai_output.eddies_change,
            reputation_change=rep_changes,
            current_node_id=next_node,
            story_pins=merged_pins,
            suggested_actions=suggested_actions,
            new_location=next_location,
            is_game_over=ai_output.is_game_over,
            roll=roll_info,
            updated_reputation=current_rep,
        )

    except Exception as e:
        import traceback

        traceback.print_exc()
        raise HTTPException(
            status_code=500, detail=f"Ollama Game Master Error: {str(e)}"
        )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)