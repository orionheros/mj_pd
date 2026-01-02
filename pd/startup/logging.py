#!/usr/bin/env python
# License: GPL v3 Copyright: 2026, Mateusz Jamróz
# pd/startup/logging.py

import logging
from pathlib import Path

def init_logging(lod_dir: Path) -> None:
    """
    Initialize logging configuration.
    Logs will be stored in the specified log directory.
    """
    lod_dir.mkdir(parents=True, exist_ok=True)
    log_file = lod_dir / "pd.log"

    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file, encoding='utf-8'),
            logging.StreamHandler()
        ]
    )

    logging.getLogger(__name__).info("Logging initialized. Log file at: %s", log_file)