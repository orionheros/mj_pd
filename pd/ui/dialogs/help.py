#!/usr/bin/env python
# License: GPL v3 Copyright: 2026, Mateusz Jamróz
# pd/ui/dialogs/about.py

from PyQt6.QtWidgets import (
    QDialog, 
    QVBoxLayout, 
    QLabel, 
    QPushButton, 
    QScrollArea,
    QHBoxLayout
)
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt

from pd.app_context import AppContext

class HelpDialog(QDialog):
    def __init__(self, ctx: AppContext):
        super().__init__()
        self.setWindowTitle(ctx.i18n.t("help.window_title"))
        self.ctx = ctx
        self._build_ui()
        self.resize(500, 600)
        self.setMinimumWidth(500)

    def _build_ui(self):
        layout = QVBoxLayout(self)

        title = QLabel(f"<h2>{self.ctx.i18n.t('help.title')}</h2>")
        subtitle = QLabel(f"<i>{self.ctx.i18n.t('help.subtitle')}</i>")
        subtitle_2 = QLabel(f"{self.ctx.i18n.t('help.subtitle_2')}")
        subtitle_2.setWordWrap(True)
        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addWidget(subtitle_2)

        scroll_content = QDialog()
        scroll_layout = QVBoxLayout(scroll_content)

        # Image and text row
        row = QHBoxLayout()

        img_label = QLabel()
        img_path = self.ctx.resources.image("help_img")
        if img_path:
            pixmap = QPixmap(img_path)
            max_height = 400
            pixmap = pixmap.scaledToHeight(max_height, Qt.TransformationMode.SmoothTransformation)
            img_label.setPixmap(pixmap)
            img_label.setAlignment(Qt.AlignmentFlag.AlignTop)
        row.addWidget(img_label)

        text_v_layout = QVBoxLayout()
        text_v_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        subtitle_3 = QLabel(f"<b>{self.ctx.i18n.t('help.subtitle_3')}</b>")
        subtitle_3.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        subtitle_3.setContentsMargins(10, 10, 10, 0)
        text_v_layout.addWidget(subtitle_3)

        content_1 = QLabel(self.ctx.i18n.t("help.content_1"))
        content_1.setWordWrap(True)
        content_1.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        content_1.setContentsMargins(10, 10, 10, 10)
        text_v_layout.addWidget(content_1)

        row.addLayout(text_v_layout)

        scroll_layout.addLayout(row)

        # Rest of the content
        subtitle_4 = QLabel(f"<b>{self.ctx.i18n.t('help.subtitle_4')}</b>")
        scroll_layout.addWidget(subtitle_4)
        subtitle_5 = QLabel(f"<b>{self.ctx.i18n.t('help.subtitle_5')}</b>")
        scroll_layout.addWidget(subtitle_5)

        content_2 = QLabel(self.ctx.i18n.t("help.content_2"))
        content_2.setWordWrap(True)
        scroll_layout.addWidget(content_2)

        subtitle_6 = QLabel(f"<b>{self.ctx.i18n.t('help.subtitle_6')}</b>")
        scroll_layout.addWidget(subtitle_6)

        content_3 = QLabel(self.ctx.i18n.t("help.content_3"))
        content_3.setWordWrap(True)
        scroll_layout.addWidget(content_3)

        subtitle_7 = QLabel(f"<b>{self.ctx.i18n.t('help.subtitle_7')}</b>")
        scroll_layout.addWidget(subtitle_7)
        content_4 = QLabel(self.ctx.i18n.t("help.content_4"))
        content_4.setWordWrap(True)
        scroll_layout.addWidget(content_4)

        content_5 = QLabel(f"<i>{self.ctx.i18n.t('help.content_5')}</i>")
        content_5.setWordWrap(True)
        scroll_layout.addWidget(content_5)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(scroll_content)
        layout.addWidget(scroll_area)

        btn_close = QPushButton(self.ctx.i18n.t("buttons.close"))
        btn_close.clicked.connect(self.accept)
        layout.addWidget(btn_close)