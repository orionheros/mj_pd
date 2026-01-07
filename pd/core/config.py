#!/usr/bin/env python
# License: GPL v3 Copyright: 2026, Mateusz Jamróz
# pd/core/config.py

from configparser import ConfigParser
from pathlib import Path

DEFAULT_CONFIG = {
    "launcher": {
        "show_on_startup": "true",
        "saved_data_package": "",
    },
    "general": {
        "language": "en",
        "theme": "system",
        "check_updates": "true",
    },
    "ui": {
        "font_size": "12",
        "show_tips": "true",
    },
    "logging": {
        "level": "INFO",
    },
    "database": {
        "path": "",
        "use_default": "true",
    },
}

def load_config(config_path: Path) -> ConfigParser:
    config = ConfigParser()
    config.read_dict(DEFAULT_CONFIG)

    if config_path.exists():
        config.read(config_path, encoding='utf-8')
    else:
        config_path.parent.mkdir(parents=True, exist_ok=True)
        with config_path.open('w', encoding='utf-8') as f:
            config.write(f)

    return config

def save_config(config: ConfigParser, path: Path) -> None:
    with path.open('w', encoding='utf-8') as f:
        config.write(f)