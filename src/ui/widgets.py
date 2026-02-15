from textual.widgets import Static, Label, Header, Footer
from textual.containers import Container, Vertical, Horizontal
from textual.app import ComposeResult
from typing import List, Optional
from src.data.models import Point

class VimMap(Static):
    """Luxury map renderer with character-specific styling and Aura support."""
    def render_map(self, map_data: List[List[str]], player_position: Point, aura_active: bool):
        """Renders the game map with colors and player positioning."""
        rows = []
        for row_index, row in enumerate(map_data):
            row_str = ""
            for col_index, char in enumerate(row):
                is_player = (col_index == player_position.x and row_index == player_position.y)
                
                if is_player:
                    style = "bold #7aa2f7 on #2ac3de" if aura_active else "bold #7aa2f7"
                    row_str += f"[{style}]@[/]"
                elif char == "G": row_str += "[bold #f7768e]G[/]"
                elif char == "B": row_str += "[bold italic #f7768e on #1f2335]B[/]" # Boss
                elif char == ">": row_str += "[bold #9ece6a]>[/]"
                elif char == "R": row_str += "[#565f89]R[/]"
                elif char.islower(): row_str += f"[bold #e0af68]{char}[/]" # Key
                elif char.isupper(): row_str += f"[bold #bb9af7]{char}[/]" # Lock
                else: row_str += "[#1a1b26]. [/]"
            rows.append(row_str)
        self.update("\n".join(rows))

class SoundBubble(Static):
    """Temporary ASCII 'sound' effect for keypresses."""
    def display(self, text: str):
        self.update(f"[bold #414868]<{text}>[/]")
        self.set_timer(0.3, self.clear)

    def clear(self):
        self.update("")

class NarrativeOverlay(Static):
    """Full-screen ASCII narrative cutscene."""
    DEFAULT_CSS = """
    NarrativeOverlay {
        width: 100%; height: 100%;
        background: #1a1b26;
        content-align: center middle;
        padding: 4;
        layer: top;
        display: none;
    }
    """
    def show(self, content: str):
        self.update(content)
        self.styles.display = "block"

    def hide(self):
        self.styles.display = "none"

class StatsDisplay(Static):
    """Displays player statistics and register contents."""
    def update_stats(self, level_num: int, hit_points: int, strokes: int, par_keystrokes: int, game_mode: str, registers: Dict[str, str]):
        """Updates the visual statistics display."""
        content = f"[bold #7aa2f7]LEVEL {level_num}[/]\n"
        content += f"[#c0caf5]HP:[/] [bold #f7768e]{hit_points}[/]\n"
        content += f"[#c0caf5]MODE:[/] [bold #9ece6a]{game_mode}[/]\n\n"
        content += f"[bold #bb9af7]REGISTERS[/]\n"
        for key, value in registers.items():
            content += f"[#565f89]\"{key}:[/] {value}\n"
        content += f"\n[bold #bb9af7]VIM GOLF[/]\n"
        content += f"[#c0caf5]STROKES:[/] {strokes}\n"
        content += f"[#c0caf5]PAR:[/] {par_keystrokes}"
        self.update(content)

class CommandBar(Label):
    """A sleek command bar that mimics the Vim command line."""
    pass
