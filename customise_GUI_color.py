from PySide2.QtWidgets import (
    QApplication,
    QDialog,
    QLineEdit,
    QGridLayout,
    QFormLayout,
    QPushButton,
)


class ColorChangeDialog(QDialog):
    def __init__(self, parent=None):
        self.app = QApplication.instance()
        QDialog.__init__(self, parent)
        self._widgets = dict()
        self.create_widgets()
        self.create_layout()
        self.create_connections()

    def create_widgets(self):
        self._widgets['background'] = QLineEdit(self, text="#111111")
        self._widgets['text'] = QLineEdit(self, text="#FFFFFF")
        self._widgets['tab'] = QLineEdit(self, text="#000000")
        self._widgets['ok'] = QPushButton("OK", self)
        self._widgets['cancel'] = QPushButton("Cancel", self)

    def create_layout(self):
        main_layout = QGridLayout(self)
        form_layout = QFormLayout(self)
        form_layout.addRow("Background:", self._widgets['background'])
        form_layout.addRow("Text:", self._widgets['text'])
        form_layout.addRow("Tab Colour:", self._widgets['tab'])
        main_layout.addLayout(form_layout, 0, 0, 3, 3)
        main_layout.addWidget(self._widgets['ok'], 3, 1)
        main_layout.addWidget(self._widgets['cancel'], 3, 2)
        self.setLayout(main_layout)

    def create_connections(self):
        self._widgets['ok'].clicked.connect(self.adjust_style_sheet)
        self._widgets['cancel'].clicked.connect(self.reject)

    def adjust_style_sheet(self):
        bgd = self._widgets['background'].text()
        text = self._widgets['text'].text()
        tab = self._widgets['tab'].text()

        print(bgd, text, tab)

        style = self.app.styleSheet()

        style += """
        QWidget {
            background-color: %s;
            color: %s
        }
        """ % (bgd, text)

        self.app.setStyleSheet(style)
