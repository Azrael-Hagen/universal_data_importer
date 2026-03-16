import os
import json
from pathlib import Path
from typing import Any, Dict


class ConfigManager:
    """
    Central configuration manager for the application.
    """

    DEFAULT_CONFIG = {
        "meltano": {
            "project_dir": ".",
        },
        "logging": {
            "level": "INFO"
        }
    }

    def __init__(self, config_file: str = "config.json"):

        self.root = Path.cwd()
        self.config_file = self.root / config_file

        self._config: Dict[str, Any] = {}

        self._load_defaults()
        self._load_file()
        self._load_env()

    # ------------------------------------------------
    # Loading configuration
    # ------------------------------------------------

    def _load_defaults(self):

        self._config.update(self.DEFAULT_CONFIG)

    def _load_file(self):

        if not self.config_file.exists():
            return

        with open(self.config_file, "r", encoding="utf-8") as f:
            data = json.load(f)

        self._merge_dicts(self._config, data)

    def _load_env(self):

        for key, value in os.environ.items():

            # Example: UDI_LOGGING_LEVEL
            if not key.startswith("UDI_"):
                continue

            config_key = key[4:].lower().replace("_", ".")

            self.set(config_key, value)

    # ------------------------------------------------
    # Access API
    # ------------------------------------------------

    def get(self, key: str, default=None):

        keys = key.split(".")
        value = self._config

        for k in keys:
            if not isinstance(value, dict):
                return default

            value = value.get(k)

            if value is None:
                return default

        return value

    def set(self, key: str, value: Any):

        keys = key.split(".")
        config = self._config

        for k in keys[:-1]:
            config = config.setdefault(k, {})

        config[keys[-1]] = value

    # ------------------------------------------------
    # Persistence
    # ------------------------------------------------

    def save(self):

        with open(self.config_file, "w", encoding="utf-8") as f:
            json.dump(self._config, f, indent=2)

    # ------------------------------------------------
    # Utilities
    # ------------------------------------------------

    def to_dict(self):

        return self._config

    def _merge_dicts(self, base: Dict, new: Dict):

        for key, value in new.items():

            if (
                key in base
                and isinstance(base[key], dict)
                and isinstance(value, dict)
            ):
                self._merge_dicts(base[key], value)

            else:
                base[key] = value

    def __repr__(self):

        return f"<ConfigManager {self._config}>"