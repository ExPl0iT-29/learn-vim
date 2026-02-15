import random
from dataclasses import dataclass, field
from typing import List, Tuple, Dict, Optional

@dataclass
class Entity:
    name: str
    symbol: str
    x: int
    y: int
    hp: int = 1
    max_hp: int = 1
    type: str = "enemy" # "player", "enemy", "rubble", "exit", "lock", "key"

@dataclass
class LevelConfig:
    num: int
    name: str
    instructions: str
    map_template: List[str]
    unlocked_commands: List[str]
    objective_type: str = "reach_exit" # "reach_exit", "clear_enemies", "clear_rubble"

class GameEngine:
    def __init__(self):
        self.levels: List[LevelConfig] = []
        self.current_level_idx = 0
        self.player = Entity("Player", "@", 1, 1, 20, 20, "player")
        self.enemies: List[Entity] = []
        self.interactables: List[Entity] = []
        self.map_data: List[List[str]] = []
        self.messages: List[str] = ["Welcome to the Vim Dungeon!", "Complete the objectives to progress."]
        self.level_complete = False
        
    def load_level(self, level: LevelConfig):
        self.current_level = level
        self.map_data = [list(row) for row in level.map_template]
        self.height = len(self.map_data)
        self.width = len(self.map_data[0])
        self.enemies = []
        self.interactables = []
        self.level_complete = False
        
        # Parse map and place entities
        for y, row in enumerate(self.map_data):
            for x, char in enumerate(row):
                if char == "@":
                    self.player.x, self.player.y = x, y
                    self.map_data[y][x] = "."
                elif char == "G":
                    self.enemies.append(Entity(f"Goblin", "G", x, y, 5, 5, "enemy"))
                    self.map_data[y][x] = "."
                elif char == ">":
                    self.interactables.append(Entity("Exit", ">", x, y, 1, 1, "exit"))
                    self.map_data[y][x] = "."
                elif char == "R":
                    self.interactables.append(Entity("Rubble", "R", x, y, 1, 1, "rubble"))
                    self.map_data[y][x] = "."

    def move_player(self, dx: int, dy: int, count: int = 1):
        for _ in range(count):
            new_x = self.player.x + dx
            new_y = self.player.y + dy
            
            if 0 <= new_x < self.width and 0 <= new_y < self.height:
                # Check interactables
                target = self.get_entity_at(new_x, new_y)
                if target:
                    if target.type == "exit":
                        self.complete_level()
                        break
                    elif target.type in ["enemy", "rubble"]:
                        self.add_message(f"There is a {target.name} in your way!")
                        break
                
                if self.map_data[new_y][new_x] == ".":
                    self.player.x = new_x
                    self.player.y = new_y
                else:
                    break
            else:
                break

    def get_entity_at(self, x: int, y: int) -> Optional[Entity]:
        for e in self.enemies + self.interactables:
            if e.x == x and e.y == y:
                return e
        return None

    def perform_action(self, action_type: str, direction: Optional[Tuple[int, int]] = None):
        # Handle 'x', 'dw', etc.
        if action_type == "delete":
            # Search adjacent for rubble or enemies
            px, py = self.player.x, self.player.y
            targets = [e for e in self.enemies + self.interactables if abs(e.x - px) <= 1 and abs(e.y - py) <= 1 and e != self.player]
            if targets:
                target = targets[0] # Just hit the first one for now
                self.attack(self.player, target)

    def attack(self, attacker: Entity, target: Entity):
        damage = random.randint(1, 3)
        target.hp -= damage
        self.add_message(f"{attacker.name} hits {target.name} for {damage} damage!")
        
        if target.hp <= 0:
            self.add_message(f"{target.name} cleared!")
            if target in self.enemies:
                self.enemies.remove(target)
            elif target in self.interactables:
                self.interactables.remove(target)

    def add_message(self, msg: str):
        self.messages.append(msg)
        if len(self.messages) > 10:
            self.messages.pop(0)

    def complete_level(self):
        self.add_message("LEVEL COMPLETE! Press any key to continue...")
        self.level_complete = True

    def get_render_data(self) -> List[List[str]]:
        render_map = [row[:] for row in self.map_data]
        for e in self.interactables + self.enemies:
            render_map[e.y][e.x] = e.symbol
        render_map[self.player.y][self.player.x] = self.player.symbol
        return render_map
