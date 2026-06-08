import json
import os
from platformdirs import user_data_dir

_DATA_DIR = user_data_dir("vim-masterpiece", "tushar")

DEFAULT_CONFIG = {
    "theme": "tokyonight",
    "key_map": {"h": "h", "j": "j", "k": "k", "l": "l"},
    "sound_enabled": True,
}


class ConfigManager:
    def __init__(self):
        os.makedirs(_DATA_DIR, exist_ok=True)
        self._path = os.path.join(_DATA_DIR, "config.json")
        self.config = self._load()

    def _load(self) -> dict:
        if os.path.exists(self._path):
            try:
                with open(self._path) as f:
                    return {**DEFAULT_CONFIG, **json.load(f)}
            except Exception:
                pass
        return dict(DEFAULT_CONFIG)

    def save(self):
        try:
            with open(self._path, "w") as f:
                json.dump(self.config, f, indent=2)
        except Exception:
            pass

    def get(self, key):
        return self.config.get(key)
