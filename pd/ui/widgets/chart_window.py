#!/usr/bin/env python
# License: GPL v3 Copyright: 2026, Mateusz Jamróz
# pd/ui/widgets/chart_window.py

import pyqtgraph as pg

from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout
)
from pd.ui.utils.tooltip import on_point_hovered

class ChartWindow(QWidget):
    def __init__(self, source_scatter, source_mean_line, title, i18n, parent=None):
        super().__init__(parent)
        self.i18n = i18n
        self.setWindowTitle(self.i18n.t("charts.chart_window_title"))
        self.resize(800, 600)

        layout = QVBoxLayout(self)
        self.plot = pg.PlotWidget()
        layout.addWidget(self.plot)

        x, y = source_scatter.getData()
        scatter = pg.ScatterPlotItem(
            x=x, y=y,
            pen=source_scatter.opts['pen'],
            brush=source_scatter.opts['brush'],
            size=source_scatter.opts['size'],
            symbol=source_scatter.opts['symbol'],
            name=source_scatter.opts['name'],
            hoverable=source_scatter.opts['hoverable'],
            tip=source_scatter.opts['tip']
        )
        self.plot.addItem(scatter)

        if source_mean_line.isVisible():
            mean_line = pg.InfiniteLine(
                angle=source_mean_line.angle,
                pen=source_mean_line.pen,
                movable=False
            )
            mean_line.setValue(source_mean_line.value())
            self.plot.addItem(mean_line)

        self.plot.setLabel("left", self.i18n.t("charts.podkladla_thickness_y"))
        self.plot.setLabel("bottom", self.i18n.t("charts.podkladla_count_x"))
        self.plot.setTitle(title)
        self.plot.showGrid(x=True, y=True)
        self.plot.getAxis('bottom').setTickSpacing(major=1, minor=1)
        self.plot.getAxis('left').setTickSpacing(major=0.01, minor=0.01)
        self.plot.setBackground('w')
        scatter.sigHovered.connect(lambda item, points, ev: on_point_hovered(self.i18n, points, self.plot))