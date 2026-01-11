#!/usr/bin/env python
# License: GPL v3 Copyright: 2026, Mateusz Jamróz
# pd/ui.dialogs/download/download_dialog.py

from PyQt6.QtWidgets import (QDialog, 
                             QVBoxLayout, 
                             QLabel, 
                             QProgressBar, 
                             QPushButton
                             )
from pd.ui.dialogs.download.download_worker import DownloadWorker

class DownloadDialog(QDialog):
    def __init__(self, ctx, update_info: dict, dest_dir, parent=None):
        super().__init__(parent)
        self.ctx = ctx
        self.update_info = update_info
        self.dest_dir = dest_dir
        self.setWindowTitle(self.ctx.i18n.t("download_dialog.title"))
        self.setMinimumSize(400, 150)
        self._build_ui()

    def _build_ui(self):
        self.label = QLabel(self.ctx.i18n.t("download_dialog.downloading").format(name=self.update_info["name"]))
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)

        self.cancel_button = QPushButton(self.ctx.i18n.t("download_dialog.cancel"))
        self.cancel_button.setEnabled(False)

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.progress_bar)
        layout.addWidget(self.cancel_button)

        self.setLayout(layout)

        if not self.dest_dir:
            self.label.setText(self.ctx.i18n.t("download_dialog.no_directory_selected"))
            return
        
        self.worker = DownloadWorker(self.update_info, self.dest_dir)
        self.worker.progress.connect(self.progress_bar.setValue)
        self.worker.finished.connect(self._on_download_finished)
        self.worker.error.connect(self._on_download_error)

        self.worker.start()

    def _on_download_finished(self, file_path: str):
        self.label.setText(self.ctx.i18n.t("download_dialog.download_finished"))
        self.cancel_button.setText(self.ctx.i18n.t("download_dialog.close"))
        self.cancel_button.setEnabled(True)
        self.cancel_button.clicked.connect(self.accept)

    def _on_download_error(self, error_msg: str):
        self.label.setText(self.ctx.i18n.t("download_dialog.download_error").format(error=error_msg))
        self.cancel_button.setText(self.ctx.i18n.t("download_dialog.close"))
        self.cancel_button.setEnabled(True)
        self.cancel_button.clicked.connect(self.reject)