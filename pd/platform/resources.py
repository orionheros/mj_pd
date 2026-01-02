#!/usr/bin/env python
# License: GPL v3 Copyright: 2026, Mateusz Jamróz
# pd/platform/resources.py

import sys
from pathlib import Path
from PyQt6.QtGui import QIcon

from pd.platform.paths import AppPaths

def resource_path(relative: str) -> Path:
    """ Get absolute path to resource, works for dev and for PyInstaller """
    if hasattr(sys, '_MEIPASS'):
        return Path(sys._MEIPASS) / relative
    else:
        base = Path(__file__).resolve().parents[2] # pd/
    
    return base / relative

class ResourceManager:
    def __init__(self):
        self._icon_cache: dict[str, QIcon] = {}

    def icon(self, name: str) -> QIcon:
        """
        Get QIcon by name, caching it for future use.
        """
        if name in self._icon_cache:
            return self._icon_cache[name]
        
        icon_path = resource_path(f"pd/assets/icons/{name}.png")

        if not icon_path.exists():
            raise FileNotFoundError(f"Icon '{name}' not found at path: {icon_path}")
        
        icon = QIcon(str(icon_path))
        self._icon_cache[name] = icon
        return icon