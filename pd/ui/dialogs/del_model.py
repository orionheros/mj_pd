#!/usr/bin/env python
# License: GPL v3 Copyright: 2026, Mateusz Jamróz
# pd/ui/dialogs/del_model.py

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QDialog, 
    QVBoxLayout, 
    QListWidget, 
    QPushButton, 
    QMessageBox, 
    QLabel, 
    QListWidgetItem, 
    QWidget, 
    QHBoxLayout
)
from pd.app_context import AppContext

class DelModelDialog(QDialog):
    def __init__(self, ctx: AppContext, parent=None):
        super().__init__(parent)
        self.ctx = ctx
        self.pd_service = ctx.pd_service
        self.i18n = ctx.i18n
        self.sort_mode = 0  # 0: id, 1: model_name asc, 2: model_name desc

        self.setWindowTitle(self.i18n.t("delete_model.title"))
        self.setMinimumWidth(300)

        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout(self)

        btn_row = QHBoxLayout()
        sort_btn = QPushButton(self.i18n.t("delete_model.sort_button"))
        sort_btn.setToolTip(self.i18n.t("delete_model.sort_button_tooltip"))
        sort_btn.clicked.connect(self._sort_models)
        btn_row.addWidget(sort_btn)
        layout.addLayout(btn_row)

        self.list_of_models = QListWidget(self)
        self.list_of_models.setSelectionMode(QListWidget.SelectionMode.SingleSelection)
        layout.addWidget(self.list_of_models)

        content = self.pd_service.list_models()
        for model_id, model_name in content:
            self._add_model_item(model_id, model_name)

        self.selected_label = QLabel(self)
        self.selected_label.setText("")
        layout.addWidget(self.selected_label)

        self.count_of_selected = QLabel(self)
        self.count_of_selected.setText("")
        layout.addWidget(self.count_of_selected)

        delete_button = QPushButton(self.i18n.t("delete_model.delete_button"))
        delete_button.clicked.connect(lambda: self._delete_model(self.selected_label.text()))
        layout.addWidget(delete_button)

        cancel_button = QPushButton(self.i18n.t("delete_model.cancel_button"))
        cancel_button.clicked.connect(self.reject)
        layout.addWidget(cancel_button)

        cancel_button.setFocus()

        self.list_of_models.setCurrentItem(None)
        self.list_of_models.clearSelection()

        self.list_of_models.currentItemChanged.connect(self._on_model_selected)

    def _add_model_item(self, model_id, model_name):
        widget = QWidget()
        content_layout = QHBoxLayout(widget)
        content_layout.setContentsMargins(0, 0, 0, 0)
        name_label = QLabel(model_name)
        id_label = QLabel(str(model_id))
        id_label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        content_layout.addWidget(name_label)
        content_layout.addStretch()
        content_layout.addWidget(id_label)
        item = QListWidgetItem()
        item.setSizeHint(widget.sizeHint())
        item.setData(Qt.ItemDataRole.UserRole, model_id)
        self.list_of_models.addItem(item)
        self.list_of_models.setItemWidget(item, widget)

    def _on_model_selected(self, current, previous):
        if current:
            model_id = current.data(Qt.ItemDataRole.UserRole)
            widget = self.list_of_models.itemWidget(current)
            if widget:
                labels = widget.findChildren(QLabel)
                if labels:
                    model_name = labels[0].text()
                else:
                    model_name = ""
            else:
                model_name = ""
            self.selected_label.setText(self.i18n.t("delete_model.selected_model") + f" {model_name}")
            count = self.pd_service.count_model(model_id)
            count_text = self.i18n.t("delete_model.count_of_pd").replace("{count}", str(count)) if count > 0 else self.i18n.t("delete_model.no_pd")
            self.count_of_selected.setText(count_text)
            self.id_to_delete = model_id
        else:
            self.selected_label.setText("")
            self.count_of_selected.setText("")
            self.id_to_delete = None

    def _sort_models(self):
        items = []
        for index in range(self.list_of_models.count()):
            item = self.list_of_models.item(index)
            widget = self.list_of_models.itemWidget(item)
            if widget:
                model_id = item.data(Qt.ItemDataRole.UserRole)
                labels = widget.findChildren(QLabel)
                if labels:
                    model_name = labels[0].text()
                else:
                    model_name = ""
                items.append((model_id, model_name))

        self.sort_mode = (self.sort_mode + 1) % 3

        if self.sort_mode == 0:
            items.sort(key=lambda x: x[0])
        elif self.sort_mode == 1:
            items.sort(key=lambda x: x[1].lower())
        elif self.sort_mode == 2:
            items.sort(key=lambda x: x[1].lower(), reverse=True)

        self.list_of_models.clear()
        for model_id, model_name in items:
            self._add_model_item(model_id, model_name)

    def _delete_model(self, model_name):
        if not hasattr(self, "id_to_delete") or self.id_to_delete is None:
            QMessageBox.warning(self, self.i18n.t("delete_model.no_selection_title"), self.i18n.t("delete_model.no_selection_message"))
            return
        
        model_name = model_name.replace(self.i18n.t("delete_model.selected_model"), "").strip()  # Extract model name from label
        reply = QMessageBox.question(
            self, 
            self.i18n.t("delete_model.confirm_title"), 
            self.i18n.t("delete_model.confirm_message").replace("{model_name}", model_name), 
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            try:
                self.pd_service.delete_model(self.id_to_delete)
                current_row = self.list_of_models.currentRow()
                self.list_of_models.takeItem(current_row)
                self.selected_label.setText("")
                self.count_of_selected.setText("")
                self.id_to_delete = None
                QMessageBox.information(self, self.i18n.t("delete_model.success_title"), self.i18n.t("delete_model.success_message").replace("{model_name}", model_name))
            except Exception as e:
                QMessageBox.critical(self, self.i18n.t("delete_model.error_title"), self.i18n.t("delete_model.error_message") + f"\n{str(e)}")
                self.reject()