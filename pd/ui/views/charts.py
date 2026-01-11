#!/usr/bin/env python
# License: GPL v3 Copyright: 2026, Mateusz Jamróz
# pd/ui/views/charts.py

import pyqtgraph as pg

from PyQt6.QtWidgets import (
    QWidget, 
    QVBoxLayout,
    QToolTip
)
from PyQt6.QtGui import QCursor

from collections import Counter

from pd.ui.widgets.chart_window import ChartWindow
from pd.ui.utils.tooltip import on_point_hovered

# Y - two decimal places
class FormattedAxis(pg.AxisItem):
    def tickStrings(self, values, scale, spacing):
        return [f"{v:.2f}" for v in values]

# X - integers only
class IntAxis(pg.AxisItem):
    def tickStrings(self, values, scale, spacing):
        return [str(int(round(v))) for v in values]

class WashersChart(QWidget):


    def set_chart_title(self):
        # Set titles for both charts
        title_upper = self.i18n.t("charts.chart1_title") + " " + self.i18n.t("charts.chart1_title_upper")
        title_lower = self.i18n.t("charts.chart1_title") + " " + self.i18n.t("charts.chart1_title_lower")
        self.upper_chart_title = f"{title_upper}"
        self.lower_chart_title = f"{title_lower}"
        self.plot_upper.setTitle(f"<div style='font-weight:bold'>{title_upper}</div>")
        self.plot_lower.setTitle(f"<div style='font-weight:bold'>{title_lower}</div>")
        

    def __init__(self, i18n, parent=None):
        super().__init__(parent)

        self.i18n = i18n

        layout = QVBoxLayout(self)

        # --- Chart for upper spring plate ---
        self.plot_upper = pg.PlotWidget(axisItems={
            'left': FormattedAxis('left'),
            'bottom': IntAxis('bottom'),
        })
        self.plot_upper.showGrid(x=True, y=True)
        self.plot_upper.getAxis('bottom').setTickSpacing(major=1, minor=1)
        self.plot_upper.getAxis('bottom').setStyle(tickFont=pg.QtGui.QFont("Arial", 10, weight=pg.QtGui.QFont.Weight.Bold))
        self.plot_upper.getAxis('left').setTickSpacing(major=0.01, minor=0.01)
        self.plot_upper.getAxis('left').setStyle(tickFont=pg.QtGui.QFont("Arial", 10, weight=pg.QtGui.QFont.Weight.Bold))
        label_bottom = self.i18n.t("charts.podkladla_count_x")
        label_left = self.i18n.t("charts.podkladla_thickness_y")
        self.plot_upper.setLabel("left", label_left)
        self.plot_upper.setLabel("bottom", label_bottom)
        self.plot_upper.setBackground('w')
        self.plot_upper.scene().sigMouseClicked.connect(self._open_uchart_window)
        layout.addWidget(self.plot_upper)

        # --- Chart for lower spring plate ---
        self.plot_lower = pg.PlotWidget(axisItems={
            'left': FormattedAxis('left'),
            'bottom': IntAxis('bottom'),
        })
        self.plot_lower.showGrid(x=True, y=True)
        self.plot_lower.getAxis('bottom').setTickSpacing(major=1, minor=1)
        self.plot_lower.getAxis('bottom').setStyle(tickFont=pg.QtGui.QFont("Arial", 10, weight=pg.QtGui.QFont.Weight.Bold))
        self.plot_lower.getAxis('left').setTickSpacing(major=0.01, minor=0.01)
        self.plot_lower.getAxis('left').setStyle(tickFont=pg.QtGui.QFont("Arial", 10, weight=pg.QtGui.QFont.Weight.Bold))
        self.plot_lower.setLabel("left", label_left)
        self.plot_lower.setLabel("bottom", label_bottom)
        self.plot_lower.setBackground('w')
        self.plot_lower.scene().sigMouseClicked.connect(self._open_lchart_window)
        layout.addWidget(self.plot_lower)

        # --- Scatter---
        self.upper_scatter = pg.ScatterPlotItem(
            pen=None,
            brush=pg.mkBrush(0, 0, 200),    # blue
            size=8,
            symbol='o',
            name="Upper Washer",
            hoverable=True,
            tip=None
        )
        self.upper_mean_line = pg.InfiniteLine(
            angle=0,
            pen=pg.mkPen('blue', width=2, style=pg.QtCore.Qt.PenStyle.DashLine),
        )
        self.upper_scatter.sigHovered.connect(lambda item, points, ev: on_point_hovered(self.i18n, points, self.plot_upper))
        self.plot_upper.addItem(self.upper_mean_line)
        self.plot_upper.addItem(self.upper_scatter)
        self.upper_mean_line.hide()
        self.plot_upper.addLegend()

        self.lower_scatter = pg.ScatterPlotItem(
            pen=None,
            brush=pg.mkBrush(0, 200, 0),    # green
            size=8,
            symbol='o',
            name="Lower Washer",
            hoverable=True,
            tip=None
        )
        self.lower_mean_line = pg.InfiniteLine(
            angle=0,
            pen=pg.mkPen('green', width=2, style=pg.QtCore.Qt.PenStyle.DashLine),
        )
        self.lower_scatter.sigHovered.connect(lambda item, points, ev: on_point_hovered(self.i18n, points, self.plot_lower))
        self.plot_lower.addItem(self.lower_mean_line)
        self.plot_lower.addItem(self.lower_scatter)
        self.lower_mean_line.hide()
        self.plot_lower.addLegend()

        self.lower_virtual_line = pg.InfiniteLine(
            angle=0,
            pen=pg.mkPen('orange', width=3, style=pg.QtCore.Qt.PenStyle.DotLine),
        )
        self.upper_virtual_line = pg.InfiniteLine(
            angle=0,
            pen=pg.mkPen('orange', width=3, style=pg.QtCore.Qt.PenStyle.DotLine),
        )

        self.plot_lower.addItem(self.lower_virtual_line)
        self.plot_upper.addItem(self.upper_virtual_line)

        self.lower_virtual_line.hide()
        self.upper_virtual_line.hide()

    def update_data(
            self,
            lower_washers: list[float],
            upper_washers: list[float],
            model_name: str
        ):
        self.model_name = model_name
        # Lower spring plate
        lower_count = Counter(lower_washers)
        x_lower = list(lower_count.values())
        y_lower = list(lower_count.keys())
        self.lower_scatter.setData(x=x_lower, y=y_lower)
        if lower_washers:
            lower_mean = round(sum(lower_washers) / len(lower_washers), 2)
            self.lower_mean_line.setValue(lower_mean)
            self.lower_mean_line.show()
        else:
            self.lower_mean_line.hide()
        self.plot_lower.enableAutoRange()

        # Upper spring plate
        upper_count = Counter(upper_washers)
        x_upper = list(upper_count.values())
        y_upper = list(upper_count.keys())
        self.upper_scatter.setData(x=x_upper, y=y_upper)
        if upper_washers:
            upper_mean = round(sum(upper_washers) / len(upper_washers), 2)
            self.upper_mean_line.setValue(upper_mean)
            self.upper_mean_line.show()
        else:
            self.upper_mean_line.hide()
        self.plot_upper.enableAutoRange()

        self.upper_washers_count = len(upper_washers)
        self.lower_washers_count = len(lower_washers)

    # New method to force y-axis range
    # autoRange() was buggy in some cases
    def force_y_range(self, plot, values: list[float], padding: float = 0.05):
        if not values:
            return
        
        vmin = min(values)
        vmax = max(values)

        if vmin == vmax:
            vmin -= padding
            vmax += padding
        else:
            span = vmax - vmin
            vmin -= span * padding
            vmax += span * padding

        plot.setYRange(vmin, vmax, padding=0)

    # New method to handle virtual_line
    # virtual_line without that method was not change y-axis range in charts 
    def ensure_y_visible(self, plot, value: float, padding: float = 0.05):
        view = plot.getViewBox()
        (ymin, ymax) = view.viewRange()[1]

        if ymin <= value <= ymax:
            return  # Already visible
        
        span = ymax - ymin
        if span <= 0:
            span = abs(value) if value != 0 else 1.0

        if value < ymin:
            ymin = value - span * padding
        elif value > ymax:
            ymax = value + span * padding

        plot.setYRange(ymin, ymax, padding=0)

    def _on_point_hovered(self, item, points, ev, plot_widget):
        if points is None or len(points) == 0:
            return
        p = points[0]
        pos = p.pos()
        x = pos.x()
        y = pos.y()
        label_x = self.i18n.t("charts.tool_tip_x")
        label_y = self.i18n.t("charts.tool_tip_y")
        text = f"{label_x}{int(x)}\n{label_y}{y:.2f}"
        QToolTip.showText(
            QCursor.pos(),
            text,
            plot_widget
        )

    def _open_uchart_window(self, event):
        n = getattr(self, 'upper_washers_count', 0)
        model_name = getattr(self, 'model_name', '')
        model_id = getattr(self, 'model_id', '')
        self.uchart_win = ChartWindow(
            self.upper_scatter, 
            self.upper_mean_line, 
            self.upper_chart_title, 
            self.i18n,
            n,
            model_name=model_name,
            model_id=model_id)
        self.uchart_win.show()

    def _open_lchart_window(self, event):
        n = getattr(self, 'lower_washers_count', 0)
        model_name = getattr(self, 'model_name', '')
        model_id = getattr(self, 'model_id', '')
        self.lchart_win = ChartWindow(
            self.lower_scatter, 
            self.lower_mean_line, 
            self.lower_chart_title, 
            self.i18n,
            n,
            model_name=model_name,
            model_id=model_id)
        self.lchart_win.show()