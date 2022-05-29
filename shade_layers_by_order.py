from PySide2.QtWidgets import QMessageBox
from mocha.project import get_current_project


class ShadeMattesByOrder:
    def __init__(self, parent=None):
        self.proj = get_current_project()

    def do_shading(self):
        if not self.proj:
            msg = QMessageBox(self)
            msg.setText("No project open")
            msg.exec_()
        layers = self.proj.layers
        if not layers:
            msg = QMessageBox(self)
            msg.setText("No layers in project")
            msg.exec_()

        divider = 1.0 / len(layers)
        for idx, layer in enumerate(layers):
            shade = 1.0 - ((idx + 1) * divider)
            layer.matte_color = (shade, shade, shade)


if __name__ == "__main__":
    color = ShadeMattesByOrder()
    color.do_shading()
