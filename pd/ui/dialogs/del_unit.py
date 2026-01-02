#!/usr/bin/env python
# License: GPL v3 Copyright: 2026, Mateusz Jamróz
# pd/ui/dialogs/del_unit.py

from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton, QMessageBox
from pd.app_context import AppContext

class DelModelDialog(QDialog):
    def __init__(self, ctx: AppContext, pd_id: int, parent=None):
        super().__init__(parent)
        self.ctx = ctx
        self.pd_service = ctx.pd_service
        self.i18n = ctx.i18n
        self.pd_id = pd_id

        self.setWindowTitle(self.i18n.t("delete_unit.title"))
        self.setMinimumWidth(300)

        layout = QVBoxLayout(self)

        label = QLabel(self.i18n.t("delete_unit.confirmation"))
        layout.addWidget(label)

        delete_button = QPushButton(self.i18n.t("delete_unit.delete_button"))
        delete_button.clicked.connect(self.delete_unit)
        layout.addWidget(delete_button)

        cancel_button = QPushButton(self.i18n.t("delete_unit.cancel_button"))
        cancel_button.clicked.connect(self.reject)
        layout.addWidget(cancel_button)

    def delete_unit(self):
        try:
            self.pd_service.delete_unit(self.pd_id)
            QMessageBox.information(self, self.i18n.t("delete_unit.title"), self.i18n.t("delete_unit.deleted_message"))
            self.accept()
        except Exception as e:
            QMessageBox.critical(self, self.i18n.t("delete_unit.title"), self.i18n.t("delete_unit.error_generic") + ": \n" + str(e))
            self.reject()