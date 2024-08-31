from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtWidgets import QMainWindow, QSplitter, QTextEdit, QTabWidget, QWidget, QVBoxLayout, QLabel, QPushButton, QInputDialog, QMenu, QAction
from gui.widgets.result_tab import ResultsTab
from gui.widgets.systems_tab import SystemsTab, EmptySystemsTab


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        splitter = QSplitter(Qt.Horizontal)
        self.right_widget = QTabWidget(parent=self)
        self.left_widget = QTextEdit("Prototype")

        splitter.addWidget(self.left_widget)
        splitter.addWidget(self.right_widget)

        splitter.setSizes([200, 800])

        self.setCentralWidget(splitter)

        self.setWindowTitle("Morphological Modeling GUI")
        self.resize(1000, 600)

        self._init_tabs()

    def _init_tabs(self):
        self.systems_tab = EmptySystemsTab(self.right_widget)
        self.right_widget.insertTab(0, self.systems_tab.systems_tab, "Systems")
        self.systems_tab.add_tab_button.clicked.connect(self._create_first_system_tab)
        self.right_widget.addTab(ResultsTab(), "Results")

    def _create_first_system_tab(self):
        self.systems_tab = SystemsTab(self.right_widget, self)

        if self.systems_tab.add_new_system_tab():
            self.right_widget.removeTab(0)
            self.right_widget.insertTab(0, self.systems_tab.systems_tab, "Systems")
            self.right_widget.setCurrentIndex(0)

    def add_new_system_tab(self):
        self.systems_tab.add_new_system_tab()

    def _reset_to_empty_systems_tab(self):
        self.right_widget.removeTab(0)
        self.systems_tab = EmptySystemsTab(self.right_widget)
        self.right_widget.insertTab(0, self.systems_tab.systems_tab, "Systems")
        self.systems_tab.add_tab_button.clicked.connect(self._create_first_system_tab)
        self.right_widget.setCurrentIndex(0)
