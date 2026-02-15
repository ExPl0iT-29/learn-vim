import json
import os
from typing import List, Dict, Optional

SCORE_FILE = "vimgame_scores.json"

class ScoringEngine:
    def __init__(self):
        self.keystrokes = 0
        self.best_scores: Dict[str, int] = self._load_scores()

    def _load_scores(self) -> Dict[str, int]:
        if os.path.exists(SCORE_FILE):
            try:
                with open(SCORE_FILE, "r") as f:
                    return json.load(f)
            except: return {}
        return {}

    def save_best(self, level_num: int, strokes: int):
        level_id = str(level_num)
        if level_id not in self.best_scores or strokes < self.best_scores[level_id]:
            self.best_scores[level_id] = strokes
            with open(SCORE_FILE, "w") as f:
                json.dump(self.best_scores, f)

    def get_rating(self, current_strokes: int, par: int) -> str:
        if current_strokes <= par: return "S - VIM MASTER"
        if current_strokes <= par * 1.5: return "A - EFFICIENT"
        if current_strokes <= par * 2.5: return "B - COMPETENT"
        return "C - NOVICE"
