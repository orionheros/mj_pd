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
from pd.core.services import PDService


class ChartsArea(QWidget):
    def __init__(self, i18n, ctx: PDService, parent=None):
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
        self.stats.virtual_lower_changed.connect(self._on_virtual_lower_changed)

        content.addWidget(self.charts, 3)
        content.addWidget(self.stats, 1)

        layout.addWidget(self.title)
        layout.addLayout(content)

    def update_data(self, lower, upper, model_id):
        model_name = self.ctx.pd_service.get_model_name(model_id)
        self.stats._virtual_active = False
        self.charts.lower_virtual_line.hide()
        self.charts.upper_virtual_line.hide()
        self.charts.update_data(lower, upper, model_name)
        self.charts.set_chart_title()
        self.charts.force_y_range(self.charts.plot_lower, lower)
        self.charts.force_y_range(self.charts.plot_upper, upper)
        self.stats.update_stats(self.ctx, model_id, model_name)

    def set_title(self, n: int, model_id: str):
        # Title for Charts Area
        text = self.i18n.plural(
            "charts.title_area",
            n,
            model_id=model_id
        )
        self.title.setText(text)

    def _on_virtual_lower_changed(self, virtual_lower: float):
        if not self.stats._virtual_active:
            return
        
        avg_total = self.stats._avg_total
        avg_spring = self.stats._avg_spring
        virtual_upper = round(avg_total - avg_spring - virtual_lower, 2)
        self.stats.set_virtual_upper(virtual_upper)

        self.charts.lower_virtual_line.setValue(virtual_lower)
        self.charts.lower_virtual_line.show()
        self.charts.ensure_y_visible(self.charts.plot_lower, virtual_lower)

        self.charts.upper_virtual_line.setValue(virtual_upper)
        self.charts.upper_virtual_line.show()
        self.charts.ensure_y_visible(self.charts.plot_upper, virtual_upper)        