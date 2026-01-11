#!/usr/bin/env python
# License: GPL v3 Copyright: 2026, Mateusz Jamróz
# pd/ui/dialogs/download/choose_dir.py

from PyQt6.QtWidgets import QFileDialog
from pathlib import Path
from pd.app_context import AppContext

def choose_download_dir(parent=None, ctx: AppContext = None) -> Path | None:
    i18n = ctx.i18n
    path = QFileDialog.getExistingDirectory(
        parent,
        i18n.t("download_dialog.select_directory")
    )
    if not path:
        return None
    return Path(path)