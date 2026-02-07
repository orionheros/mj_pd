#!/usr/bin/env python
# License: GPL v3 Copyright: 2026, Mateusz Jamróz
# pd/core/ui_state.py

from pd.core.config import load_config, save_config

"""
This module handles saving and restoring the UI state (window geometry, splitter states...) to/from the config file.
"""

def restore_settings(self):
    config = load_config(self.paths.config / "config.ini")

    if not config.has_section("ui"):
        return

    geometry_hex = config.get("ui", "geometry", fallback="").strip()
    if geometry_hex:
        try:
            self.restoreGeometry(bytes.fromhex(geometry_hex))
        except Exception as e:
            print(f"Invalid geometry data in config: {e}")

    window_state_hex = config.get("ui", "window_state", fallback="").strip()
    if window_state_hex:
        try:
            self.restoreState(bytes.fromhex(window_state_hex))
        except Exception as e:
            print(f"Invalid window state data in config: {e}")

def restore_splitter_state(self):
    config = load_config(self.paths.config / "config.ini")
    splitter_state_hex = config.get("ui", "splitter_state", fallback="").strip()
    if not splitter_state_hex:
        return False
    if splitter_state_hex and hasattr(self, "splitter"):
        try:
            restored = self.splitter.restoreState(bytes.fromhex(splitter_state_hex))
            return restored
        except Exception as e:
            print(f"Invalid splitter state data in config: {e}")
            return False

def save_settings(self, config):
    config["ui"]["geometry"] = self.saveGeometry().toHex().data().decode()
    config["ui"]["window_state"] = self.saveState().toHex().data().decode()

def save_splitter_state(self, config):
    if hasattr(self, "_last_splitter_pos"):
        config["ui"]["splitter_state"] = self._last_splitter_pos.toHex().data().decode()