#!/usr/bin/env python
# License: GPL v3 Copyright: 2026, Mateusz Jamróz
# pd/core/database.py

import sqlite3
import logging
from pathlib import Path
from pd.platform.resources import resource_path
from pd.core.seed import seed_pd_models, seed_opening_pressures

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
