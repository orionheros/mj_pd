#!/usr/bin/env python
# License: GPL v3 Copyright: 2026, Mateusz Jamróz
# pd/bootstrap.py

import sqlite3
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

def start_app():
    platform = get_platform()
    paths = init_paths(platform)
    config = load_config(paths.config / "config.ini")
    i18n = I18n(config["general"]["language"])

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

        run_ui(ctx)
    except Exception as e:
        hse(e, i18n)
