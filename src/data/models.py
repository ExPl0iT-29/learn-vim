from dataclasses import dataclass, field
from typing import List, Tuple, Dict, Optional, Set
from enum import Enum, auto

class GameMode(Enum):
    NORMAL = auto()
    INSERT = auto()
    VISUAL = auto()
    VISUAL_LINE = auto()
    COMMAND = auto()

class EntityType(Enum):
    PLAYER = auto()
    ENEMY = auto()
    RUBBLE = auto()
    EXIT = auto()
    KEY = auto()
    LOCK = auto()
    TERMINAL = auto()
    BOSS = auto() # New: Regex Boss
    DECOR = auto()

@dataclass(frozen=True)
class Point:
    x: int
    y: int

@dataclass
class Entity:
    name: str
    symbol: str
    pos: Point
    hp: int = 1
    max_hp: int = 1
    entity_type: EntityType = EntityType.ENEMY
    aura: bool = False # New: For Vim Aura
    metadata: Dict = field(default_factory=dict) # e.g. {"reg": "a"} for locks/keys

@dataclass
class LevelConfig:
    num: int
    name: str
    instructions: str
    map_template: List[str]
    unlocked_commands: Set[str] = field(default_factory=set)
    par_keystrokes: int = 0
    objective: str = "reach_exit" 
    narrative_intro: Optional[str] = None # New: Cyberpunk narrative
