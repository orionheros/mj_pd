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
    QCheckBox,
    QLineEdit,
)

from pd.core.i18n import AVAILABLE_LANGUAGES
from pd.core.config import save_config


class SettingsDialog(QDialog):
    def __init__(self, ctx):
        super().__init__()
        self.ctx = ctx
        self.initial_lang = self.ctx.config["general"].get("language", "en")
        self.setMinimumSize(400, 300)
        self.setWindowTitle(self.ctx.i18n.t("settings.title"))
        self.init_ui()

    def init_ui(self):
        t = self.ctx.i18n.t
        layout = QVBoxLayout()

        label = QLabel(t("settings.title1"))
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
        self.launcher.stateChanged.connect(self._save_settings)

        #
        ## Path for database on-off
        # Show launcher checkbox for choosing database path
        self.db_show_ask_cb = QCheckBox(t("settings.db_selector_on_startup"))
        self.db_show_ask_cb.setChecked(self.ctx.config["database"].getboolean("show_ask"))

        #
        ## Default path for database on-off
        self.db_use_default_cb = QCheckBox(t("settings.db_use_default"))
        self.db_use_default_cb.setChecked(self.ctx.config.getboolean("database", "use_default"))
        self.db_use_default_cb.setToolTip(t("settings.db_use_default_tooltip"))

        # Label i przycisk do otwarcia folderu bazy danych
        db_path = self.ctx.config["database"].get("path", "")
        if not db_path:
            db_path = str(self.ctx.paths.data / "pd.db")
        self.db_folder_label = QLineEdit(db_path)
        self.db_folder_label.setReadOnly(True)
        self.db_folder_label.setToolTip(t("settings.db_path_tooltip"))
        db_folder_row = QHBoxLayout()
        db_folder_row.addWidget(self.db_folder_label)

        self.lang_restart_info = QLabel(t("settings.language_restart_info"))
        self.lang_restart_info.setStyleSheet("color: gray; font-style: italic;")
        self.lang_restart_info.setVisible(False)

            # Restarting app don't working properly now
            # It's seems to be problem with PyQt6 and numpy`
            # reload_btn = QPushButton(t("settings.restart"))
            # reload_btn.clicked.connect(self._restart_app)

        ok_btn = QPushButton(t("settings.ok"))
        ok_btn.clicked.connect(self._save_and_close)

        btn_row = QHBoxLayout()
            # btn_row.addWidget(reload_btn)
        btn_row.addWidget(ok_btn)

        layout.addWidget(self.launcher)
        layout.addWidget(self.db_show_ask_cb)
        layout.addWidget(self.db_use_default_cb)
        layout.addLayout(db_folder_row)
        layout.addStretch()
        layout.addWidget(self.lang_restart_info)
        layout.addLayout(btn_row)

        self.setLayout(layout)

    def _open_db_folder(self, db_path):
        folder = os.path.dirname(db_path)
        if os.name == 'nt':
            os.startfile(folder)
        elif sys.platform == 'darwin':
            subprocess.Popen(['open', folder])
        else:
            subprocess.Popen(['xdg-open', folder])

    def _on_language_changed(self):
        code = self.language_combo.currentData()
        if code != self.initial_lang:
            self.lang_restart_info.setVisible(True)
        else:
            self.lang_restart_info.setVisible(False)
        self.ctx.config["general"]["language"] = code
        save_config(self.ctx.config, self.ctx.paths.config / "config.ini")
    
    def _save_settings(self):
        cfg = self.ctx.config

        cfg["launcher"]["show_on_startup"] = "true" if self.launcher.isChecked() else "false"

        cfg["database"]["show_ask"] = "true" if self.db_show_ask_cb.isChecked() else "false"
        cfg["database"]["use_default"] = "true" if self.db_use_default_cb.isChecked() else "false"

        save_config(cfg, self.ctx.paths.config / "config.ini")

    def _save_and_close(self):
        self._on_language_changed()
        self._save_settings()
        self.accept()

    def _restart_app(self):
        self._on_language_changed()
        self._save_settings()
        if os.environ.get("DEBUGPY_RUNNING"):
            print("DEBUG: Restarting application...")
            return
        
        executable = sys.executable
        args = sys.argv[1:]
        print("Restarting application...")
        os.execv(executable, [executable] + args)