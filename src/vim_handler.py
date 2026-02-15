from typing import Tuple, Optional, Callable, List

class VimHandler:
    def __init__(self, move_callback: Callable, action_callback: Callable):
        self.move_callback = move_callback
        self.action_callback = action_callback
        self.buffer = ""
        self.mode = "NORMAL"

    def handle_key(self, key: str, map_row: List[str], player_x: int) -> str:
        """Processes a key press and returns the current command buffer."""
        if key == "escape":
            self.buffer = ""
            return ""

        self.buffer += key
        
        # Parse count and command
        count_str = ""
        cmd_idx = 0
        while cmd_idx < len(self.buffer) and self.buffer[cmd_idx].isdigit():
            count_str += self.buffer[cmd_idx]
            cmd_idx += 1
        
        count = int(count_str) if count_str else 1
        cmd = self.buffer[cmd_idx:]

        if not cmd:
            return self.buffer

        # Basic Movement
        if cmd == "h":
            self.move_callback(-1, 0, count)
        elif cmd == "j":
            self.move_callback(0, 1, count)
        elif cmd == "k":
            self.move_callback(0, -1, count)
        elif cmd == "l":
            self.move_callback(1, 0, count)
            
        # Word Navigation (Simulation for a game grid)
        elif cmd == "w":
            # Jump to next obstacle/entity or space (simulated)
            self.move_callback(3, 0, count)
        elif cmd == "b":
            self.move_callback(-3, 0, count)

        # Line Navigation
        elif cmd == "0":
            # Start of line (well, left-most in our engine for now)
            self.move_callback(-player_x + 1, 0, 1)
        elif cmd == "$":
            # We'd need map width here, but for now let's just use a large number if we don't have it
            self.move_callback(len(map_row) - player_x - 2, 0, 1)
        
        # Deletion
        elif cmd == "x":
            self.action_callback("delete")
        elif cmd == "dw" or cmd == "dd":
            self.action_callback("delete")

        # Clear buffer if command was executed or too long
        if cmd in ["h", "j", "k", "l", "w", "b", "0", "$", "x"] or len(self.buffer) > 4:
            self.buffer = ""
        elif cmd in ["dw", "dd"]:
            self.buffer = ""

        return self.buffer
