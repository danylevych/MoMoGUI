from PyQt5.QtWidgets import QWidget, QCheckBox, QHBoxLayout
from PyQt5.QtCore import Qt


class CenteredCheckbox(QWidget):
    def __init__(self, state=False, parent=None):
        super().__init__(parent)
        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setAlignment(Qt.AlignCenter)

        self.checkbox = QCheckBox(self)
        self.checkbox.setChecked(state)
        self.layout.addWidget(self.checkbox)

    def isChecked(self):
        return self.checkbox.isChecked()

    def setChecked(self, checked):
        self.checkbox.setChecked(checked)

    def toggle(self):
        self.checkbox.toggle()

    def stateChanged(self, callback):
        self.checkbox.stateChanged.connect(callback)
