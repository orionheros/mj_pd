#!/usr/bin/env python3
# License: GPL v3 Copyright: 2026, Mateusz Jamróz
# pd/ui/app.py

import sys

from PyQt6.QtWidgets import QApplication

from pd.ui.main_window import MainWindow

def run_ui(ctx) -> None:
    app = QApplication(sys.argv)

    window = MainWindow(ctx)
    window.show()

    sys.exit(app.exec())