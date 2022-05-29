from mocha.project import XControlPointData, View, get_current_project
from PySide2.QtWidgets import (
    QDialog,
    QLineEdit,
    QGridLayout,
    QFormLayout,
    QPushButton,
    QApplication,
)

app = QApplication.instance()
widgets = app.allWidgets()


class GridLayers(QDialog):
    def __init__(self, parent=None):
        QDialog.__init__(self, parent)
        self._widgets = dict()
        self.create_widgets()
        self.create_layout()
        self.create_connections()

    def create_widgets(self):
        self._widgets["num_x"] = QLineEdit(self)
        self._widgets["num_y"] = QLineEdit(self)
        self._widgets["ok"] = QPushButton("OK", self)
        self._widgets["cancel"] = QPushButton("Cancel", self)

    def create_layout(self):
        main_layout = QGridLayout(self)
        form_layout = QFormLayout(self)
        form_layout.addRow("Number in X:", self._widgets["num_x"])
        form_layout.addRow("Number in Y:", self._widgets["num_y"])
        main_layout.addLayout(form_layout, 0, 0, 3, 3)
        main_layout.addWidget(self._widgets["ok"], 3, 1)
        main_layout.addWidget(self._widgets["cancel"], 3, 2)
        self.setLayout(main_layout)

    def create_connections(self):
        self._widgets["ok"].clicked.connect(self.create_grid)
        self._widgets["cancel"].clicked.connect(self.reject)

    def create_layer(self, proj, clip, width, height, x, y):

        x_points = (
            XControlPointData(
                corner=True,
                active=True,
                x=float(width * x),
                y=float(height * y),
                edge_width=0.0,
                edge_angle_ratio=0.5,
                weight=0.0,
            ),
            XControlPointData(
                corner=True,
                active=True,
                x=float(width * x),
                y=float((height * y) + height),
                edge_width=0.0,
                edge_angle_ratio=0.5,
                weight=0.0,
            ),
            XControlPointData(
                corner=True,
                active=True,
                x=float((width * x) + width),
                y=float((height * y) + height),
                edge_width=0.0,
                edge_angle_ratio=0.5,
                weight=0.0,
            ),
            XControlPointData(
                corner=True,
                active=True,
                x=float((width * x) + width),
                y=float(height * y),
                edge_width=0.0,
                edge_angle_ratio=0.5,
                weight=0.0,
            ),
        )

        x_layer = proj.add_layer(
            clip, name=("cell" + str(x) + str(y)), view=0, frame_number=0
        )
        x_layer.add_xspline_contour(0, x_points)
        x_layer.parameter(["Track", "TrackingModel"]).set(
            3, time=0, view=View(0)
        )  # turn shear off
        print(
            x_layer.parameter(["Track", "TrackingModel"]).keyframes
        )  # turn shear off

    def create_grid(self):
        proj = get_current_project()
        if not proj:
            self.reject()
        num_x = int(self._widgets["num_x"].text())
        num_y = int(self._widgets["num_y"].text())

        first_clip = proj.default_trackable_clip

        clip_size = proj.clips[first_clip.name].frame_size
        cell_width = int(clip_size[0] / num_x)
        cell_height = int(clip_size[1] / num_y)

        # build layers from bottom of frame to top
        for y in range(num_y - 1, -1, -1):
            for x in range(0, num_x):
                self.create_layer(
                    proj, first_clip, cell_width, cell_height, x, y
                )

        self.accept()


if __name__ == "__main__":
    grid = GridLayers()
    grid.show()
