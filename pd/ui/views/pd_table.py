#!/usr/bin/env python
# License: GPL v3 Copyright: 2026, Mateusz Jamróz
# pd/ui/views/pd_table.py

from PyQt6.QtWidgets import (
    QWidget,
    QAbstractItemView,
    QVBoxLayout,
    QTableWidget,
    QTableWidgetItem,
    QLineEdit
)
from PyQt6.QtCore import pyqtSignal

class PDTable(QWidget):
    rowSelected = pyqtSignal(int, str, str)
    # pd_id, model, model_id

    def __init__(self, i18n, parent=None):
        super().__init__(parent)
        self.i18n = i18n
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Search Label
        self.search = QLineEdit()
        self.search.setPlaceholderText(self.i18n.t("table.search"))
        self.search.textChanged.connect(self._search_label)

        # Table
        self.table = QTableWidget()
        self._setup(self.table)
        self.table.setStyleSheet("""
        QTableWidget:item:selected {
            color: lightblue;
        }
        """)

        layout.addWidget(self.search)
        layout.addSpacing(4)
        layout.addWidget(self.table)

    def _search_label(self, text: str):
        text = text.strip().lower()

        for row in range(self.table.rowCount()):
            pu = self.table.item(row, 2)  # model_name column
            if not pu:
                self.table.setRowHidden(row, True)
                continue

            model = pu.text().lower()
            self.table.setRowHidden(row, text not in model)
        
    def _setup(self, table: QTableWidget):
        table.setColumnCount(8)
        table.setHorizontalHeaderLabels([
            self.i18n.t("table.pd_id"),
            self.i18n.t("table.model_id"),
            self.i18n.t("table.model_name"),
            self.i18n.t("table.opening_pressure"),
            self.i18n.t("table.washer1"),
            self.i18n.t("table.washer2"),
            self.i18n.t("table.spring_length"),
            self.i18n.t("table.final_pressure"),
        ])
        table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        table.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        table.itemSelectionChanged.connect(self._emit_selected)
        table.setColumnHidden(0, True)  # Hide pd_id column
        table.setColumnHidden(1, True)  # Hide model_id column
        table.setSortingEnabled(True)

    def _emit_selected(self):
        items = self.table.selectedItems()
        if not items:
            return
        row = items[0].row()

        pd_id = int(self.table.item(row, 0).text())
        model_name = self.table.item(row, 2).text()
        model_id = self.table.item(row, 1).text()

        self.rowSelected.emit(pd_id, model_name, model_id)

    def set_data(self, models: list):
        self.table.setRowCount(len(models))

        for row, model in enumerate(models):
            self.table.setItem(row, 0, QTableWidgetItem(str(model.id)))  # hidden pd_id
            self.table.setItem(row, 1, QTableWidgetItem(str(model.model_id)))  # hidden model_id
            self.table.setItem(row, 2, QTableWidgetItem(str(model.model_name)))
            self.table.setItem(row, 3, QTableWidgetItem(str(model.opening_pressure)))
            self.table.setItem(row, 4, QTableWidgetItem(f"{model.washer1:.2f}"))
            self.table.setItem(row, 5, QTableWidgetItem(f"{model.washer2:.2f}"))
            self.table.setItem(row, 6, QTableWidgetItem(f"{model.spring_length:.2f}")) 
            self.table.setItem(row, 7, QTableWidgetItem(str(int(model.final_pressure))))

        self.table.resizeColumnsToContents()
        self.table.resizeRowsToContents()