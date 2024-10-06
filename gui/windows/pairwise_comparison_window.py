from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QMessageBox
)

from anahiepro.models.model import Model

class ComparisonMatrixWindow(QWidget):
    def __init__(self, model: Model):
        super().__init__()
        self.model = model
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        pcm = self.model.get_problem().get_pcm()
        self.size = pcm.shape[0]

        self.table = QTableWidget(self.size, self.size)
        self.table.setHorizontalHeaderLabels([item._name for item in self.model.alternatives])
        self.table.setVerticalHeaderLabels([item._name for item in self.model.alternatives])

        self._update_table()

        layout.addWidget(self.table)

        self.table.itemChanged.connect(self._on_item_changed)

        self.setLayout(layout)
        self.setWindowTitle("Pairwise Comparison Matrix For " + self.model.problem._name)
        self.resize(500, 500)


    def _update_table(self):
        self.table.blockSignals(True)

        pcm = self.model.get_problem().get_pcm()
        for i in range(self.size):
            for j in range(self.size):
                self._set_mark(i, j, round(pcm[i, j], 3))

        self.table.blockSignals(False)


    def _set_mark(self, i, j, value):
        self.table.setItem(i, j, QTableWidgetItem(str(value)))


    def _on_item_changed(self, item):
        i = item.row()
        j = item.column()
        value = item.text()

        try:
            value_float = float(value)
            self.model.problem.set_comparison(i, j, round(value_float))
            self._update_table()

        except ValueError:
            QMessageBox.warning(self, "Invalid Input", "Please enter a valid number.")
            self._update_table()
