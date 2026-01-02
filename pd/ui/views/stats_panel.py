#!/usr/bin/env python
# License: GPL v3 Copyright: 2026, Mateusz Jamróz
# pd/ui/views/stats_panel.py

from PyQt6.QtWidgets import (
    QWidget,
    QFormLayout,
    QLabel,
    QVBoxLayout
)
from PyQt6.QtCore import Qt

class StatsPanel(QWidget):
    def __init__(self, ctx, parent=None):
        super().__init__(parent)
        self.ctx = ctx

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

        layout.addRow("Average Lower:", self.avg_lower)
        layout.addRow("Average Spring:", self.avg_spring)
        layout.addRow("Average Upper:", self.avg_upper)
        layout.addRow("Average Total:", self.avg_total)

        layout.addRow("", QLabel(""))  # Spacer

        layout.addRow("Median Lower:", self.median_lower)
        layout.addRow("Median Upper:", self.median_upper)

        layout.addRow("", QLabel(""))  # Spacer

        layout.addRow("Common Config:", self.common)

        outer.addLayout(layout)
        outer.addStretch(1)

    def update_stats(self, ctx, model_id):
        if not ctx or not model_id:
            return
        print("DEBUG: Updating stats panel")
        stats = ctx.pd_service.get_model_stats(model_id)

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