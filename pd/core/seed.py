#!/usr/bin/env python
# License: GPL v3 Copyright: 2026, Mateusz Jamróz
# pd/core/seed.py

import sqlite3
import logging
from pd.platform.resources import resource_path

logger = logging.getLogger(__name__)

def seed_pd_models(conn: sqlite3.Connection) -> None:
    """
    Seed the database with initial PD models from a SQL file.
    """
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM pd_models;")
    count = cursor.fetchone()[0]

    if count > 0:
        return
    
    seed_file = resource_path("pd/assets/seed/pd_models.sql")
    with open(seed_file, 'r', encoding='utf-8') as f:
        conn.executescript(f.read())

    logger.info("Seeded PD models into the database.")

def seed_opening_pressures(conn: sqlite3.Connection) -> None:
    """
    Seed the database with initial opening pressures from a SQL file.
    """
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM pd_opening_pressure;")
    count = cursor.fetchone()[0]

    if count > 0:
        return
    
    seed_file = resource_path("pd/assets/seed/opening_pressures.sql")
    with open(seed_file, 'r', encoding='utf-8') as f:
        conn.executescript(f.read())

    logger.info("Seeded opening pressures into the database.")