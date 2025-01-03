from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QSizePolicy


class WelcomeScreenWidget(QWidget):
    """
    A widget that displays a welcome message in the chat area.
    """
    def __init__(self):
        """
        Initializes the WelcomeWidget.
        """
        super().__init__()
        welcome_layout = QVBoxLayout()

        self.welcome_label = QLabel((
                "<h1>Welcome to the MoMo AI Chat Assistant!</h1>" +
                "<p><b>Ask your questions below.</b></p>"
            )
        )

        self.welcome_label.setWordWrap(True)
        self.welcome_label.setAlignment(Qt.AlignCenter)
        self.welcome_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # Set the stylesheet to adapt text to full width
        self.welcome_label.setStyleSheet("color: black;")

        welcome_layout.addWidget(self.welcome_label, alignment=Qt.AlignCenter)
        self.setLayout(welcome_layout)
