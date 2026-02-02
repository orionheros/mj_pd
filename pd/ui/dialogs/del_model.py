#!/usr/bin/env python
# License: GPL v3 Copyright: 2026, Mateusz Jamróz
# pd/ui/dialogs/del_model.py

from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton, QMessageBox
from pd.app_context import AppContext

class DelModelDialog(QDialog):
    def __init__(self, ctx: AppContext, parent=None):
        super().__init__(parent)
        self.ctx = ctx
        self.pd_service = ctx.pd_service
        self.i18n = ctx.i18n

        self.setWindowTitle(self.i18n.t("delete_model.title"))
        self.setMinimumWidth(300)

        layout = QVBoxLayout(self)

        label = QLabel(self.i18n.t("delete_model.confirmation"))
        layout.addWidget(label)

        delete_button = QPushButton(self.i18n.t("delete_model.delete_button"))
        delete_button.clicked.connect(self.delete_model)
        layout.addWidget(delete_button)

        cancel_button = QPushButton(self.i18n.t("delete_model.cancel_button"))
        cancel_button.clicked.connect(self.reject)
        layout.addWidget(cancel_button)

    def delete_model(self):
        try:
            pass
        except Exception as e:
            QMessageBox.critical(self, self.i18n.t("delete_model.title"), self.i18n.t("delete_model.error_generic") + ": \n" + str(e))
            self.reject()