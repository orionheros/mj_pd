#!/usr/bin/env python
# License: GPL v3 Copyright: 2026, Mateusz Jamróz
# pd/ui/utils/tooltip.py

from PyQt6.QtWidgets import QToolTip
from PyQt6.QtGui import QCursor
from PyQt6.QtCore import QRect

def on_point_hovered(i18n, points, plot_widget):
    if points is None or len(points) == 0:
        return
    p = points[0]
    pos = p.pos()
    x = pos.x()
    y = pos.y()
    label_x = i18n.t("charts.tool_tip_x")
    label_y = i18n.t("charts.tool_tip_y")
    text = f"{label_x}{int(x)}\n{label_y}{y:.2f}"
    QToolTip.showText(
        QCursor.pos(),
        text,
        plot_widget,
        QRect(),
        3000
    )