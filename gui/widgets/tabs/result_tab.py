from PyQt5.QtWidgets import (
    ###########################
        QWidget,
        QVBoxLayout,
        QTableWidget,
        QTableWidgetItem,
        QLabel
    )

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
        self.label = QLabel("<h2>Results</h2>")
        self.table = QTableWidget()

        self.setLayout(self.main_layout)
        self.main_layout.addWidget(self.label)
        self.main_layout.addWidget(self.table)

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
