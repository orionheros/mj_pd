#!/usr/bin/env python
# License: GPL v3 Copyright: 2026, Mateusz Jamróz
# pd/ui/widgets/settings.py

import os
import sys
import subprocess

from PyQt6.QtWidgets import (
    QVBoxLayout,
    QLabel,
    QDialog,
    QPushButton,
    QComboBox,
    QHBoxLayout,
    QApplication,
    QCheckBox
)

from pd.core.i18n import AVAILABLE_LANGUAGES
from pd.core.config import save_config


class SettingsDialog(QDialog):
    def __init__(self, ctx):
        super().__init__()
        self.ctx = ctx
        self.setMinimumSize(400, 300)
        self.setWindowTitle(self.ctx.i18n.t("settings.title"))
        self.init_ui()

    def init_ui(self):
        t = self.ctx.i18n.t
        layout = QVBoxLayout()
        label = QLabel(t("settings.title"))
        layout.addWidget(label)
        layout.addSpacing(10)

        #
        ## Language Selection
        self.language_combo = QComboBox()
        self.language_combo.setToolTip(t("settings.language_tooltip"))
        self.language_combo.setFixedWidth(100)

        for lang in AVAILABLE_LANGUAGES:
            self.language_combo.addItem(lang.native_name, lang.code)

        current_lang = self.ctx.config["general"].get("language", "en")
        index = self.language_combo.findData(current_lang)
        if index >= 0:
            self.language_combo.setCurrentIndex(index)

        self.language_combo.currentIndexChanged.connect(self._on_language_changed)

        layout.addWidget(QLabel(t("settings.language") + ":"))
        layout.addWidget(self.language_combo)
        layout.addSpacing(10)

        #
        ## Launcher on-off
        self.launcher = QCheckBox(t("settings.launcher_on_startup"))
        show_launcher = self.ctx.config["launcher"].getboolean("show_on_startup", fallback=False)
        self.launcher.setChecked(show_launcher)
        self.launcher.stateChanged.connect(self._on_launcher_changed)

        reload_btn = QPushButton(t("settings.restart"))
        reload_btn.clicked.connect(self._restart_app)

        ok_btn = QPushButton(t("settings.ok"))
        ok_btn.clicked.connect(self.close)

        btn_row = QHBoxLayout()
        btn_row.addWidget(reload_btn)
        btn_row.addWidget(ok_btn)

        layout.addWidget(self.launcher)
        layout.addStretch()
        layout.addLayout(btn_row)

        self.setLayout(layout)

    def _on_language_changed(self):
        code = self.language_combo.currentData()
        self.ctx.config["general"]["language"] = code
        save_config(self.ctx.config, self.ctx.paths.config / "config.ini")
    
    def _on_launcher_changed(self):
        show_launcher = self.launcher.isChecked()
        self.ctx.config["launcher"]["show_on_startup"] = "true" if show_launcher else "false"
        save_config(self.ctx.config, self.ctx.paths.config / "config.ini")

    def _restart_app(self):
        self._on_language_changed()
        self._on_launcher_changed()
        if os.environ.get("DEBUGPY_RUNNING"):
            print("DEBUG: Restarting application...")
            return
        
        executable = sys.executable
        args = sys.argv[1:]
        
        env = os.environ.copy()
        env.pop("_MEIPASS2", None)
        env.pop("PYTHONPATH", None)
        env.pop("PYTHONHOME", None)

        subprocess.Popen([executable] + args, env=env)

        QApplication.quit()
        sys.exit(0)