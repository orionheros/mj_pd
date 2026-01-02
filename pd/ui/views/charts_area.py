#!/usr/bin/env python
# License: GPL v3 Copyright: 2026, Mateusz Jamróz
# pd/ui/views/charts_area.py

from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel
)
from PyQt6.QtCore import Qt

from pd.ui.views.charts import WashersChart
from pd.ui.views.stats_panel import StatsPanel


class ChartsArea(QWidget):
    def __init__(self, i18n, ctx=None, parent=None):
        super().__init__(parent)
        self.i18n = i18n
        self.ctx = ctx

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(6)

        # Title
        self.title = QLabel("")
        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title.setStyleSheet("font-weight: bold; font-size: 16px;")

        content = QHBoxLayout()

        # Charts
        self.charts = WashersChart(self.i18n)
        self.stats = StatsPanel(ctx)

        content.addWidget(self.charts, 3)
        content.addWidget(self.stats, 1)

        layout.addWidget(self.title)
        layout.addLayout(content)

    def update_data(self, lower, upper, model_id):
        self.charts.update_data(lower, upper)
        self.charts.set_chart_title()

        self.stats.update_stats(self.ctx, model_id)

    def set_title(self, n: int, model_id: str):
        # Title for Charts Area
        text = self.i18n.plural(
            "charts.title_area",
            n,
            model_id=model_id
        )
        self.title.setText(text)
        