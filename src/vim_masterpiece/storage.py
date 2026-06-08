import json
import os
from platformdirs import user_data_dir


class StorageManager:
    def __init__(self, filename: str = "scores.json"):
        self.data_dir = user_data_dir("vim-masterpiece", "tushar")
        self.file_path = os.path.join(self.data_dir, filename)
        os.makedirs(self.data_dir, exist_ok=True)

    def load(self) -> dict:
        if not os.path.exists(self.file_path):
            return {}
        try:
            with open(self.file_path) as f:
                return json.load(f)
        except Exception:
            return {}

    def save(self, data: dict):
        try:
            with open(self.file_path, "w") as f:
                json.dump(data, f, indent=2)
        except Exception:
            pass
