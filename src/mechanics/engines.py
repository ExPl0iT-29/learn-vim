import json
import os
from typing import List, Dict, Optional

SCORE_FILE = "vimgame_scores.json"

class ScoringEngine:
    """Manages player performance scores and ratings."""
    def __init__(self):
        self.keystrokes = 0
        self.best_scores: Dict[str, int] = self.load_existing_scores()

    def load_existing_scores(self) -> Dict[str, int]:
        """Loads historical best scores from the local file."""
        if os.path.exists(SCORE_FILE):
            try:
                with open(SCORE_FILE, "r") as score_file:
                    return json.load(score_file)
            except Exception as error:
                print(f"Failed to load scores: {error}")
                return {}
        return {}

    def save_best(self, level_num: int, strokes: int):
        """Updates the best score for a level if the current performance is better."""
        level_id = str(level_num)
        if level_id not in self.best_scores or strokes < self.best_scores[level_id]:
            self.best_scores[level_id] = strokes
            try:
                with open(SCORE_FILE, "w") as score_file:
                    json.dump(self.best_scores, score_file)
            except Exception as error:
                print(f"Failed to save best score: {error}")

    def get_rating(self, current_strokes: int, par_keystrokes: int) -> str:
        """Returns a human-readable rating based on performance relative to par."""
        if current_strokes <= par_keystrokes: return "S - VIM MASTER"
        if current_strokes <= par_keystrokes * 1.5: return "A - EFFICIENT"
        if current_strokes <= par_keystrokes * 2.5: return "B - COMPETENT"
        return "C - NOVICE"
