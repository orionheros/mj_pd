#!/usr/bin/env python
# License: GPL v3 Copyright: 2026, Mateusz Jamróz
# pd/launcher/launcher.py

"""
The module features a startup launcher for selecting the language 
and the program data package (PD; additional packages coming soon).
"""
from pathlib import Path
import json
from PyQt6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QStackedWidget,
    QWidget,
    QLabel,
    QComboBox,
    QPushButton,
    QListWidget,
    QCheckBox,
    QListWidgetItem,
    QMessageBox
)
from PyQt6.QtCore import Qt


class Launcher(QDialog):
    def __init__(self, config, paths):
        super().__init__()
        self.config = config
        self.paths = paths

        self.launcher_langs_path = Path(__file__).parent / "langs"
        self.current_translations = {}

        self.selected_lang = config["general"].get("language", "en")
        self._load_translations(self.selected_lang)

        self._build_ui()
        self.retranslate_ui()

    def _load_translations(self, lang_code):
        lang_file = self.launcher_langs_path / f"{lang_code}.json"
        try:
            with open(lang_file, 'r', encoding='utf-8') as f:
                self.current_translations = json.load(f)
        except FileNotFoundError:
            if lang_code != "en":
                self._load_translations("en")

    def _build_ui(self):
        self.setFixedSize(400, 300)
        self.layout = QVBoxLayout(self)
        self.stack = QStackedWidget()
        self.layout.addWidget(self.stack)

        # Page 1: Language Selection
        self.page1 = QWidget()
        self.layout1 = QVBoxLayout(self.page1)
        self.label_lang = QLabel()
        self.lang_combo = QComboBox()

        langs = [
            ("English", "en"),
            ("Polski", "pl"),
        ]
        for name, code in langs:
            self.lang_combo.addItem(name, code)

        idx = self.lang_combo.findData(self.selected_lang)
        self.lang_combo.setCurrentIndex(idx if idx != -1 else 0)

        self.lang_combo.currentIndexChanged.connect(self._on_lang_changed)

        self.next_btn = QPushButton()
        self.next_btn.clicked.connect(lambda: self.stack.setCurrentIndex(1))

        self.layout1.addWidget(self.label_lang)
        self.layout1.addWidget(self.lang_combo)
        self.layout1.addStretch()
        self.layout1.addWidget(self.next_btn)

        # Page 2: Module Selection
        self.page2 = QWidget()
        self.layout2 = QVBoxLayout(self.page2)
        self.label_module = QLabel()
        self.module_list = QListWidget()

        item = QListWidgetItem("PD (Pump Duse)")
        item.setData(Qt.ItemDataRole.UserRole, "pd")
        self.module_list.addItem(item)

        item2 = QListWidgetItem(self.current_translations.get("give_idea"))
        font = item2.font()
        font.setItalic(True)
        item2.setFont(font)
        item2.setData(Qt.ItemDataRole.UserRole, "idea")
        item2.setFlags(item2.flags() & ~Qt.ItemFlag.ItemIsSelectable & ~Qt.ItemFlag.ItemIsEnabled)
        self.module_list.addItem(item2)

        # test item
        # item3 = QListWidgetItem(self.current_translations.get("ui"))
        # item3.setData(Qt.ItemDataRole.UserRole, "ui")
        # self.module_list.addItem(item3)

        self.default_check = QCheckBox()
        self.default_check.setToolTip(self.current_translations.get("default_tooltip"))

        self.btn_row = QHBoxLayout()
        self.back_btn = QPushButton()
        self.back_btn.clicked.connect(lambda: self.stack.setCurrentIndex(0))
        self.finish_btn = QPushButton()
        self.finish_btn.clicked.connect(self._finish)
        self.btn_row.addWidget(self.back_btn)
        self.btn_row.addWidget(self.finish_btn)

        self.layout2.addWidget(self.label_module)
        self.layout2.addWidget(self.module_list)
        self.layout2.addWidget(self.default_check)
        self.layout2.addLayout(self.btn_row)

        self.stack.addWidget(self.page1)
        self.stack.addWidget(self.page2)

    def _on_lang_changed(self):
        new_lang = self.lang_combo.currentData()
        self.selected_lang = new_lang
        self._load_translations(new_lang)
        self.retranslate_ui()

    def retranslate_ui(self):
        t = self.current_translations
        self.setWindowTitle(t.get("window_title", "Launcher"))
        self.label_lang.setText(t.get("select_language", "Select Language:"))
        self.next_btn.setText(t.get("next", "Next"))
        self.label_module.setText(t.get("select_module", "Select Module to Launch:"))
        self.default_check.setText(t.get("set_as_default", "Set as Default"))
        self.default_check.setToolTip(t.get("default_tooltip", ""))
        self.back_btn.setText(t.get("back", "Back"))
        self.finish_btn.setText(t.get("finish", "Finish"))

    def _finish(self):
        selected = self.module_list.selectedItems()

        if not selected:
            t = self.current_translations
            QMessageBox.warning(
                self,
                t.get("no_selection_title"),
                t.get("no_selection_msg")
            )
            return
        
        current_item = selected[0]
        self.selected_module = current_item.data(Qt.ItemDataRole.UserRole)
        self.set_default = self.default_check.isChecked()
        self.accept()

    def get_results(self):
        return self.selected_lang, self.selected_module, self.set_default