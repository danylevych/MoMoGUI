from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton


class EmptySystemsTab(QWidget):
    def __init__(self, parent):
        super().__init__(parent=parent)
        self.init_ui()

    def init_ui(self):
        systems_layout = QVBoxLayout()
        buttons_layout = QHBoxLayout()

        label = QLabel("The systems tab is empty. Click the button below to add a new tab or upload an excel file.")
        label.setAlignment(Qt.AlignCenter)

        self.add_tab_button = QPushButton("Add")
        self.add_tab_button.setFixedWidth(100)
        self.upload_file_button = QPushButton("Upload")
        self.upload_file_button.setFixedWidth(100)

        buttons_layout.addWidget(self.add_tab_button)
        buttons_layout.addWidget(self.upload_file_button)
        buttons_layout.setAlignment(Qt.AlignCenter)

        systems_layout.addStretch()
        systems_layout.addWidget(label, alignment=Qt.AlignCenter)
        systems_layout.addLayout(buttons_layout)
        systems_layout.addStretch()

        self.setLayout(systems_layout)


    def connect_action_to_add_button(self, action):
        self.add_tab_button.clicked.connect(action)

    def connect_action_to_upload_button(self, action):
        self.upload_file_button.clicked.connect(action)
