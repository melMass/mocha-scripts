from mocha_common_tools import (
    set_current_playhead_time,
    get_current_playhead_time,
)
from PySide2.QtCore import Qt, QCoreApplication
from PySide2.QtWidgets import QDialog, QLineEdit, QPushButton, QHBoxLayout

from mocha.project import get_current_project
from mocha.ui import get_widgets

main_window = get_widgets()['MainWindow']


class FrameJump(QDialog):
    def __init__(self, parent=main_window):
        if sys.version[0] == 3:
            super().__init__(parent)  # initialise using Python 3
        else:
            super(FrameJump, self).__init__(parent)  # initialise using Python 2
        self._widgets = dict()
        self.create_widgets()
        self.create_layout()
        self.create_connections()
        self.proj = get_current_project()
        self.setWindowFlags(Qt.Tool)

    def create_widgets(self):
        self._widgets['Back'] = QPushButton("<", self)
        self._widgets['Frames'] = QLineEdit(self)
        self._widgets['Forward'] = QPushButton(">", self)
        self._widgets['Frames'].insert('10')

    def create_layout(self):
        main_layout = QHBoxLayout(self)
        main_layout.addWidget(self._widgets['Back'])
        main_layout.addWidget(self._widgets['Frames'])
        main_layout.addWidget(self._widgets['Forward'])

        self.setLayout(main_layout)

    def create_connections(self):
        self._widgets['Back'].clicked.connect(lambda: self.do_jump(-1))
        self._widgets['Forward'].clicked.connect(lambda: self.do_jump(+1))

    def do_jump(self, mult):
        current_time = int(get_current_playhead_time())
        frame_value = self._widgets['Frames'].text()
        next_frame = current_time + (int(frame_value) * mult)

        proj_range = self.proj.in_out_range

        if proj_range[0] < next_frame < proj_range[1]:
            err = set_current_playhead_time(next_frame)
        elif next_frame <= proj_range[0]:
            err = set_current_playhead_time(proj_range[0])
        elif next_frame >= proj_range[1]:
            err = set_current_playhead_time(proj_range[1])

        QCoreApplication.processEvents()
