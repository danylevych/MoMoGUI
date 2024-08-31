from PyQt5.QtWidgets import QWidget, QCheckBox,QHBoxLayout
from PyQt5.QtCore import Qt


class CenteredCheckBox(QWidget):
    def __init__(self, parent=None, state=0):
        super().__init__(parent)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setAlignment(Qt.AlignCenter)

        self.checkbox = QCheckBox()
        self.checkbox.setChecked(state)
        layout.addWidget(self.checkbox)

        self.setLayout(layout)

    def toggle(self):
        self.checkbox.toggle()
