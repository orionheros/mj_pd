#!/usr/bin/env python
# License: GPL v3 Copyright: 2026, Mateusz Jamróz
# pd/ui.dialogs/download/download_worker.py

from PyQt6.QtCore import QThread, pyqtSignal
import requests
from pathlib import Path

class DownloadWorker(QThread):
    progress = pyqtSignal(int)
    finished = pyqtSignal(str)
    error = pyqtSignal(str)

    def __init__(self, update_info: dict, dest_dir: Path):
        super().__init__()
        self.url = update_info["browser_download_url"]
        self.filename = update_info["name"]
        self.dest_dir = dest_dir

    def run(self):
        try:
            self.dest_dir.mkdir(parents=True, exist_ok=True)
            dest_path = self.dest_dir / self.filename

            with requests.get(self.url, stream=True, timeout=10) as r:
                r.raise_for_status()

                total = int(r.headers.get('content-length', 0))
                downloaded = 0

                with open(dest_path, 'wb') as f:
                    for chunk in r.iter_content(chunk_size=8192):
                        if not chunk:
                            continue
                        f.write(chunk)
                        downloaded += len(chunk)

                        if total:
                            percent = int(downloaded * 100 / total)
                            self.progress.emit(percent)

            self.finished.emit(str(dest_path))
        except Exception as e:
            self.error.emit(str(e))