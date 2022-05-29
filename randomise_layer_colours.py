from PySide2.QtWidgets import QMessageBox
from random import random
from mocha.project import get_current_project


class RandomiseColours:
    def __init__(self, parent=None):
        self.proj = get_current_project()

    def do_color(self):
        if not self.proj:
            msg = QMessageBox(self)
            msg.setText("No project open")
            msg.exec_()
        layers = self.proj.layers
        if not layers:
            msg = QMessageBox(self)
            msg.setText("No layers in project")
            msg.exec_()

        for layer in layers:
            layer.matte_color = (random(), random(), random())


if __name__ == "__main__":
    color = RandomiseColours()
    color.do_color()
