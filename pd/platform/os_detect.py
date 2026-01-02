#!/usr/bin/env python
# License: GPL v3 Copyright: 2026, Mateusz Jamróz
# pd/platform/os_detect.py

import platform as pfm
from enum import Enum, auto

class Platform(Enum):
    WINDOWS = auto()
    MACOS = auto()
    LINUX = auto()

def get_platform() -> Platform:
    system = pfm.system()
    if system == "Windows":
        return Platform.WINDOWS
    elif system == "Darwin":
        return Platform.MACOS
    elif system == "Linux":
        return Platform.LINUX
    else:
        raise RuntimeError(f"Unsupported platform: {system}")