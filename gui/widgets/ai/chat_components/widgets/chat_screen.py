

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QScrollArea


class ChatScreenWidget(QWidget):
    """
    A widget that contains the chat area, for displaying chat messages.
    """
    def __init__(self):
        """
        Initializes the ChatScreenWidget.
        """
        super().__init__()
        chat_layout = QVBoxLayout()

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)

        self.chat_area_widget = QWidget()
        self.chat_layout = QVBoxLayout(self.chat_area_widget)
        self.chat_layout.addStretch()
        self.scroll_area.setWidget(self.chat_area_widget)

        chat_layout.addWidget(self.scroll_area)
        self.setLayout(chat_layout)
