#!/usr/bin/env python
# License: GPL v3 Copyright: 2026, Mateusz Jamróz
# pd/ui/main_window.py

import sqlite3

from PyQt6.QtWidgets import (
    QMainWindow, 
    QMessageBox, 
    QVBoxLayout, 
    QWidget, 
    QDialog,
    QSplitter
)
from PyQt6.QtGui import QAction
from PyQt6.QtCore import QEvent, Qt

from pd.app_context import AppContext
from pd.core.config import load_config, save_config
from pd.ui.widgets.settings import SettingsDialog
from pd.ui.dialogs.add_new import AddNewDialog
from pd.ui.dialogs.add_model import AddModelDialog
from pd.ui.dialogs.del_unit import DelModelDialog
from pd.ui.dialogs.about import AboutDialog
from pd.ui.dialogs.help import HelpDialog
from pd.ui.views.charts_area import ChartsArea
from pd.ui.views.pd_table import PDTable

# I just wanna SLEEEEEP, I just wanna DIEEEEEEEEEEEEEEEEEEEE

class MainWindow(QMainWindow):
    def __init__(self, ctx: AppContext):
        super().__init__()

        self.ctx = ctx
        self.paths = ctx.paths
        self.i18n = ctx.i18n
        self.resources = ctx.resources
        self.pd_service = ctx.pd_service

        self.setWindowTitle("PD UI Manager")
        self.setWindowIcon(ctx.resources.icon("logo"))
        
        self.restore_settings()

        main_widget = QWidget()
        layout = QVBoxLayout(main_widget)
        
        self.statusBar().showMessage(self.ctx.i18n.t("app.label"))

        # Menu Bar
        menu_bar = self.menuBar()
        file_menu = menu_bar.addMenu(self.i18n.t("menu.file"))
        file_menu.setToolTipsVisible(True)
        edit_menu = menu_bar.addMenu(self.i18n.t("menu.edit"))
        edit_menu.setToolTipsVisible(True)
        help_menu = menu_bar.addMenu(self.i18n.t("menu.help"))
        help_menu.setToolTipsVisible(True)


        # FILE MENU
        # Settings
        stgs_action = QAction(self.i18n.t("menu.settings"), self)
        stgs_action.triggered.connect(lambda: SettingsDialog(self.ctx).exec())
        file_menu.addAction(stgs_action)

        exit_action = QAction(self.i18n.t("menu.exit"), self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        # EDIT MENU
        # Add new
        add_action = QAction(self.i18n.t("menu.add_new"), self)
        add_action.setShortcut("Ctrl+N")
        add_action.triggered.connect(self._open_add_dialog)
        edit_menu.addAction(add_action)

        # Add new model of pump unit
        # if it's not in the pump unit models list yet
        new_model = QAction(self.i18n.t("menu.add_model"), self)
        new_model.triggered.connect(lambda: AddModelDialog(self.ctx).exec())
        edit_menu.addAction(new_model)

        # Delete unique pump unit, not the fabric model like 0414720215
        del_unit = QAction(self.i18n.t("menu.delete_unit"), self)
        del_unit.triggered.connect(self._delete_selected_unit)
        edit_menu.addAction(del_unit)

        # HELP MENU
        # Help
        help_action = QAction(self.i18n.t("menu.help"), self)
        help_action.triggered.connect(lambda: HelpDialog(self.ctx).exec())
        help_menu.addAction(help_action)

        # About
        about_action = QAction(self.i18n.t("menu.about"), self)
        about_action.triggered.connect(lambda: AboutDialog(self.ctx).exec())
        help_menu.addAction(about_action)

        #
        ##
        splitter = QSplitter(Qt.Orientation.Horizontal)

        #
        # TABLE AREA
        self.table = PDTable(self.i18n)
        self.table.rowSelected.connect(self._row_selected)
        splitter.addWidget(self.table)

        #
        # CHARTS AREA
        self.charts_area = ChartsArea(self.i18n, self.ctx)

        splitter.addWidget(self.charts_area)

        splitter.setStretchFactor(0, 0)
        splitter.setStretchFactor(1, 1)

        layout.addWidget(splitter)
        self.setCentralWidget(main_widget)
        self.refresh()


    def refresh(self):
        models = self.ctx.pd_service.list_models_with_name()
        
        self.table.set_data(models)

    def closeEvent(self, event: QEvent):
        self.save_settings()
        event.accept()

    def restore_settings(self):
        config = load_config(self.paths.config / "config.ini")
        if "ui" in config and "geometry" in config["ui"]:
            geometry = bytes.fromhex(config["ui"]["geometry"])
            self.restoreGeometry(geometry)
        if "ui" in config and "window_state" in config["ui"]:
            window_state = bytes.fromhex(config["ui"]["window_state"])
            self.restoreState(window_state)

    def save_settings(self):
        config = load_config(self.paths.config / "config.ini")
        config["ui"]["geometry"] = self.saveGeometry().toHex().data().decode()
        config["ui"]["window_state"] = self.saveState().toHex().data().decode()
        save_config(config, self.paths.config / "config.ini")

    def _open_add_dialog(self):
        dlg = AddNewDialog(self.ctx, on_accept_callback=self.refresh)
        if dlg.exec() == QDialog.DialogCode.Accepted:
            self.refresh()

    def get_selected_pd_id(self) -> int | None:
        selected = self.table.selectedItems()
        if not selected:
            return None
        row = selected[0].row()
        pd_id = int(self.table.item(row, 0).text()) # model_id is in hidden column 0
        return pd_id, row
    
    def _row_selected(self, pd_id: int, model: str, model_id: str):
        self.current_pd = pd_id

        count = self.ctx.pd_service.count_model(model_id)
        values = self.ctx.pd_service.washers_distribution(model_id)
        print(f"DEBUG: Selected PD ID: {pd_id}")
        
        if values:
            self.charts_area.update_data(values[0], values[1], model_id)
            
            # Title on top Charts Area
            self.charts_area.set_title(count, model)

    def _delete_selected_unit(self):
        result = self.get_selected_pd_id()
        if result is None:
            QMessageBox.warning(self, self.i18n.t("delete_unit.title"), self.i18n.t("delete_unit.no_selection"))
            return
        pd_id, row = result
        dlg = DelModelDialog(self.ctx, pd_id)
        if dlg.exec() == QDialog.DialogCode.Accepted:
            self.refresh()