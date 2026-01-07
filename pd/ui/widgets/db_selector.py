#!/usr/bin/env python
# License: GPL v3 Copyright: 2026, Mateusz Jamróz
# pd/ui/db_selector.py

from PyQt6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QCheckBox,
    QLineEdit,
    QPushButton,
    QHBoxLayout,
    QFileDialog
)
from pathlib import Path

class DatabaseSelector(QDialog):
    def __init__(self, config, paths, i18n):
        super().__init__()
        self.config = config
        self.paths = paths
        self.i18n = i18n
        self.selected_db_path = config["database"].get("path", "")

        self.setWindowTitle(self.i18n.t("db_selector.title"))
        self.setFixedWidth(450)
        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout(self)

        self.default_cb = QCheckBox(self.i18n.t("db_selector.use_default"))
        is_default = self.config["database"].getboolean("use_default", fallback=False)
        self.default_cb.setChecked(is_default)
        self.default_cb.stateChanged.connect(self._toggle_manual_selection)
        layout.addWidget(self.default_cb)

        self.path_input = QLineEdit(self)
        self.path_input.setText(self.selected_db_path)
        self.browse_file_btn = QPushButton(self.i18n.t("db_selector.browse"))
        self.browse_file_btn.setToolTip(self.i18n.t("db_selector.browse_tooltip"))
        self.browse_folder_btn = QPushButton(self.i18n.t("db_selector.browse_folder"))
        self.browse_folder_btn.setToolTip(self.i18n.t("db_selector.browse_folder_tooltip"))

        path_layout = QHBoxLayout()
        path_layout.addWidget(self.path_input)
        path_layout.addWidget(self.browse_file_btn)
        path_layout.addWidget(self.browse_folder_btn)
        layout.addLayout(path_layout)

        self.browse_file_btn.clicked.connect(self._browse_file)
        self.browse_folder_btn.clicked.connect(self._browse_folder)

        btn_layout = QHBoxLayout()
        save_btn = QPushButton(self.i18n.t("db_selector.save"))
        save_btn.clicked.connect(self._save_and_close)
        btn_layout.addStretch()
        btn_layout.addWidget(save_btn)
        layout.addLayout(btn_layout)

        self._toggle_manual_selection()

    def _toggle_manual_selection(self):
        enabled = not self.default_cb.isChecked()
        self.path_input.setEnabled(enabled)
        self.browse_file_btn.setEnabled(enabled)
        self.browse_folder_btn.setEnabled(enabled)

    def _browse_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, self.i18n.t("db_selector.select_file"))
        if file_path:
            self.path_input.setText(file_path)

    def _browse_folder(self):
        folder = QFileDialog.getExistingDirectory(self, self.i18n.t("db_selector.select_folder"))
        if folder:
            full_path = Path(folder) / "pd.db"
            self.path_input.setText(str(full_path))

    def _save_and_close(self):
        self.selected_db_path = self.path_input.text().strip()
        self.accept()

def get_database_path(config, paths, i18n):
    if config["database"].getboolean("use_default") and config["database"].get("path") == "":
        return paths.data / "pd.db"
    
    saved_path = config["database"].get("path")
    if saved_path and not config["database"].getboolean("use_default"):
        return Path(saved_path)
    
    selector = DatabaseSelector(config, paths, i18n)
    if selector.exec() == QDialog.DialogCode.Accepted:
        config["database"]["use_default"] = str(selector.default_cb.isChecked()).lower()

        if selector.default_cb.isChecked():
            final_path = paths.data / "pd.db"
            config["database"]["path"] = ""
        else:
            final_path = Path(selector.selected_db_path)
            config["database"]["path"] = str(final_path)

        return final_path
    
    return paths.data / "pd.db"  # Fallback to default if dialog is cancelled

