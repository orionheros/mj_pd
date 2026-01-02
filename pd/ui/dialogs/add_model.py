#!/usr/bin/env python
# License: GPL v3 Copyright: 2026, Mateusz Jamróz
# pd/ui/dialogs/add_model.py

from PyQt6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QFormLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QMessageBox
)

from pd.app_context import AppContext

class AddModelDialog(QDialog):
    def __init__(self, ctx: AppContext):
        super().__init__()
        self.setWindowTitle(ctx.i18n.t("add_model.title"))
        self.ctx = ctx
        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout(self)

        form = QFormLayout()

        label = QLabel(self.ctx.i18n.t("add_model.label")) # Informational label
        label.setStyleSheet("font-weight: bold;")

        self.model_name = QLineEdit()

        form.addRow(self.ctx.i18n.t("fields.model_name") + ":", self.model_name)

        layout.addWidget(label)
        layout.addSpacing(10)
        layout.addLayout(form)
        layout.addSpacing(10)

        # Buttons
        btn_add = QPushButton(self.ctx.i18n.t("buttons.confirm"))
        btn_add.clicked.connect(self._on_add_clicked)

        layout.addWidget(btn_add)

        self.setLayout(layout)

    def _on_add_clicked(self):
        name = self.model_name.text().strip()

        if not name:
            QMessageBox.warning(self, self.ctx.i18n.t("add_model.title"),
                                self.ctx.i18n.t("add_model.error_empty_name"))
            return
        try:
            self.ctx.pd_service.add_model(name)
            QMessageBox.information(self, self.ctx.i18n.t("add_model.title"),
                                    self.ctx.i18n.t("add_model.success"))
            self.accept()
        except Exception as e:
            QMessageBox.critical(self, self.ctx.i18n.t("add_model.title"),
                                 self.ctx.i18n.t("add_model.error_generic") + f"\n{str(e)}")