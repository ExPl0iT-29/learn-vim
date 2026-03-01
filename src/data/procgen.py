import random
from typing import List, Tuple

class DungeonGenerator:
    """Procedurally generates levels for the Vim Masterpiece game."""
    
    def __init__(self, width: int = 20, height: int = 10):
        self.width = width
        self.height = height

    def generate(self, difficulty: int) -> List[str]:
        """Generates a random map based on difficulty level (11-30)."""
        # Initialize with empty space
        grid = [["." for _ in range(self.width)] for _ in range(self.height)]
        
        # Add perimeter walls
        for x in range(self.width):
            grid[0][x] = "#"
            grid[self.height - 1][x] = "#"
        for y in range(self.height):
            grid[y][0] = "#"
            grid[y][self.width - 1] = "#"
            
        # Place player at top left
        grid[1][1] = "@"
        
        # Place exit at bottom right
        exit_x, exit_y = self.width - 2, self.height - 2
        grid[exit_y][exit_x] = ">"

        # Determine features based on difficulty
        num_rubble = min(15, difficulty // 2)
        num_enemies = min(10, difficulty // 3)
        num_bosses = 1 if difficulty % 5 == 0 else 0 # Boss every 5 levels
        needs_key_lock = difficulty % 3 == 0 # Puzzle every 3 levels

        # Scatter rubble
        self._scatter(grid, "R", num_rubble)
        
        # Scatter enemies
        self._scatter(grid, "G", num_enemies)
        
        if num_bosses > 0:
            self._scatter(grid, "B", num_bosses)
            
        if needs_key_lock:
            # Pick a random register a-z
            reg_char = chr(random.randint(97, 122))
            key_char = reg_char
            lock_char = reg_char.upper()
            
            # Place Lock somewhere blocking the exit (simplified to near exit)
            if self._is_empty(grid, exit_x - 1, exit_y):
                grid[exit_y][exit_x - 1] = lock_char
            elif self._is_empty(grid, exit_x, exit_y - 1):
                grid[exit_y - 1][exit_x] = lock_char
                
            # Hide key somewhere random
            self._scatter(grid, key_char, 1)

        # Convert to list of strings
        return ["".join(row) for row in grid]

    def _is_empty(self, grid: List[List[str]], x: int, y: int) -> bool:
        return 0 < x < self.width - 1 and 0 < y < self.height - 1 and grid[y][x] == "."

    def _scatter(self, grid: List[List[str]], char: str, count: int):
        placed = 0
        while placed < count:
            x = random.randint(1, self.width - 2)
            y = random.randint(1, self.height - 2)
            # Don't place on player or exit start positions
            if (x, y) not in [(1,1), (self.width-2, self.height-2)] and grid[y][x] == ".":
                grid[y][x] = char
                placed += 1
