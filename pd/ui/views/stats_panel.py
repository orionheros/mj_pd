#!/usr/bin/env python
# License: GPL v3 Copyright: 2026, Mateusz Jamróz
# pd/ui/views/stats_panel.py

from PyQt6.QtWidgets import (
    QWidget,
    QFormLayout,
    QLabel,
    QVBoxLayout,
    QSlider,
    QHBoxLayout,
    QToolButton
)
from PyQt6.QtCore import Qt, pyqtSignal

class StatsPanel(QWidget):
    virtual_lower_changed = pyqtSignal(float)
    def __init__(self, ctx, parent=None):
        super().__init__(parent)
        self.ctx = ctx
        self.i18n = ctx.i18n

        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.setAlignment(Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignHCenter)

        layout = QFormLayout()

        self.avg_lower = QLabel()
        self.avg_spring = QLabel()
        self.avg_upper = QLabel()
        self.avg_total = QLabel()

        self.median_lower = QLabel()
        self.median_upper = QLabel()

        self.common = QLabel()
        self.common.setToolTip(self.i18n.t("stats_panel.common_config_tooltip"))

        self.virtual_label = QLabel("--")
        self.virtual_slider = QSlider(Qt.Orientation.Horizontal)

        self.virtual_slider.setMinimum(0)
        self.virtual_slider.setMaximum(200)
        self.virtual_slider.setSingleStep(1)
        self.virtual_slider.setPageStep(1)

        self.virtual_slider.valueChanged.connect(self._on_virtual_changed)

        self.virtual_upper_label = QLabel("--")

        # Arrow buttons and slider
        self.btn_minus = QToolButton()
        self.btn_minus.setText("◀")
        self.btn_minus.setAutoRepeat(True)
        self.btn_minus.setAutoRepeatDelay(300)
        self.btn_minus.setAutoRepeatInterval(60)

        self.btn_plus = QToolButton()
        self.btn_plus.setText("▶")
        self.btn_plus.setAutoRepeat(True)
        self.btn_plus.setAutoRepeatDelay(300)
        self.btn_plus.setAutoRepeatInterval(60)

        self.btn_minus.clicked.connect(self._step_down)
        self.btn_plus.clicked.connect(self._step_up)

        slider_row = QHBoxLayout()
        slider_row.addWidget(self.btn_minus)
        slider_row.addWidget(self.virtual_slider, 1)
        slider_row.addWidget(self.btn_plus)

        # Reset virtual line after choosing PD in table
        self._virtual_active = False

        layout.addRow(self.i18n.t("stats_panel.average_lower"), self.avg_lower)
        layout.addRow(self.i18n.t("stats_panel.average_spring"), self.avg_spring)
        layout.addRow(self.i18n.t("stats_panel.average_upper"), self.avg_upper)
        layout.addRow(self.i18n.t("stats_panel.average_total"), self.avg_total)

        layout.addRow("", QLabel(""))  # Spacer

        layout.addRow(self.i18n.t("stats_panel.median_lower"), self.median_lower)
        layout.addRow(self.i18n.t("stats_panel.median_upper"), self.median_upper)

        layout.addRow("", QLabel(""))  # Spacer

        layout.addRow(self.i18n.t("stats_panel.common_config"), self.common)

        layout.addRow("", QLabel(""))  # Spacer

        layout.addRow(self.i18n.t("stats_panel.virtual_lower_label"), self.virtual_label)
        layout.addRow(self.i18n.t("stats_panel.virtual_upper_label"), self.virtual_upper_label)
        layout.addRow("", slider_row)
        
        outer.addLayout(layout)
        outer.addStretch(1)

    def update_stats(self, ctx, model_id, model_name: str):
        if not ctx or not model_id:
            return
        
        stats = ctx.pd_service.get_model_stats(model_id)
        self.reset_virtuals()
        self._virtual_active = False
        self.virtual_slider.blockSignals(True)
        self._configure_virtual_slider_range(model_name)

        slider_value = int(stats.avg_lower * 100)
        self.virtual_slider.setValue(slider_value)

        self.virtual_slider.blockSignals(False)

        self.avg_lower.setText(f"{stats.avg_lower:.2f} mm")
        self.avg_spring.setText(f"{stats.avg_spring:.2f} mm")
        self.avg_upper.setText(f"{stats.avg_upper:.2f} mm")
        self.avg_total.setText(f"{stats.avg_total:.2f} mm")

        self.median_lower.setText(f"{stats.median_lower:.2f} mm")
        self.median_upper.setText(f"{stats.median_upper:.2f} mm")

        if stats.common_config:
            l, s, u = stats.common_config
            self.common.setText(f"{l:.2f} mm + {s:.2f} mm + {u:.2f} mm")
            print(f"DEBUG: Common config: {l}, {s}, {u}")
        else:
            self.common.setText("--")

        self._avg_total = stats.avg_total
        self._avg_spring = stats.avg_spring
        self._avg_lower = stats.avg_lower

    def _on_virtual_changed(self, value: int):
        if not self.isVisible():
            return
        mm = value / 100
        self.virtual_label.setText(f"{mm:.2f} mm")
        self._virtual_active = True
        self.virtual_lower_changed.emit(mm)

    def _configure_virtual_slider_range(self, model_name: str):
        """
        Configure the range of the virtual lower slider based on the PD model.
        """
        if model_name[-3:].startswith("40"):
            max_mm = 12.0
        else:
            max_mm = 2.0

        self.virtual_slider.setMaximum(int(max_mm * 100))

    def _step_down(self):
        step = self.virtual_slider.singleStep()
        self.virtual_slider.setValue(
            max(self.virtual_slider.minimum(),
                self.virtual_slider.value() - step)
        )

    def _step_up(self):
        step = self.virtual_slider.singleStep()
        self.virtual_slider.setValue(
            min(self.virtual_slider.maximum(),
                self.virtual_slider.value() + step)
        )

    def set_virtual_upper(self, value: float):
        self.virtual_upper_label.setText(f"{value:.2f} mm")
        self.virtual_upper_label.show()

    def reset_virtuals(self):
        self.virtual_upper_label.setText("--")
        self.virtual_label.setText("--")