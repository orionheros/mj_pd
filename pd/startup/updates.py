#!/usr/bin/env python
# License: GPL v3 Copyright: 2026, Mateusz Jamróz
# pd/startup/updates.py

import os
import requests
from pd import __version__, __author__
from packaging.version import Version
from pd.platform.os_detect import Platform, get_platform

GITHUB_API = "https://api.github.com/repos/orionheros/mj_pd/releases"

def check_update(
        current_version: str, 
        platform: str,
        allow_prerelease: bool = False
    ) -> dict | None:

    try:
        r = requests.get(GITHUB_API, timeout=5)
        if r.status_code == 404:
            print ("No releases found on GitHub.")
            return None
        r.raise_for_status()
        releases = r.json()

        for rel in releases:
            if rel.get("prerelease") and not allow_prerelease:
                continue

            latest = rel["tag_name"].lstrip("v")
            if Version(latest) <= Version(current_version):
                return None  # No update available
            
            asset = _select_asset(rel["assets"], platform)
            if not asset:
                print(f"No suitable asset found for platform: {platform}")
                return None
            
            return {
                "version": latest,
                "browser_download_url": asset["browser_download_url"],
                "name": asset["name"],
                "changes": rel.get("body",) or "",
                "prerelease": rel.get("prerelease", False)
            }
        
        return None
    except Exception as e:
        print(f"Update check failed: {e}")
        return None

def _select_asset(assets: list[dict], platform: str) -> dict | None:
    print(f"Assets available: {[a['name'] for a in assets]}")
    for a in assets:
        name = a["name"].lower()
        if platform is Platform.WINDOWS and name.endswith(".exe"):
            return a
        elif platform is Platform.MACOS and name.endswith(".dmg"):
            return a
        elif platform is Platform.LINUX and (name.endswith(".appimage") or name.endswith(".deb") or name.endswith(".tar.gz")):
            return a
    return None

def download_crit_update():
        info = check_update(__version__, platform=get_platform(), allow_prerelease=False)
        if not info or "browser_download_url" not in info:
            raise RuntimeError("No critical update available to download.")
        url = info["browser_download_url"]
        filename = info["name"]
        dest_dir = os.path.join(os.path.expanduser("~"), "Downloads")
        dest = os.path.join(dest_dir, filename)
        r = requests.get(url, timeout=10)
        r.raise_for_status()
        with open(dest, 'wb') as f:
            f.write(r.content)
        return dest

def update_on_startup(current_version: str, platform: str) -> dict | None:
    """
    Check for updates on startup without allowing prerelease versions.
    Returns update info dict if an update is available, otherwise None,
    don't need to inform the user here.
    """
    try:
        r = requests.get(GITHUB_API, timeout=3)
        if r.status_code != 200:
            print (f"Update check failed with status code: {r.status_code}")
            return None
        r.raise_for_status()
        releases = r.json()

        for rel in releases:
            latest = rel["tag_name"].lstrip("v")
            if Version(latest) <= Version(current_version):
                print("DEBUG: No update available.")
                print(f"DEBUG: Current version: {current_version}, Latest version: {latest}")
                return None
            
            asset = _select_asset(rel["assets"], platform)
            if not asset:
                print(f"No suitable asset found for platform: {platform}")
                return None
            
            print(f"DEBUG: Update available: {latest}")
            return {
                "version": latest
            }
    except Exception as e:
        print(f"Update check failed: {e}")
        return None