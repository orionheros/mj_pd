#!/usr/bin/env python3
# License: GPL v3 Copyright: 2026, Mateusz Jamróz
# pd/app_context.py

from dataclasses import dataclass
import sqlite3

from pd.platform.paths import AppPaths
from pd.platform.resources import ResourceManager
from pd.core.services import PDService
from pd.core.i18n import I18n

@dataclass
class AppContext:
    conn: sqlite3.Connection
    paths: AppPaths
    pd_service: PDService
    config: dict
    i18n: I18n
    resources: ResourceManager