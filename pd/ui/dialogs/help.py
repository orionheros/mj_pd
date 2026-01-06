#!/usr/bin/env python
# License: GPL v3 Copyright: 2026, Mateusz Jamróz
# pd/ui/dialogs/about.py

from PyQt6.QtWidgets import (
    QDialog, 
    QVBoxLayout, 
    QLabel, 
    QPushButton, 
    QScrollArea
)

from pd.app_context import AppContext

class HelpDialog(QDialog):
    def __init__(self, ctx: AppContext):
        super().__init__()
        self.setWindowTitle(ctx.i18n.t("help.title"))
        self.ctx = ctx
        self._build_ui()
        self.resize(600, 300)
        self.setMinimumWidth(600)

    def _build_ui(self):
        layout = QVBoxLayout(self)

        # Help text area
        help_text = QLabel(self.ctx.i18n.t("help.content"))
        help_text.setWordWrap(True)


        # Building area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setWidget(help_text)

        layout.addWidget(scroll)

        btn_close = QPushButton(self.ctx.i18n.t("buttons.close"))
        btn_close.clicked.connect(self.accept)

        layout.addWidget(btn_close)