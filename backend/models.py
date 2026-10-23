from pydantic import BaseModel
from typing import List, Optional, Dict

class PlayerState(BaseModel):
    name: str = "V-2077"
    role: str = "Netrunner"
    hp: int = 100
    max_hp: int = 100
    eddies: int = 0
    inventory: List[str] = []
    location: str = "Thessaloniki - Sector 09 Alleyway"
    stats: Dict[str, int] = {
        "HACKING": 0,
        "COMBAT": 0,
        "TECH": 0
    }
    # Faction standings: ranges from -100 (Hostile) to +100 (Allied)
    reputation: Dict[str, int] = {
        "corporates": 0,
        "underground": 0,
        "law_enforcement": 0
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
    new_items: List[str] = []
    lost_items: List[str] = []
    suggested_actions: List[str] = []
    new_location: Optional[str] = None
    is_game_over: bool = False
    roll: Optional[RollResult] = None
    updated_reputation: Dict[str, int] = {}