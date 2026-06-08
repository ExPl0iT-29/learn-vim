from vim_masterpiece.storage import StorageManager


class ScoringEngine:
    def __init__(self):
        self.storage = StorageManager("scores.json")
        self.best_scores: dict = self.storage.load()

    def save_best(self, level_num: int, strokes: int):
        key = str(level_num)
        if key not in self.best_scores or strokes < self.best_scores[key]:
            self.best_scores[key] = strokes
            self.storage.save(self.best_scores)

    def get_rating(self, strokes: int, par: int) -> str:
        if strokes <= par:
            return "S - VIM MASTER"
        if strokes <= par * 1.5:
            return "A - EFFICIENT"
        if strokes <= par * 2.5:
            return "B - COMPETENT"
        return "C - NOVICE"
