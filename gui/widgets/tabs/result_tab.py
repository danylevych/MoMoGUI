from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QInputDialog, QMenu, QAction
from gui.widgets.system_table import SystemTable


class ResultsTab(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        result_layout = QVBoxLayout()
        result_layout.addWidget(QLabel("Content of Results tab"))
        self.setLayout(result_layout)
