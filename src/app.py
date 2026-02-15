from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Static
from textual.containers import Container, Vertical, Horizontal

from src.core.engine import GameEngine
from src.core.vim_logic import VimParser
from src.core.config import ConfigManager
from src.data.levels import LEVELS
from src.data.models import GameMode
from src.data.narrative import MILESTONE_1, MILESTONE_10, MILESTONE_30
from src.ui.widgets import VimMap, StatsDisplay, CommandBar, SoundBubble, NarrativeOverlay
from src.mechanics.engines import ScoringEngine

class VimMasterpiece(App):
    """The Ultimate Vim Learning Game: Fun & Polish Edition."""
    
    CSS = """
    Screen { background: #1a1b26; color: #c0caf5; }
    #main-container { layout: horizontal; width: 100%; height: 100%; }
    VimMap { 
        width: 70%; height: 100%; 
        border: heavy #414868; 
        padding: 2; 
        content-align: center middle; 
        background: #1f2335;
    }
    #side-pane { width: 30%; height: 100%; border-left: heavy #414868; }
    StatsDisplay { height: 40%; padding: 1; border-bottom: double #414868; }
    #log { height: 60%; padding: 1; color: #9ece6a; }
    #command-bar { 
        dock: bottom; height: 3; 
        background: #414868; color: #7aa2f7; 
        padding: 1; 
        text-style: bold;
    }
    #sound-fx {
        dock: right;
        width: 15;
        height: 1;
        background: transparent;
    }
    """

    def compose(self) -> ComposeResult:
        yield Header()
        with Container(id="main-container"):
            yield VimMap(id="map")
            with Vertical(id="side-pane"):
                yield StatsDisplay(id="stats")
                yield Static(id="log")
        yield CommandBar("Buffer: ", id="command-bar")
        yield SoundBubble(id="sound-fx")
        yield NarrativeOverlay(id="narrative")
        yield Footer()

    def on_mount(self) -> None:
        """Called when the application is mounted. Initializes game components."""
        self.engine = GameEngine()
        self.parser = VimParser(self.on_mode_change, self.on_action)
        self.scoring = ScoringEngine()
        self.config = ConfigManager()
        self.load_level()

    def load_level(self):
        """Loads the current level and shows narrative milestones."""
        level_index = self.engine.current_level_index
        if level_index < len(LEVELS):
            if level_index == 0: self.show_narrative(MILESTONE_1)
            elif level_index == 9: self.show_narrative(MILESTONE_10)
            elif level_index == 29: self.show_narrative(MILESTONE_30)

            self.engine.load_level(LEVELS[level_index])
            self.update_ui()
        else:
            self.show_narrative(MILESTONE_30)
            self.set_timer(5, self.exit)

    def show_narrative(self, content: str):
        overlay = self.query_one("#narrative")
        overlay.show(content)

    def on_mode_change(self, new_mode: GameMode):
        self.engine.mode = new_mode
        self.update_ui()

    def on_action(self, action: str, params: dict):
        """Processes actions emitted by the Vim parser."""
        self.engine.keystroke_count += 1
        
        if action == "move":
            motion = params["motion"]
            count = params.get("count", 1)
            
            # Translate Vim motions to engine vectors
            dx, dy = 0, 0
            if motion == "l": dx = 1
            elif motion == "h": dx = -1
            elif motion == "j": dy = 1
            elif motion == "k": dy = -1
            elif motion == "w": dx = 3
            elif motion == "b": dx = -3
            
            self.engine.move_player(dx, dy, count)
            
        elif action in ["delete_line", "delete_word", "delete_char"]:
            self.engine.perform_action("delete")
        elif action == "yank":
            self.engine.perform_action("yank", {"reg": params["reg"]})
        elif action == "put":
            self.engine.perform_action("put", {"reg": params["reg"]})
        elif action == "regex_attack":
            self.engine.perform_action("regex_attack", {"command": params["command"]})
        
        if self.engine.level_complete:
            self.scoring.save_best(self.engine.current_level.num, self.engine.keystroke_count)
            self.engine.current_level_index += 1
            self.load_level()
        
        self.update_ui()

    def on_key(self, event) -> None:
        overlay = self.query_one("#narrative")
        if overlay.styles.display == "block":
            overlay.hide()
            event.stop()
            return

        bubble = self.query_one("#sound-fx")
        if self.config.get("sound_enabled"):
            bubble.display("CLACK" if event.key.isalnum() else "TICK")

        buffer = self.parser.handle_key(event.key, self.engine.mode)
        self.query_one("#command-bar").update(f"Buffer: {buffer}")
        self.update_ui()
        event.stop()

    def update_ui(self):
        """Updates all UI components based on the current engine state."""
        self.query_one("#map").render_map(
            self.engine.get_render_data(), 
            self.engine.player.position,
            self.engine.aura_active
        )
        self.query_one("#log").update("\n".join(self.engine.messages))
        self.query_one("#stats").update_stats(
            self.engine.current_level.num,
            self.engine.player.hp,
            self.engine.keystroke_count,
            self.engine.current_level.par_keystrokes,
            self.engine.mode.name,
            self.engine.registers
        )

if __name__ == "__main__":
    VimMasterpiece().run()
