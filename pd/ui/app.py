#!/usr/bin/env python3
# License: GPL v3 Copyright: 2026, Mateusz Jamróz
# pd/ui/app.py

import sys

from pd.ui.main_window import MainWindow

def run_ui(ctx, app) -> None:

    window = MainWindow(ctx)
    window.show()

    sys.exit(app.exec())