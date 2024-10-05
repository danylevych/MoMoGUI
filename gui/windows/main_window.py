from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtWidgets import QMainWindow, QSplitter, QTextEdit, QTabWidget, QFileDialog, QWidget, QVBoxLayout, QLabel, QPushButton, QInputDialog, QMenu, QAction
from gui.widgets.tabs.result_tab import ResultsTab
from gui.widgets.tabs.systems_tab import SystemsTab
from gui.widgets.tabs.empty_system_tab import EmptySystemsTab
from src.file_validator import ExcelFileValidator
from gui.widgets.system_table import SystemTable


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self._init_ui()

    def _init_ui(self):
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
        self._init_empty_systems_tab()
        self.right_widget.addTab(ResultsTab(), "Results")

    def _init_empty_systems_tab(self):
        self.systems_tab = EmptySystemsTab(self.right_widget)
        self.right_widget.insertTab(0, self.systems_tab.systems_tab, "Systems")
        self.systems_tab.add_tab_button.clicked.connect(self._create_first_system_tab)
        self.systems_tab.upload_file_button.clicked.connect(self._upload_file)

    def _create_first_system_tab(self):
        self.systems_tab = SystemsTab(self.right_widget, self, lambda: self._reset_to_empty_systems_tab())

        if self.systems_tab.add_system_tab_via_dialog_window():
            self._remove_old_system_tab_and_insert_new(self.systems_tab)

    def _remove_old_system_tab_and_insert_new(self, new_tab):
        self.right_widget.removeTab(0)
        self.right_widget.insertTab(0, new_tab, "Systems")
        self.right_widget.setCurrentIndex(0)

    def _reset_to_empty_systems_tab(self):
        self.right_widget.removeTab(0)
        self._init_empty_systems_tab()
        self.right_widget.setCurrentIndex(0)

    def _upload_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Open File", "", "Excel Files (*.xlsx *.xls)")

        if file_path:
            systems_data = self._get_system_data_and_validate(file_path)

            self.systems_tab = SystemsTab(self.right_widget, self)
            self._remove_old_system_tab_and_insert_new(self.systems_tab)

            for system in systems_data['Systems']:
                self.systems_tab.add_system_tab(SystemTable(system))

            # TODO: add filling prototype and results tabs

    def _get_system_data_and_validate(self, file_path):
        file_validator = ExcelFileValidator()

        try:
            file_validator.validate(file_path)
        except Exception as e:
            self._show_error_message(str(e))
            return

        return file_validator.get_systems_data(file_path)
