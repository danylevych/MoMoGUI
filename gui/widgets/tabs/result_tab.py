from PyQt5.QtWidgets import (
    ###########################
        QWidget,
        QVBoxLayout,
        QTableWidget,
        QTableWidgetItem,
        QLabel
    )


class ResultsTab(QWidget):
    def __init__(self, data: dict, parent=None):
        super().__init__(parent)
        self._try_set_up_data(data)
        self._init_ui()

    def _try_set_up_data(self, data):
        if not isinstance(data, dict):
            raise TypeError("Data should be a dictionary")

        # if not hasattr(data, "systems_names"):
        #     raise ValueError("Data should be a dictionary")

        # if not hasattr(data, "similarity_menshure"):
        #     raise ValueError("Data should be a dictionary")

        print(data)

        self.systems_names = data["systems_names"]
        self.similarity_menshure = data["similarity_menshure"]

        self.colums_len = len(self.systems_names) + 1


    def _init_ui(self):
        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)

        self.label = QLabel("<h2>Results</h2>")
        self.main_layout.addWidget(self.label)

        self.table = QTableWidget()
        self.main_layout.addWidget(self.table)

        self._setup_table()
        self._set_up_table_data()

    def _setup_table(self):
        self.table.setColumnCount(self.colums_len)
        self.table.setHorizontalHeaderLabels(list(self.systems_names) + ["Similarity"])
        self.table.setSortingEnabled(True)


    def _set_up_table_data(self):
        self.table.clearContents()
        self.table.setRowCount(0)

        self.table.setRowCount(len(self.similarity_menshure))

        for row_index, (key, value) in enumerate(self.similarity_menshure.items()):
            for col_index, system in enumerate(key):
                self.table.setItem(row_index, col_index, QTableWidgetItem(system))
            self.table.setItem(row_index, self.colums_len - 1, QTableWidgetItem(f"{value:.3f}"))

        self.table.sortByColumn(self.colums_len - 1, 1)
        #self.table.resizeColumnsToContents()
        self.table.resizeRowsToContents()

    @property
    def data(self):
        return {
            "systems_names": self.systems_names,
            "similarity_menshure": self.similarity_menshure
        }

    @data.setter
    def data(self, data):
        self._try_set_up_data(data)
        self._set_up_table_data()

