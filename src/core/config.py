import json
import os

CONFIG_FILE = ".vimgamerc"

DEFAULT_CONFIG = {
    "theme": "tokyonight",
    "key_map": {
        "h": "h", "j": "j", "k": "k", "l": "l"
    },
    "sound_enabled": True
}

class ConfigManager:
    def __init__(self):
        self.config = self._load()

    def _load(self):
        if os.path.exists(CONFIG_FILE):
            try:
                with open(CONFIG_FILE, "r") as f:
                    return {**DEFAULT_CONFIG, **json.load(f)}
            except: pass
        return DEFAULT_CONFIG

    def save(self):
        with open(CONFIG_FILE, "w") as f:
            json.dump(self.config, f, indent=4)

    def get(self, key):
        return self.config.get(key)
