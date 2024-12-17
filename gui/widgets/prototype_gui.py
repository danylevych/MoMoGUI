from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    ##########################
        QTableWidget,
        QTableWidgetItem,
        QVBoxLayout,
        QFormLayout,
        QWidget,
        QLabel,
        QPushButton,
        QComboBox,
    )

from momo.prototype import Prototype
from gui.widgets.utils import create_centered_checkbox


class PrototypeGUI(QWidget):
    def __init__(self, prototype: Prototype, parent=None):
        super().__init__(parent)
        self.prototype = prototype
        self._init_ui()

    def _init_ui(self):
        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)

        self.label = QLabel("<h2>System Prototype</h2>")
        self.label.setAlignment(Qt.AlignCenter)
        self.main_layout.addWidget(self.label)

        self.table = QTableWidget()
        self.main_layout.addWidget(self.table)

        similarity_layout = QFormLayout()
        similarity_layout.setSpacing(2)  # Встановлюємо мінімальну відстань

        self.u_label = QLabel("Similarity measure:")
        font = self.u_label.font()
        font.setBold(True)
        self.u_label.setFont(font)

        self.u_type = QComboBox()
        self.u_type.addItems(["Sorensen–Dice", "Jaccard"])

        similarity_layout.addRow(self.u_label, self.u_type)  # Лейбл зверху, QComboBox знизу
        self.main_layout.addLayout(similarity_layout)

        self.calculate_button = QPushButton("Calculate combinations")
        self.main_layout.addSpacing(10)
        self.main_layout.addWidget(self.calculate_button)

        self.populate_table()


    def populate_table(self):
        self.table.setRowCount(len(self.prototype))
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["System", "Feature", "State"])

        for row_index, (index, state) in enumerate(self.prototype.items()):
            system, feature = index

            system_item = QTableWidgetItem(system)
            system_item.setFlags(system_item.flags() & ~Qt.ItemIsEditable)
            self.table.setItem(row_index, 0, system_item)


            feature_item = QTableWidgetItem(feature)
            feature_item.setFlags(feature_item.flags() & ~Qt.ItemIsEditable)
            self.table.setItem(row_index, 1, feature_item)

            checkbox = create_centered_checkbox(state=bool(state))
            checkbox.stateChanged.connect(lambda state, index=index: self.on_state_changed(index, state))
            self.table.setCellWidget(row_index, 2, checkbox)

        self.table.resizeRowsToContents()

    def on_state_changed(self, index, state):
        self.prototype[index] = 1 if state == Qt.Checked else 0

    def get_prototype(self):
        return self.prototype

    def get_similarity_measure_type(self):
        return self.u_type.currentText().replace("–", "_").lower()
