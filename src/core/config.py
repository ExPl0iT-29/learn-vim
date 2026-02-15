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
    """Manages game configuration and persistence."""
    def __init__(self):
        self.config = self._load_configuration()

    def _load_configuration(self):
        """Loads configuration from the .vimgamerc file."""
        if os.path.exists(CONFIG_FILE):
            try:
                with open(CONFIG_FILE, "r") as config_file:
                    return {**DEFAULT_CONFIG, **json.load(config_file)}
            except Exception as error:
                print(f"Failed to load configuration: {error}")
        return DEFAULT_CONFIG

    def save(self):
        """Saves the current configuration to disk."""
        try:
            with open(CONFIG_FILE, "w") as config_file:
                json.dump(self.config, config_file, indent=4)
        except Exception as error:
            print(f"Failed to save configuration: {error}")

    def get(self, key):
        """Retrieves a configuration value by key."""
        return self.config.get(key)
