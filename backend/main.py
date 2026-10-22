import random
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from models import GameAction, GameResponse, PlayerState, RollResult
from game_data import CLASSES_DATA

app = FastAPI(title="Neon Grid RPG Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

CURRENT_SCENARIOS = {}

@app.get("/api/classes")
async def get_classes():
    return CLASSES_DATA

@app.post("/api/start")
async def start_game(player_state: PlayerState):
    role = player_state.role
    class_info = CLASSES_DATA.get(role, CLASSES_DATA["Netrunner"])
    start_key = class_info.get("start_scenario", "net_start")
    
    CURRENT_SCENARIOS[player_state.name] = start_key
    scenario = class_info["scenarios"][start_key].copy()
    
    return {
        "system_log": f"OPERATIVE LOGGED IN: [CLASS: {role.upper()}]",
        "story": scenario
    }

@app.post("/api/action", response_model=GameResponse)
async def process_action(data: GameAction):
    try:
        role = data.player_state.role
        class_info = CLASSES_DATA.get(role, CLASSES_DATA["Netrunner"])
        scenarios = class_info["scenarios"]
        
        current_key = CURRENT_SCENARIOS.get(data.player_state.name, class_info["start_scenario"])
        current_scenario = scenarios.get(current_key, scenarios[class_info["start_scenario"]])
        
        action_map = current_scenario.get("action_map", {})
        action_target = action_map.get(data.action)

        roll_info = None
        next_key = None

        # Check if action requires a dice roll skill check
        if isinstance(action_target, dict):
            stat_name = action_target.get("stat", "COMBAT")
            dc = action_target.get("dc", 10)
            
            # Fetch player attribute modifier
            modifier = data.player_state.stats.get(stat_name, 0)
            d20_roll = random.randint(1, 20)
            total = d20_roll + modifier
            success = total >= dc

            roll_info = RollResult(
                stat_used=stat_name,
                d20_roll=d20_roll,
                modifier=modifier,
                total=total,
                dc=dc,
                success=success
            )

            next_key = action_target["success"] if success else action_target["fail"]
        elif isinstance(action_target, str):
            next_key = action_target
        else:
            next_key = list(action_map.values())[0] if action_map else current_key

        CURRENT_SCENARIOS[data.player_state.name] = next_key
        next_scenario = scenarios[next_key]

        return GameResponse(
            narrative=next_scenario["narrative"],
            hp_change=next_scenario.get("hp_change", 0),
            eddies_change=next_scenario.get("eddies_change", 0),
            new_items=next_scenario.get("new_items", []),
            lost_items=next_scenario.get("lost_items", []),
            suggested_actions=next_scenario.get("suggested_actions", []),
            new_location=next_scenario.get("new_location", data.player_state.location),
            is_game_over=next_scenario.get("is_game_over", False),
            roll=roll_info
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)