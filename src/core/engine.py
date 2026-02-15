import random
import re
from typing import List, Tuple, Dict, Optional, Set
from src.data.models import Entity, EntityType, Point, LevelConfig, GameMode

class GameEngine:
    def __init__(self):
        self.mode = GameMode.NORMAL
        self.current_level_idx = 0
        self.player = Entity("Player", "@", Point(1, 1), 20, 20, EntityType.PLAYER)
        self.enemies: List[Entity] = []
        self.interactables: List[Entity] = []
        self.map_data: List[List[str]] = []
        self.messages: List[str] = ["VimRunner Online. System stable."]
        self.level_complete = False
        self.keystroke_count = 0
        self.registers: Dict[str, str] = {} # Key-value pairs for yank/put
        self.aura_active = False # Vim Aura
        self.last_move_efficient = False

    def load_level(self, config: LevelConfig):
        self.current_level = config
        self.map_data = [list(row) for row in config.map_template]
        self.height = len(self.map_data)
        self.width = len(self.map_data[0])
        self.enemies = []
        self.interactables = []
        self.level_complete = False
        self.keystroke_count = 0
        self.mode = GameMode.NORMAL
        self.aura_active = False
        
        for y, row in enumerate(self.map_data):
            for x, char in enumerate(row):
                p = Point(x, y)
                if char == "@":
                    self.player.pos = p
                    self.map_data[y][x] = "."
                elif char in "G B": # G for Goblin, B for Regex Boss
                    etype = EntityType.BOSS if char == "B" else EntityType.ENEMY
                    name = "Corrupted Binary" if char == "B" else "Minion"
                    self.enemies.append(Entity(name, char, p, 10 if char == "B" else 5, 10 if char == "B" else 5, etype))
                    self.map_data[y][x] = "."
                elif char == ">":
                    self.interactables.append(Entity("Exit", ">", p, 1, 1, EntityType.EXIT))
                    self.map_data[y][x] = "."
                elif char == "R":
                    self.interactables.append(Entity("Rubble", "R", p, 1, 1, EntityType.RUBBLE))
                    self.map_data[y][x] = "."
                elif char.islower() and char != 'b': # 'a', 'c', etc. are keys
                    self.interactables.append(Entity(f"Key {char}", char, p, 1, 1, EntityType.KEY, metadata={"reg": char}))
                    self.map_data[y][x] = "."
                elif char.isupper() and char not in "RGB B": # 'A', 'C', etc. are locks
                    self.interactables.append(Entity(f"Lock {char}", char, p, 1, 1, EntityType.LOCK, metadata={"reg": char.lower()}))
                    self.map_data[y][x] = "."

    def move_player(self, dx: int, dy: int, count: int = 1):
        # Efficiency check for Aura
        self.aura_active = (count > 1) or self.last_move_efficient
        
        for _ in range(count):
            new_x = max(0, min(self.width - 1, self.player.pos.x + dx))
            new_y = max(0, min(self.height - 1, self.player.pos.y + dy))
            new_pos = Point(new_x, new_y)
            
            target = self.get_entity_at(new_pos)
            if target:
                if target.entity_type == EntityType.EXIT:
                    self.complete_level()
                    break
                elif target.entity_type in [EntityType.ENEMY, EntityType.RUBBLE, EntityType.LOCK, EntityType.BOSS]:
                    self.add_message(f"Obstacle: {target.name}")
                    break
            
            if self.map_data[new_y][new_x] == ".":
                self.player.pos = new_pos
            else:
                break

    def perform_action(self, action: str, params: Dict = None):
        if action == "yank":
            self.handle_yank(params)
        elif action == "put":
            self.handle_put(params)
        elif action == "regex_attack":
            self.handle_regex_attack(params["command"])

    def handle_yank(self, params: Dict):
        reg = params.get("reg", '"')
        # Check if standing next to a Key
        px, py = self.player.pos.x, self.player.pos.y
        for e in self.interactables[:]:
            if e.entity_type == EntityType.KEY and abs(e.pos.x - px) <= 1 and abs(e.pos.y - py) <= 1:
                self.registers[reg] = e.metadata["reg"]
                self.add_message(f"Yanked {e.name} into register '{reg}'")
                self.interactables.remove(e)
                return

    def handle_put(self, params: Dict):
        reg = params.get("reg", '"')
        val = self.registers.get(reg)
        if not val: 
            self.add_message(f"Register '{reg}' is empty.")
            return

        # Check if next to a Lock
        px, py = self.player.pos.x, self.player.pos.y
        for e in self.interactables[:]:
            if e.entity_type == EntityType.LOCK and abs(e.pos.x - px) <= 1 and abs(e.pos.y - py) <= 1:
                if e.metadata["reg"] == val:
                    self.add_message(f"Lock {e.metadata['reg'].upper()} disengaged!")
                    self.interactables.remove(e)
                    return
                else:
                    self.add_message("Mismatch! Key doesn't fit this lock.")

    def handle_regex_attack(self, cmd: str):
        # Format: s/target/replace/g
        match = re.search(r's/(.+)/(.+)/g', cmd)
        if not match:
            self.add_message("Invalid Regex Command. Use s/target/replace/g")
            return

        target_pattern = match.group(1)
        # Damage nearest Boss if regex matches its corruption string (simulated)
        for enemy in self.enemies:
            if enemy.entity_type == EntityType.BOSS:
                self.add_message(f"REGEX ATTACK: Purging {target_pattern}...")
                enemy.hp -= 5
                if enemy.hp <= 0:
                    self.add_message(f"BOSS PURGED: {enemy.name}")
                    self.enemies.remove(enemy)
                return

    def get_entity_at(self, pos: Point) -> Optional[Entity]:
        for e in self.enemies + self.interactables:
            if e.pos == pos: return e
        return None

    def attack(self, attacker: Entity, target: Entity):
        damage = 5 if self.aura_active else 2
        target.hp -= damage
        self.add_message(f"HIT: {target.name} (-{damage} HP)")
        if target.hp <= 0:
            self.add_message(f"PURGED: {target.name}")
            if target in self.enemies: self.enemies.remove(target)
            elif target in self.interactables: self.interactables.remove(target)

    def add_message(self, msg: str):
        self.messages.append(msg)
        if len(self.messages) > 10: self.messages.pop(0)

    def complete_level(self):
        self.level_complete = True

    def get_render_data(self) -> List[List[str]]:
        render_map = [row[:] for row in self.map_data]
        for e in self.interactables + self.enemies:
            render_map[e.pos.y][e.pos.x] = e.symbol
        render_map[self.player.pos.y][self.player.pos.x] = self.player.symbol
        return render_map
