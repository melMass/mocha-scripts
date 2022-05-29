from mocha.tools import  AbstractTool
from mocha.ui import find_widget
from PySide2.QtWidgets import QAction, QToolBar

from mocha.project import (
    XControlPointData,
    get_current_project,
)


class SpotCleaner(AbstractTool):
    def __init__(self, project):
        action = QAction(None)
        action.setText("Spot Cleaner Tool")
        AbstractTool.__init__(self, action)
        action.setParent(self)
        tools_bar = find_widget("AdvancedToolsBar", QToolBar)
        tools_bar.addAction(action)

    def create_spot(self, pos):

        new_layer = self.proj.add_layer(
            self.proj.default_trackable_clip,
            name="spot",
            frame_number=0,
            view=0,
        )
        points = [[0, 10], [0, 0], [10, 0], [10, 10]]
        x_point_data = []

        for x, y in points:
            x_point = XControlPointData(
                corner=False,
                active=True,
                x=float(x) + pos.x(),
                y=float(y) + pos.y(),
                edge_width=0.0,
                edge_angle_ratio=0.5,
                weight=0.25,
            )
            x_point_data.append(x_point)

        x_contour = new_layer.add_xspline_contour(0.0, tuple(x_point_data))
        print("spot created!")
        return x_contour

    def on_mouse_press(self, event):
        cur_pos = event.pos_on_canvas
        self.create_spot(cur_pos)

    def on_mouse_move(self, event):
        pass

    def on_mouse_release(self, event):
        pass

    def on_activate(self):
        self.proj = get_current_project()

    def on_deactivate(self):
        print("All done")
