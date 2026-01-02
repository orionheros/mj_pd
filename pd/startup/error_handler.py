#!/usr/bin/env python
# License: GPL v3 Copyright: 2026, Mateusz Jamróz
# pd/startup/error_handler.py

import sys
import traceback

from pd.core.i18n import I18n
from PyQt6.QtWidgets import QApplication, QMessageBox

def handle_startup_error(exception: Exception, i18n: I18n | None = None) -> None:
    """ Handle errors that occur during startup """

    try:
        if QApplication.instance() and i18n:
            QMessageBox.critical(
                None,
                i18n.t("app.title"),
                i18n.t("error.startup_failed").format(str(exception))
            )
        else:
            raise RuntimeError
    
    except Exception:
        print("A fatal error occurred during startup:", file=sys.stderr)
        print(str(exception), file=sys.stderr)
        traceback.print_exc(file=sys.stderr)

    sys.exit(1)