#!/usr/bin/env python
# License: GPL v3 Copyright: 2026, Mateusz Jamróz
# pd/ui/dialogs/about.py

from PyQt6.QtWidgets import (
    QDialog, 
    QVBoxLayout,
    QLabel, 
    QPushButton
)

from pd import (__version__, 
                __author__, 
                __license__,
                __app_name__)
from pd.app_context import AppContext
from pd.startup.updates import UpdateWorker

class AboutDialog(QDialog):
    def __init__(self, ctx: AppContext):
        super().__init__()
        self.setWindowTitle(ctx.i18n.t("about.title"))
        self.ctx = ctx
        self._build_ui()
        self.setMinimumSize(300, 200)

    def _build_ui(self):
        layout = QVBoxLayout(self)

        app_name = QLabel(f"<h2>{self._get_app_name()}</h2>")
        version = QLabel(f"{self.ctx.i18n.t('about.version')}: {self._app_version()}")
        author = QLabel(f"{self.ctx.i18n.t('about.author')}: {self._get_author()}")
        license_info = QLabel(f"{self.ctx.i18n.t('about.license')}: {self._get_license()}")

        layout.addWidget(app_name)
        layout.addWidget(version)
        layout.addWidget(author)
        layout.addWidget(license_info)

        btn_close = QPushButton(self.ctx.i18n.t("buttons.close"))
        btn_close.clicked.connect(self.accept)

        check_upd = QPushButton(self.ctx.i18n.t("help.check_updates"))
        check_upd.clicked.connect(self._check_updates)

        layout.addWidget(check_upd)
        layout.addWidget(btn_close)

    def _get_app_name(self):
        return __app_name__
    
    def _get_author(self):
        return __author__
    
    def _app_version(self):
        return __version__
    
    def _get_license(self):
        return __license__

    def _check_updates(self):
        worker = UpdateWorker()
        worker.finished.connect(self._on_update_check_finished)
        worker.run()

    def _on_update_check_finished(self, is_update_available, latest_version, release_url):
        if is_update_available:
            print(f"Update available: {latest_version}. Check {release_url}")
        else:
            print("No updates available.")