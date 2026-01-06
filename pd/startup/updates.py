#!/usr/bin/env python
# License: GPL v3 Copyright: 2026, Mateusz Jamróz
# pd/startup/updates.py

import requests
from PyQt6.QtCore import QObject, pyqtSignal
from pd import __version__
from pd.platform.os_detect import get_platform

class UpdateWorker(QObject):
    finished = pyqtSignal(bool, str, str)  # is_update_available, latest_version, release_url
    def run(self):
        try:
            response = requests.get("https://api.github.com/repos/mjpd/pd-ui-manager/releases/latest", timeout=5)
            response.raise_for_status()
            latest_release = response.json()
            latest_version = latest_release["tag_name"].lstrip("v")

            if latest_version != __version__:
                self.finished.emit(True, latest_version, latest_release["html_url"])
            else:
                self.finished.emit(False, latest_version, None)
        except requests.RequestException:
            self.finished.emit(False, "", "")