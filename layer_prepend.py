from mocha.project import  get_current_project

from PySide2.QtWidgets import (QWidget, QApplication, QDialog, QFormLayout, QLineEdit, QDialogButtonBox)
from mocha.project import get_current_project
from mocha.ui import get_widgets


class LayerPrepend:
    def __init__(self):

        self.app = QApplication.instance()
        self.layer_tree = self.get_layer_tree()
        self.layer_prepend()

    def get_layer_tree(self) -> QWidget:
        widgets = get_widgets()
        return widgets["LayerControl"]

    def layer_prepend(self):

        selected_layers = self.layer_tree.selectedIndexes()

        if len(selected_layers) > 0:
            dlg = QDialog()
            layout = QFormLayout()
            edt = QLineEdit()
            layout.addRow("Prefix", edt)
            btn_box = QDialogButtonBox(
                QDialogButtonBox.Ok | QDialogButtonBox.Cancel
            )
            btn_box.accepted.connect(dlg.accept)
            btn_box.rejected.connect(dlg.reject)
            layout.addRow(btn_box)
            dlg.setLayout(layout)
            if dlg.exec_() == QDialog.Accepted:
                self.prepend_selected_layers(edt.text())
                self.layer_tree.update()

    def prepend_selected_layers(self, prefix):

        project = get_current_project()
        selected_layers = self.layer_tree.selectedIndexes()
        for idx in selected_layers:
            layer = project.layer(idx.row())
            layer.name = prefix + layer.name
