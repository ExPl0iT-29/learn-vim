import random
import re
import copy
from typing import List, Tuple, Dict, Optional, Set
from src.data.models import Entity, EntityType, Point, LevelConfig, GameMode, Effect

class GameEngine:
    """
    The core logic for the Vim learning game.
    Manages the player, enemies, map state, and game rules.
    """
    def __init__(self):
        self.mode = GameMode.NORMAL
        self.current_level_index = 0
        self.player = Entity("Player", "@", Point(1, 1), 20, 20, EntityType.PLAYER)
        self.enemies: List[Entity] = []
        self.interactables: List[Entity] = []
        self.map_data: List[List[str]] = []
        self.messages: List[str] = ["VimRunner Online. Neural link established."]
        self.level_complete = False
        self.keystroke_count = 0
        self.registers: Dict[str, str] = {} # Key-value pairs for yank/put
        self.aura_active = False # Vim Aura
        self.last_move_efficient = False
        self.history_stack = []
        self.visual_anchor: Optional[Point] = None
        self.active_effects: List[Effect] = []

    def load_level(self, config: LevelConfig):
        """
        Loads a new level based on the provided configuration.
        Initializes map, player, enemies, and interactables.
        """
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
        self.history_stack = []
        self.visual_anchor = None
        self.active_effects = []
        
        for y, row in enumerate(self.map_data):
            for x, char in enumerate(row):
                point = Point(x, y)
                if char == "@":
                    self.player.position = point
                    self.map_data[y][x] = "."
                elif char in "G B": # G for Goblin, B for Regex Boss
                    entity_type = EntityType.BOSS if char == "B" else EntityType.ENEMY
                    name = "Corrupted Binary" if char == "B" else "Minion"
                    self.enemies.append(Entity(name, char, point, 10 if char == "B" else 5, 10 if char == "B" else 5, entity_type))
                    self.map_data[y][x] = "."
                elif char == ">":
                    self.interactables.append(Entity("Exit", ">", point, 1, 1, EntityType.EXIT))
                    self.map_data[y][x] = "."
                elif char == "R":
                    self.interactables.append(Entity("Rubble", "R", point, 1, 1, EntityType.RUBBLE))
                    self.map_data[y][x] = "."
                elif char.islower() and char != 'b': # 'a', 'c', etc. are keys
                    self.interactables.append(Entity(f"Key {char}", char, point, 1, 1, EntityType.KEY, metadata={"reg": char}))
                    self.map_data[y][x] = "."
                elif char.isupper() and char not in "RGB B": # 'A', 'C', etc. are locks
                    self.interactables.append(Entity(f"Lock {char}", char, point, 1, 1, EntityType.LOCK, metadata={"reg": char.lower()}))
                    self.map_data[y][x] = "."

    def move_player(self, dx: int, dy: int, count: int = 1):
        """
        Moves the player by dx, dy for a specified count.
        Handles collision detection and efficiency tracking.
        """
        # Efficiency check for Aura
        self.aura_active = (count > 1) or self.last_move_efficient
        
        for _ in range(count):
            new_x = max(0, min(self.width - 1, self.player.position.x + dx))
            new_y = max(0, min(self.height - 1, self.player.position.y + dy))
            new_position = Point(new_x, new_y)
            
            target = self.get_entity_at(new_position)
            if target:
                if target.entity_type == EntityType.EXIT:
                    self.complete_level()
                    break
                elif target.entity_type == EntityType.LOCK:
                    register_needed = target.metadata["reg"]
                    self.add_message(f"SECURITY ALERT: Lock {register_needed.upper()} active.")
                    self.add_message(f"Hint: Yank Key {register_needed} into register '{register_needed}' first.")
                    break
                elif target.entity_type == EntityType.BOSS:
                    self.add_message(f"WARNING: {target.name} detected.")
                    self.add_message("standard attacks are useless. Use [bold]:s/target/replace/g[/].")
                    break
                elif target.entity_type in [EntityType.ENEMY, EntityType.RUBBLE]:
                    self.add_message(f"Path blocked by: {target.name}")
                    break
            
            if self.map_data[new_y][new_x] == ".":
                self.player.position = new_position
            else:
                self.add_message("Collided with boundary.")
                break

    def perform_action(self, action: str, params: Dict = None):
        """Dispatches game actions like yank, put, and regex attacks."""
        if action == "yank":
            self.handle_yank(params)
        elif action == "put":
            self.handle_put(params)
        elif action == "regex_attack":
            self.handle_regex_attack(params["command"])
        elif action == "delete":
            self.handle_delete()

    def set_visual_anchor(self):
        """Sets the anchor point for visual mode selection."""
        self.visual_anchor = Point(self.player.position.x, self.player.position.y)

    def save_state(self):
        """Saves current state for undo functionality."""
        state = {
            "player_pos": Point(self.player.position.x, self.player.position.y),
            "player_hp": self.player.hp,
            "enemies": copy.deepcopy(self.enemies),
            "interactables": copy.deepcopy(self.interactables),
            "map_data": copy.deepcopy(self.map_data),
            "registers": copy.deepcopy(self.registers),
            "keystroke_count": self.keystroke_count,
            "messages": list(self.messages),
            "level_complete": self.level_complete
        }
        self.history_stack.append(state)
        if len(self.history_stack) > 20: 
            self.history_stack.pop(0)

    def undo(self):
        """Reverts the game state to the previous turn."""
        if not self.history_stack:
            self.add_message("Already at oldest change.")
            return

        state = self.history_stack.pop()
        self.player.position = state["player_pos"]
        self.player.hp = state["player_hp"]
        self.enemies = state["enemies"]
        self.interactables = state["interactables"]
        self.map_data = state["map_data"]
        self.registers = state["registers"]
        self.keystroke_count = state["keystroke_count"]
        self.messages = state["messages"]
        self.level_complete = state["level_complete"]
        self.add_message("Undid previous action.")

    def handle_delete(self):
        """Handles deletion, weaponizing Visual mode selection."""
        if self.mode == GameMode.VISUAL and self.visual_anchor:
            min_x = min(self.player.position.x, self.visual_anchor.x)
            max_x = max(self.player.position.x, self.visual_anchor.x)
            min_y = min(self.player.position.y, self.visual_anchor.y)
            max_y = max(self.player.position.y, self.visual_anchor.y)

            entities_to_remove = []
            for entity in self.enemies + self.interactables:
                if min_x <= entity.position.x <= max_x and min_y <= entity.position.y <= max_y:
                    if entity.entity_type not in [EntityType.EXIT, EntityType.PLAYER]:
                        entities_to_remove.append(entity)
            
            if not entities_to_remove:
                self.add_message("Nothing selected to delete.")
            else:
                for e in entities_to_remove:
                    if e in self.enemies: self.enemies.remove(e)
                    if e in self.interactables: self.interactables.remove(e)
                    self.spawn_explosion(e.position, e.entity_type)
                self.add_message(f"Visual strike destroyed {len(entities_to_remove)} targets!")
            
            self.mode = GameMode.NORMAL
            self.visual_anchor = None

    def handle_yank(self, params: Dict):
        """Handles yanking keys from the environment into registers."""
        register = params.get("reg", '"')
        # Check if standing next to a Key
        px, py = self.player.position.x, self.player.position.y
        for entity in self.interactables[:]:
            if entity.entity_type == EntityType.KEY and abs(entity.position.x - px) <= 1 and abs(entity.position.y - py) <= 1:
                self.registers[register] = entity.metadata["reg"]
                self.add_message(f"Success: {entity.name} extracted into register '{register}'")
                self.interactables.remove(entity)
                return
        self.add_message("Nothing here to yank.")

    def handle_put(self, params: Dict):
        """Handles using register contents on locks in the environment."""
        register = params.get("reg", '"')
        value = self.registers.get(register)
        if not value: 
            self.add_message(f"Error: Register '{register}' is currently empty.")
            return

        # Check if next to a Lock
        px, py = self.player.position.x, self.player.position.y
        for entity in self.interactables[:]:
            if entity.entity_type == EntityType.LOCK and abs(entity.position.x - px) <= 1 and abs(entity.position.y - py) <= 1:
                if entity.metadata["reg"] == value:
                    self.add_message(f"Access Granted: Lock {entity.metadata['reg'].upper()} disengaged!")
                    self.interactables.remove(entity)
                    return
                else:
                    self.add_message(f"Failure: Key '{register}' does not match Lock {entity.metadata['reg'].upper()}.")

    def handle_regex_attack(self, command: str):
        """Executes a regex search-and-replace attack on nearby bosses."""
        # Format: s/target/replace/g
        match = re.search(r's/(.+)/(.+)/g', command)
        if not match:
            self.add_message("Invalid syntax. Use s/target/replace/g to initiate regex attack.")
            return

        target_pattern = match.group(1)
        # Damage nearest Boss if regex matches its corruption string (simulated)
        for enemy in self.enemies:
            if enemy.entity_type == EntityType.BOSS:
                self.add_message(f"SYSTEM PURGE: Targeted {target_pattern} corruption...")
                enemy.hp -= 5
                if enemy.hp <= 0:
                    self.add_message(f"THREAT NEUTRALIZED: {enemy.name} purged.")
                    self.enemies.remove(enemy)
                return
        self.add_message("No eligible targets for regex attack in range.")

    def get_entity_at(self, position: Point) -> Optional[Entity]:
        """Returns the entity at a given position, if any."""
        for entity in self.enemies + self.interactables:
            if entity.position == position: return entity
        return None

    def attack(self, attacker: Entity, target: Entity):
        """Executes a melee attack between two entities."""
        damage = 5 if self.aura_active else 2
        target.hp -= damage
        self.add_message(f"LINK DAMAGE: {target.name} suffered {damage} damage.")
        if target.hp <= 0:
            self.add_message(f"ERASED: {target.name}")
            self.spawn_explosion(target.position, target.entity_type)
            if target in self.enemies: self.enemies.remove(target)
            elif target in self.interactables: self.interactables.remove(target)

    def spawn_explosion(self, position: Point, entity_type: EntityType):
        """Spawns particle effects at the entity's position."""
        color = "#f7768e" if entity_type in [EntityType.ENEMY, EntityType.BOSS] else "#c0caf5"
        for dx, dy in [(-1,0), (1,0), (0,-1), (0,1)]:
            nx, ny = position.x + dx, position.y + dy
            if 0 <= nx < self.width and 0 <= ny < self.height:
                if self.map_data[ny][nx] == ".":
                    self.active_effects.append(Effect(Point(nx, ny), random.choice(["*", "%", "x"]), color, 2))

    def add_message(self, message: str):
        """Adds a message to the game log, maintaining a maximum size."""
        self.messages.append(message)
        if len(self.messages) > 10: self.messages.pop(0)

    def complete_level(self):
        """Marks the current level as completed."""
        self.level_complete = True

    def get_render_data(self) -> List[List[str]]:
        """Prepares a character matrix of the map for rendering."""
        # Decrement effect lifespans
        self.active_effects = [e for e in self.active_effects if e.lifespan > 0]
        for e in self.active_effects: e.lifespan -= 1

        render_map = [row[:] for row in self.map_data]
        
        # Draw effects first (under entities)
        for effect in self.active_effects:
            render_map[effect.position.y][effect.position.x] = effect.char

        for entity in self.interactables + self.enemies:
            render_map[entity.position.y][entity.position.x] = entity.symbol
        render_map[self.player.position.y][self.player.position.x] = self.player.symbol
        return render_map
