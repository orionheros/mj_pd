#!/usr/bin/env python
# License: GPL v3 Copyright: 2026, Mateusz Jamróz
# pd/bootstrap.py

import sqlite3
import sys
from PyQt6.QtWidgets import QApplication, QDialog
from pd.platform.os_detect import get_platform
from pd.platform.paths import init_paths
from pd.startup.logging import init_logging
from pd.core.database import init_database
from pd.core.config import load_config
from pd.core.i18n import I18n
from pd.ui.app import run_ui
from pd.startup.error_handler import handle_startup_error as hse
from pd.app_context import AppContext
from pd.core.repositories import PDRepository
from pd.core.services import PDService
from pd.platform.resources import ResourceManager
from pd.launcher.launcher import Launcher

def start_app():
    platform = get_platform()
    paths = init_paths(platform)
    config = load_config(paths.config / "config.ini")

    app = QApplication(sys.argv)

    selected_lang = config["general"]["language"]
    selected_module = config["launcher"].get("saved_data_package", "")   

    if config.getboolean("launcher", "show_on_startup", fallback=True):
        launcher = Launcher(config, paths)

        if launcher.exec() == QDialog.DialogCode.Accepted:
            selected_lang, selected_module, set_default = launcher.get_results()

            config["general"]["language"] = selected_lang
            config["launcher"]["saved_data_package"] = selected_module

            if set_default:
                config["launcher"]["show_on_startup"] = "false"

            with open(paths.config / "config.ini", 'w', encoding='utf-8') as f:
                config.write(f)
                
            del launcher
        else:
            return

    i18n = I18n(selected_lang)

    if selected_module == "pd":
        try:
            init_logging(paths.logs)

            db_path = paths.data / "pd.db"
            init_database(db_path)

            conn = sqlite3.connect(db_path)
            conn.execute("PRAGMA foreign_keys = ON;")

            pd_repo = PDRepository(conn)
            pd_service = PDService(pd_repo)
            resources = ResourceManager()

            ctx = AppContext(
                conn=conn,
                paths=paths,
                pd_service=pd_service,
                config=config,
                i18n=i18n,
                resources=resources
            )

            run_ui(ctx, app)

            del ctx
            conn.close()
        except Exception as e:
            hse(e, i18n)

    else:
        print(f"Unknown module selected: {selected_module}")
