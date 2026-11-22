from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Literal

MapNodeId = Literal[
    "pier6",
    "westside",
    "ladadika",
    "venizelou",
    "aristotelous",
    "ano_poli",
    "rotunda",
    "white_tower",
    "eastside",
]


class StoryPin(BaseModel):
    node_id: MapNodeId
    title: str
    objective: str
    action_text: str
    status: str = "active"  # "active", "escalated", "resolved"


class PlayerState(BaseModel):
    name: str = "V-2077"
    role: str = "Netrunner"
    hp: int = 100
    max_hp: int = 100
    eddies: int = 0
    current_node_id: MapNodeId = "venizelou"
    story_pins: List[StoryPin] = []
    location: str = "Thessaloniki - Sector 09 Alleyway"
    stats: Dict[str, int] = {
        "HACKING": 0,
        "COMBAT": 0,
        "TECH": 0,
    }
    reputation: Dict[str, int] = {
        "corporates": 0,
        "underground": 0,
        "law_enforcement": 0,
    }


class GameAction(BaseModel):
    action: str
    player_state: PlayerState
    history: List[str] = []


class RollResult(BaseModel):
    stat_used: str
    d20_roll: int
    modifier: int
    rep_modifier: int = 0
    total: int
    dc: int
    effective_dc: int
    success: bool


class GameResponse(BaseModel):
    narrative: str
    hp_change: int = 0
    eddies_change: int = 0
    reputation_change: Dict[str, int] = {}
    current_node_id: MapNodeId = "venizelou"
    story_pins: List[StoryPin] = []
    suggested_actions: List[str] = []
    new_location: Optional[str] = None
    is_game_over: bool = False
    roll: Optional[RollResult] = None
    updated_reputation: Dict[str, int] = {}


class AIGameOutput(BaseModel):
    narrative: str
    hp_change: int = 0
    eddies_change: int = 0
    reputation_change: Dict[str, int] = {}
    current_node_id: MapNodeId = "venizelou"
    new_pin: Optional[StoryPin] = None
    resolved_node_id: Optional[MapNodeId] = None
    suggested_actions: List[str]
    new_location: Optional[str] = None
    is_game_over: bool = False