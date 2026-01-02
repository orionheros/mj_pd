#!/usr/bin/env python
# License: GPL v3 Copyright: 2026, Mateusz Jamróz
# pd/ui/dialogs/add_new.py

from PyQt6.QtWidgets import (
    QDialog, 
    QVBoxLayout,
    QHBoxLayout,
    QLabel, 
    QLineEdit,
    QFormLayout, 
    QPushButton,
    QMessageBox,
    QComboBox
)

from pd.app_context import AppContext

class AddNewDialog(QDialog):
    def __init__(self, ctx: AppContext, on_accept_callback=None):
        super().__init__()
        self.setWindowTitle(ctx.i18n.t("add_new.title"))
        self.ctx = ctx
        self._on_accept_callback = on_accept_callback
        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout(self)

        form = QFormLayout()

        label = QLabel(self.ctx.i18n.t("add_new.label")) # Informational label
        label.setStyleSheet("font-weight: bold;")

        self.model_id = QComboBox()
        self.opening_pressure = QComboBox()
        for mid, mname in self.ctx.pd_service.get_models():
            self.model_id.addItem(f"{mname}", userData=mid)
        for pid, pval in self.ctx.pd_service.get_opening_pressures():
            self.opening_pressure.addItem(f"{pval}", userData=pid)

        self.washer1 = QLineEdit()
        self.washer2 = QLineEdit()
        self.spring_length = QLineEdit()
        self.final_pressure = QLineEdit()

        form.addRow(self.ctx.i18n.t("fields.model_id") + ":", self.model_id)
        form.addRow(self.ctx.i18n.t("fields.opening_pressure") + ":", self.opening_pressure)
        form.addRow(self.ctx.i18n.t("fields.washer1") + ":", self.washer1)
        form.addRow(self.ctx.i18n.t("fields.washer2") + ":", self.washer2) 
        form.addRow(self.ctx.i18n.t("fields.spring_length") + ":", self.spring_length)
        form.addRow(self.ctx.i18n.t("fields.final_pressure") + ":", self.final_pressure)

        # Info label
        text = self.ctx.i18n.t("add_new.instructions")
        esi_text = self.ctx.i18n.t("add_new.info_ESI")
        info_label = QLabel(text)
        info_label.setWordWrap(True)
        esi_label = QLabel(esi_text)
        esi_label.setStyleSheet("color: gray;")
        esi_label.setWordWrap(True)

        layout.addWidget(label)
        layout.addSpacing(10)
        layout.addLayout(form)
        layout.addSpacing(10)
        layout.addWidget(info_label)
        layout.addSpacing(5)
        layout.addWidget(esi_label)

        # Buttons
        btn_new = QPushButton(self.ctx.i18n.t("buttons.save"))
        btn_new.setToolTip(self.ctx.i18n.t("buttons.save_add_tooltip"))
        btn_ok = QPushButton(self.ctx.i18n.t("buttons.add"))
        btn_cancel = QPushButton(self.ctx.i18n.t("buttons.cancel"))

        btn_ok.setDefault(True)

        btn_new.clicked.connect(self._save_and_new)
        btn_ok.clicked.connect(self._on_accept)
        btn_cancel.clicked.connect(self.reject)

        btn_row = QHBoxLayout()
        btn_row.addWidget(btn_new)
        btn_row.addWidget(btn_ok)
        btn_row.addWidget(btn_cancel)

        layout.addLayout(btn_row)

    def _save(self):
        try:
            data = self._collect_data()
            self.ctx.pd_service.add_new(**data)
        except Exception as e:
            QMessageBox.critical(
                self,
                self.ctx.i18n.t("errors.title"),
                str(e)
            )

    def _on_accept(self):
        try:
            self._save()
            self.accept()
            if self._on_accept_callback:
                self._on_accept_callback()
        except Exception as e:
            QMessageBox.critical(
                self,
                self.ctx.i18n.t("errors.title"),
                str(e)
            )

    def _save_and_new(self):
        try:
            self._save()
            self._clear_fields()
            self.model_id.setFocus()
        except Exception as e:
            QMessageBox.critical(
                self,
                self.ctx.i18n.t("errors.title"),
                str(e)
            )


    def _collect_data(self):
        def parse_float(val):
            return float(val.replace(",", "."))

        return {
            "model_id": self.model_id.currentData(),
            "washer1": parse_float(self.washer1.text()),
            "washer2": parse_float(self.washer2.text()),
            "spring_length": parse_float(self.spring_length.text()),
            "final_pressure": parse_float(self.final_pressure.text()),
            "opening_pressure": self.opening_pressure.currentData()
        }

    def _clear_fields(self):
        self.washer1.clear()
        self.washer2.clear()
        self.spring_length.clear()
        self.final_pressure.clear()
        

