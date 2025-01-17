from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QTableWidget,
    QTableWidgetItem,
    QLabel,
    QPushButton,
    QFileDialog,
    QSizePolicy,
    QHeaderView
)
from PyQt5.QtCore import Qt
import pandas as pd
from src.dtypes import ResultsMap


class ResultsTab(QWidget):
    def __init__(self, results: ResultsMap, parent=None):
        super().__init__(parent)
        self._init_fields(results)
        self._init_ui()

    def _init_fields(self, results: ResultsMap):
        self._results = results
        self.colums_len = len(results.systems_names) + 1

    def _init_ui(self):
        self.main_layout = QVBoxLayout()
        self.header_layout = QHBoxLayout()

        self.label = QLabel("<h2>Results</h2>")
        self.save_button = QPushButton("Save to Excel")

        self.table = QTableWidget()
        self.table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)

        self.header_layout.addWidget(self.label)
        self.header_layout.addWidget(self.save_button, alignment=Qt.AlignRight)
        self.main_layout.addLayout(self.header_layout)

        self.main_layout.addWidget(self.table)

        self.setLayout(self.main_layout)

        self.save_button.clicked.connect(self._save_to_excel)

        self._setup_table()
        self._set_up_table_data()

    def _setup_table(self):
        self.table.setColumnCount(self.colums_len)
        self.table.setHorizontalHeaderLabels(list(self._results.systems_names) + ["Similarity"])
        self.table.setSortingEnabled(True)


    def _set_up_table_data(self):
        self.table.clearContents()
        self.table.setRowCount(0)

        self.table.setRowCount(len(self._results.similarity_menshure))

        for row_index, (key, value) in enumerate(self._results.similarity_menshure.items()):
            for col_index, system in enumerate(key):
                self.table.setItem(row_index, col_index, QTableWidgetItem(system))
            self.table.setItem(row_index, self.colums_len - 1, QTableWidgetItem(f"{value:.3f}"))

        self.table.sortByColumn(self.colums_len - 1, 1)
        self.table.resizeRowsToContents()

    def _save_to_excel(self):
        file_path, _ = QFileDialog.getSaveFileName(self, "Save Results", "", "Excel Files (*.xlsx)")
        if file_path:
            if not file_path.endswith(".xlsx"):
                file_path += ".xlsx"

            self._results.prototype.to_excel(file_path, index=False, sheet_name="Prototype")
            self._results.results.to_excel(file_path, index=False, sheet_name="Results")

    @property
    def results(self):
        """
        ResultsMap: ResultsMap object.
        """
        return self._results

    @results.setter
    def results(self, results: ResultsMap):
        """
        Set the results to be displayed in the table.
        """
        self._results = results
        self._setup_table()
        self._set_up_table_data()

    @property
    def table_results(self):
        """
        DataFrame with the results.
        """
        return self._results.results

    @property
    def data(self):
        """
        Dict with the parameters used to generate the results.
        """
        return self._results.data
