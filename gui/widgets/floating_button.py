from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QPushButton, QApplication


class FloatingButton(QWidget):
    def __init__(self, parent=None, callback=None):
        super().__init__(parent=parent)
        self.callback = callback
        self.parent_widget = parent
        self._init_ui()

        if self.parent_widget:
            self.parent_widget.installEventFilter(self)

    def _init_ui(self):
        self._set_attributes_and_flags()
        self._create_button()
        self._update_position()

    def _set_attributes_and_flags(self):
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setAttribute(Qt.WA_NoSystemBackground)

    def _create_button(self):
        self.button = QPushButton(str(), self)
        self.button.setFixedSize(70, 30)
        self.button.clicked.connect(self._on_click)

    def _update_position(self):
        if self.parent_widget:
            position = self.parent_widget.geometry()
            self.move(position.x() + position.width() - 90, position.y() + position.height() - 100)
        else:
            screen_geometry = QApplication.primaryScreen().geometry()
            self.move(screen_geometry.width() - 100, screen_geometry.height() - 100)

    def _on_click(self):
        if self.callback:
            self.callback()

    def eventFilter(self, source, event):
        if source == self.parent_widget and event.type() in (event.Move, event.Resize):
            self._update_position()
        return super().eventFilter(source, event)
