#!/usr/bin/env python
# License: GPL v3 Copyright: 2026, Mateusz Jamróz
# pd/platform/paths.py

from pathlib import Path
from pd.platform.os_detect import Platform

APP_NAME = "PDApp"

class AppPaths:
    def __init__(self, base: Path):
        self.base = base
        self.config = base / "config"
        self.data = base / "data"
        self.logs = base / "logs"
        
        self.config.mkdir(parents=True, exist_ok=True)
        self.data.mkdir(parents=True, exist_ok=True)
        self.logs.mkdir(parents=True, exist_ok=True)
        
def init_paths(platform: Platform) -> AppPaths:
    if platform == Platform.WINDOWS:
        base = Path.home() / "AppData" / "Local" / APP_NAME
    elif platform == Platform.LINUX:
        base = Path.home() / ".config" / APP_NAME
    elif platform == Platform.MACOS:
        base = Path.home() / "Library" / "Application Support" / APP_NAME
    else:
        raise RuntimeError(f"Unsupported platform: {platform}")
    
    base.mkdir(parents=True, exist_ok=True)
    return AppPaths(base)

