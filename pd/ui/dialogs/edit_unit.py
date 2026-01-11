#!/usr/bin/env python
# License: GPL v3 Copyright: 2026, Mateusz Jamróz
# pd/ui/dialogs/edit_unit.py

from PyQt6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QHBoxLayout,
    QFormLayout,
    QComboBox,
) 
from pd.app_context import AppContext
from pd.core.models import PD


class EditUnitDialog(QDialog):
    def __init__(self, ctx: AppContext, pd_id: str, row: int):
        super().__init__()
        self.ctx = ctx
        self.pd_id = pd_id
        self.row = row
        self.setWindowTitle(self.ctx.i18n.t("edit_unit.title"))
        self.setMinimumSize(300, 150)
        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout(self)

        form = QFormLayout()

        unit_data = self.ctx.pd_service.unit_info(self.pd_id)

        label = QLabel(self.ctx.i18n.t("edit_unit.label")) # Informational label
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

        self.model_id.setCurrentIndex(self.model_id.findData(unit_data.model_id))
        self.opening_pressure.setCurrentIndex(self.opening_pressure.findData(unit_data.opening_pressure_id))
        self.washer1.setText(str(f"{unit_data.washer1_thickness:.2f}"))
        self.washer2.setText(str(f"{unit_data.washer2_thickness:.2f}"))
        self.spring_length.setText(str(f"{unit_data.spring_length:.2f}"))
        self.final_pressure.setText(str(f"{unit_data.final_pressure:.0f}"))

        layout.addWidget(label)
        layout.addSpacing(10)
        layout.addLayout(form)

        # Buttons
        btn_ok = QPushButton(self.ctx.i18n.t("buttons.save_changes"))
        btn_cancel = QPushButton(self.ctx.i18n.t("buttons.cancel"))

        btn_ok.setDefault(True)

        btn_ok.clicked.connect(self._on_accept)
        btn_cancel.clicked.connect(self.reject)

        btn_row = QHBoxLayout()
        btn_row.addWidget(btn_ok)
        btn_row.addWidget(btn_cancel)

        layout.addLayout(btn_row)

    def _on_accept(self):
        data = self._collect_data()
        pd_obj = PD(
            id=self.pd_id,
            model_id=data["model_id"],
            washer1_thickness=data["washer1_thickness"],
            washer2_thickness=data["washer2_thickness"],
            spring_length=data["spring_length"],
            final_pressure=data["final_pressure"],
            opening_pressure_id=data["opening_pressure_id"]
        )

        self.ctx.pd_service.update_unit(pd_obj)
        self.accept()

    def _collect_data(self) -> dict:
        def parse_float(val):
            return float(val.replace(",", "."))

        return {
            "model_id": self.model_id.currentData(),
            "washer1_thickness": parse_float(self.washer1.text()),
            "washer2_thickness": parse_float(self.washer2.text()),
            "spring_length": parse_float(self.spring_length.text()),
            "final_pressure": parse_float(self.final_pressure.text()),
            "opening_pressure_id": self.opening_pressure.currentData()
        }