from typing import Tuple, Optional, List, Dict, Callable
from src.data.models import GameMode

class VimParser:
    def __init__(self, mode_change_callback: Callable, action_callback: Callable):
        self.mode_change_callback = mode_change_callback
        self.action_callback = action_callback
        self.reset()

    def handle_key(self, key: str, mode: GameMode) -> str:
        if key == "escape":
            self.reset()
            self.mode_change_callback(GameMode.NORMAL)
            return ""

        if mode == GameMode.COMMAND:
            if key == "enter":
                self.action_callback("regex_attack", {"command": self.buffer})
                self.reset()
                self.mode_change_callback(GameMode.NORMAL)
                return ""
            elif key == "backspace":
                self.buffer = self.buffer[:-1]
            else:
                self.buffer += key
            return ":" + self.buffer

        # Register support
        if key == '"' and not self.active_register:
            self.waiting_for_reg = True
            return '"'
        
        if self.waiting_for_reg:
            self.active_register = key
            self.waiting_for_reg = False
            return f'"{key}'

        if self.pending_search:
            self.action_callback("search_jump", {"type": self.pending_search, "char": key})
            self.reset()
            return ""

        if key.isdigit() and not (key == "0" and not self.count_str):
            self.count_str += key
            return self.count_str

        count = int(self.count_str) if self.count_str else 1
        
        # Action Operators
        if key == "y":
            self.action_callback("yank", {"reg": self.active_register or '"', "count": count})
            self.reset()
        elif key == "p":
            self.action_callback("put", {"reg": self.active_register or '"', "count": count})
            self.reset()
        elif key == "d":
            if self.operator == "d":
                self.action_callback("delete_line", count)
                self.reset()
            else:
                self.operator = "d"
        elif key == "w":
            if self.operator == "d":
                self.action_callback("delete_word", count)
                self.reset()
            else:
                self.action_callback("move", {"motion": "w", "count": count})
                self.reset()

        # Motions
        elif key in ["h", "j", "k", "l", "0", "$"]:
            self.action_callback("move", {"motion": key, "count": count})
            self.reset()
        
        # Modes
        elif key == ":":
            self.mode_change_callback(GameMode.COMMAND)
            self.reset()
        elif key == "v":
            self.mode_change_callback(GameMode.VISUAL)
            self.reset()
        
        return self.format_buffer()

    def reset(self):
        self.buffer = ""
        self.count_str = ""
        self.operator = None
        self.pending_search = None
        self.active_register = None
        self.waiting_for_reg = False

    def format_buffer(self) -> str:
        res = ""
        if self.active_register: res += f'"{self.active_register}'
        res += self.count_str
        if self.operator: res += self.operator
        return res
