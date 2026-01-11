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
from PyQt6.QtCore import Qt

from pd import (__version__, 
                __author__, 
                __license__,
                __app_name__)
from pd.app_context import AppContext
from pd.platform.os_detect import get_platform
from pd.startup.updates import check_update
from pd.ui.dialogs.download.choose_dir import choose_download_dir
from pd.ui.dialogs.download.download_dialog import DownloadDialog

class AboutDialog(QDialog):
    def __init__(self, ctx: AppContext):
        super().__init__()
        self.setWindowTitle(ctx.i18n.t("about.title"))
        self.ctx = ctx
        self._build_ui()
        self.setMinimumSize(300, 200)
        t = self.ctx.i18n.t

    def _build_ui(self):
        layout = QVBoxLayout(self)

        info_layout = QVBoxLayout()
        info_layout.setSpacing(0)
        info_layout.setContentsMargins(0, 0, 0, 0)
        app_name = QLabel(f"<h2>{self._get_app_name()}</h2>")
        version = QLabel(f"{self.ctx.i18n.t('about.version')}: {self._app_version()}")
        author = QLabel(f"{self.ctx.i18n.t('about.author')}: {self._get_author()}")
        license_info = self._get_license()

        info_layout.addWidget(app_name)
        info_layout.addWidget(version)
        info_layout.addSpacing(10)
        info_layout.addWidget(author)
        info_layout.addWidget(self._get_contact())
        info_layout.addSpacing(10)
        info_layout.addWidget(QLabel(self.ctx.i18n.t("about.github") + ":"))
        info_layout.addWidget(self._github())
        info_layout.addSpacing(10)
        info_layout.addWidget(license_info)
        layout.addLayout(info_layout)
        layout.addStretch()

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
        gpl = "https://www.gnu.org/licenses/gpl-3.0.en.html"
        license_text = f"{self.ctx.i18n.t('about.license')}: <a href=\"{gpl}\" style=\"text-decoration:none; color: #0078d4;\">{__license__}</a>"
        license_info = QLabel(license_text)
        license_info.setOpenExternalLinks(True)
        license_info.setCursor(Qt.CursorShape.PointingHandCursor)
        return license_info
    
    def _get_contact(self):
        email = "orionhero@protonmail.com"
        contact_text = f'{self.ctx.i18n.t("about.contact")}: <a href="mailto:{email}" style="text-decoration:none; color: #0078d4;">{email}</a>'
        contact_label = QLabel(contact_text)
        contact_label.setOpenExternalLinks(True)
        contact_label.setCursor(Qt.CursorShape.PointingHandCursor)
        return contact_label
        

    def _github(self):
        github_url = "https://github.com/orionheros/mj_pd"
        git_text = f'<a href="{github_url}" style="text-decoration:none; color: #0078d4;">{github_url}</a>'
        git_label = QLabel(git_text)
        git_label.setOpenExternalLinks(True)
        git_label.setCursor(Qt.CursorShape.PointingHandCursor)
        return git_label

    def _check_updates(self):
        try:
            info = check_update(
                current_version=__version__, 
                platform=get_platform(),
                allow_prerelease=True # dev for testing: True
            )
        except Exception as e:
            msg = str(e).lower()
            if '404' in msg or 'not found' in msg or 'repo_not_found' in msg:
                QMessageBox.information(
                    self, 
                    self.ctx.i18n.t("update.no_update_title"), 
                    self.ctx.i18n.t("update.repo_not_found")
                )
                return
            else:
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
        changelog = info.get("changes", "")
        msg = (
            f"{self.ctx.i18n.t('update.update_available')} {info['version']}\n\n"
            f"{text_a}:\n{changelog}\n\n"
            f"{text_b}"
        )

        if QMessageBox.question(
            self,
            self.ctx.i18n.t("update.update_available_title"),
            msg,
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        ) == QMessageBox.StandardButton.Yes:
            
            try:
                dest_dir = choose_download_dir(ctx=self.ctx)
                if not dest_dir:
                    QMessageBox.information(self, self.ctx.i18n.t("update.no_directory_selected_title"), self.ctx.i18n.t("update.no_directory_selected_message"))
                    return

                if "name" not in info:
                    info["name"] = __app_name__
                downloaded_file = DownloadDialog(self.ctx, info, dest_dir=dest_dir, parent=self).exec()

                QMessageBox.information(
                    self,
                    self.ctx.i18n.t("update.download_complete_title"),
                    f"{self.ctx.i18n.t('update.download_complete_message')}:\n{dest_dir}"
                )
            except Exception as e:
                QMessageBox.warning(self, self.ctx.i18n.t("update.download_error"), str(e))