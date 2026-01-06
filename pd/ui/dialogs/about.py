#!/usr/bin/env python
# License: GPL v3 Copyright: 2026, Mateusz Jamróz
# pd/ui/dialogs/about.py

from PyQt6.QtWidgets import (
    QDialog, 
    QVBoxLayout,
    QLabel, 
    QPushButton,
    QMessageBox
)

from pd import (__version__, 
                __author__, 
                __license__,
                __app_name__)
from pd.app_context import AppContext
from pd.platform.os_detect import get_platform
from pd.startup.updates import check_update, download_update
from pathlib import Path

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

        check_upd = QPushButton(self.ctx.i18n.t("update.check_updates"))
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
        try:
            info = check_update(
                current_version=__version__, 
                platform=get_platform()
            )
        except Exception as e:
            QMessageBox.warning(self, self.ctx.i18n.t("update.update_error"), str(e))
            return
        
        if not info or not isinstance(info, dict):
            QMessageBox.information(
                self, 
                self.ctx.i18n.t("update.no_update_title"), 
                self.ctx.i18n.t("update.no_update_message")
            )
            return
        
        text_a = self.ctx.i18n.t("update.change_text")
        text_b = self.ctx.i18n.t("update.want_update")
        msg = (
            f"{self.ctx.i18n.t('update.update_available')} {info['version']}\n\n"
            f"{text_a}:\n{info['changelog']}\n\n"
            f"{text_b}"
        )

        if QMessageBox.question(
            self,
            self.ctx.i18n.t("update.update_available_title"),
            msg,
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        ) == QMessageBox.StandardButton.Yes:
            
            try:
                dest_dir = Path.home() / "Downloads"

                downloaded_file = download_update(info, dest_dir)

                QMessageBox.information(
                    self,
                    self.ctx.i18n.t("update.download_complete_title"),
                    f"{self.ctx.i18n.t('update.download_complete_message')}:\n{downloaded_file}"
                )
            except Exception as e:
                QMessageBox.warning(self, self.ctx.i18n.t("update.download_error"), str(e))