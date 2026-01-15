#!/usr/bin/env python
# License: GPL v3 Copyright: 2026, Mateusz Jamróz
# pd/core/database.py

import sys
import sqlite3
import logging
from pathlib import Path
from pd.platform.resources import resource_path
from pd.core.seed import seed_pd_models, seed_opening_pressures
from PyQt6.QtWidgets import QMessageBox
from pd.startup.updates import GITHUB_API, download_crit_update
from pd import __app_name__

logger = logging.getLogger(__name__)

def init_database(db_path: Path) -> None:
    """
    Initialize the SQLite database.
    If the database file does not exist, it creates a new one from pd.sql.
    """
    try:
        if db_path.exists():
            logger.info("Database already exists at %s", db_path)
            return
        
        logger.info("Database not found, initializing from schema.")
        
        schema_path = resource_path("pd/assets/pd.sql")
        if not schema_path.exists():
            raise RuntimeError(f"Database schema file not found at {schema_path}")
        
        with sqlite3.connect(db_path) as conn:
            with open(schema_path, 'r', encoding='utf-8') as f:
                conn.executescript(f.read())
                seed_pd_models(conn)
                seed_opening_pressures(conn)

        logger.info("Database initialized successfully.")
    except Exception as e:
        logger.error("Failed to initialize database: %s", e)
        raise

def get_db_version(db_path: str) -> int:
    try:
        with sqlite3.connect(db_path) as conn:
            row = conn.execute("PRAGMA user_version").fetchone()
            print(f"DEBUG: PRAGMA user_version row: {row}")
            return row[0] if row else 0
    except sqlite3.Error as e:
        raise RuntimeError(f"Cannot read database version: {e}")
    
def assert_db_version(db_path: Path, db_version: int, i18n, app) -> None:
    """
    Checks if the database version matches the expected version.
    If not, shows an error message and raises an exception.
    We don't want to proceed with incompatible, newer database versions.
    """
    pragma = get_db_version(db_path)
    print(f"DEBUG: Database PRAGMA version: {pragma}, Expected version: {db_version}")

    if pragma > db_version:
        box = QMessageBox()
        box.setIcon(QMessageBox.Icon.Critical)
        box.setWindowTitle(i18n.t("errors.startup_failed"))
        box.setText(i18n.t("errors.db_incompatible").format(
            version=pragma,
            app_version=db_version))
        
        if GITHUB_API:
            box.setInformativeText(
                i18n.t("errors.update_prompt")
            )
            box.setStandardButtons(
                QMessageBox.StandardButton.Yes | 
                QMessageBox.StandardButton.No
            )
            box.setDefaultButton(QMessageBox.StandardButton.Yes)
        else:
            box.setStandardButtons(QMessageBox.StandardButton.Ok)

        result = box.exec()

        if GITHUB_API and result == QMessageBox.StandardButton.Yes:
            try:
                download_crit_update()
                QMessageBox.information(
                    None,
                    i18n.t("update.download_complete_title"),
                    i18n.t(f"update.download_complete_message")
                )
            except Exception as e:
                QMessageBox.warning(
                    None,
                    i18n.t("update.download_error"),
                    str(e)
                )
                sys.exit()
        sys.exit(app.exec())