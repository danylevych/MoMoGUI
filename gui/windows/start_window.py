from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (
    ##########################
    QMainWindow,
    QFileDialog,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QInputDialog,
    QWidget,
    QMessageBox
)


from src.file_validator import load_systems_data, ExcelFileValidator
from gui.styles import load_window_style
from momo.system_models.system_models import SystemModel
from src.dtypes import ResultsMap


class StartWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self._systems_data = []
        self._results_map = None
        self._window_widget = QWidget()
        self._init_ui()
        self.setCentralWidget(self._window_widget)

        self.setStyleSheet(load_window_style())
        self.setFixedSize(470, 250)

        self.setWindowIcon(QIcon("resources/img/logo/logo.ico"))


    def _init_ui(self):
        systems_layout = QVBoxLayout()
        buttons_layout = QHBoxLayout()

        self.setWindowTitle("MoMo")

        label = QLabel()
        label.setText("""
                    <h1>Welcome to MoMo</h1>
                    <p>MoMo is a tool for morphological modeling.</p>
                    <p>Click the button below to create a new system.</p>
                      """)
        label.setAlignment(Qt.AlignTop | Qt.AlignCenter)
        systems_layout.addWidget(label)

        create_button = QPushButton("Create")
        create_button.setFixedWidth(100)
        create_button.clicked.connect(self._create_action)

        upload_file_button = QPushButton("Load File")
        upload_file_button.setFixedWidth(100)
        upload_file_button.clicked.connect(self._load_from_file_action)

        buttons_layout.addWidget(create_button)
        buttons_layout.addWidget(upload_file_button)
        buttons_layout.setAlignment(Qt.AlignCenter)

        systems_layout.addLayout(buttons_layout)
        systems_layout.setContentsMargins(20, 20, 20, 60)

        self._window_widget.setLayout(systems_layout)

    def _load_from_file_action(self):
        file_name, _ = QFileDialog.getOpenFileName(self, 'Open File', filter="Excel Files (*.xlsx *.xls)")

        if file_name:
            file_validator = ExcelFileValidator()
            is_results_file = file_validator.is_results_file(file_name)

            self._systems_data = load_systems_data(file_name)

            if not self._systems_data:
                QMessageBox.warning(self, "Error", "No systems found in the file. Please ensure the file has the correct format or data.")
                return

            if is_results_file:
                try:
                    self._results_map = ResultsMap.from_excel(file_name)
                except Exception as e:
                    print(f"Error loading results: {e}")

            self.close()

    def _create_action(self):
        system_name, ok = QInputDialog.getText(self, "New System", "Enter the name of the new system:")

        if ok and system_name:
            self._systems_data.append(SystemModel(system_name))
            self.close()

    @property
    def systems_data(self):
        return self._systems_data

    @property
    def results_map(self):
        return self._results_map
