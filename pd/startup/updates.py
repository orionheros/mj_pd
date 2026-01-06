#!/usr/bin/env python
# License: GPL v3 Copyright: 2026, Mateusz Jamróz
# pd/startup/updates.py

import requests
from pd import __version__, __author__
from packaging.version import Version
from pathlib import Path
from typing import Dict, Any

GITHUB_API = "https://api.github.com/repos/mjpd/pd-ui-manager/releases/latest"

def check_update(current_version: str, platform: str) -> dict | None:
    try:
        r = requests.get(GITHUB_API, timeout=5)

        if r.status_code == 404:
            print ("No releases found on GitHub.")
            return None
        r.raise_for_status()
        data = r.json()

        latest = data["tag_name"].lstrip("v")
        if Version(latest) <= Version(current_version):
            return None
        
        asset = _select_asset(data["assets"], platform)
        if not asset:
            return None
        
        return {
            "version": latest,
            "url": asset["browser_download_url"],
            "filename": asset["name"],
            "changelog": data.get("body", "")
        }
    except Exception as e:
        print(f"Update check failed: {e}")
        return None

def _select_asset(assets: list[dict], platform: str) -> dict | None:
    for a in assets:
        name = a["name"].lower()
        if platform == "windows" and name.endswith(".exe"):
            return a
        elif platform == "macos" and name.endswith(".dmg"):
            return a
        elif platform == "linux" and (name.endswith(".appimage") or name.endswith(".deb") or name.endswith(".tar.gz")):
            return a
    return None

def download_update(update_info: Dict[str, Any], dest_dir: Path) -> Path:
    url = update_info["url"]
    filename = update_info["filename"]
    dest_path = dest_dir / filename

    dest_dir.mkdir(parents=True, exist_ok=True)

    with requests.get(url, stream=True, timeout=30) as r:
        r.raise_for_status()
        with open(dest_path, 'wb') as f:
            for chunk in r.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)

    return dest_path