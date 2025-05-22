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
        QSizePolicy,
        QHeaderView,
    )

from momo.prototype import Prototype
from gui.widgets.centered_checkbox import CenteredCheckbox


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
        similarity_layout.setSpacing(2)

        self.u_label = QLabel("Similarity measure:")
        font = self.u_label.font()
        font.setBold(True)
        self.u_label.setFont(font)

        self.u_type = QComboBox()
        self.u_type.addItems(["Sorensen-Dice", "Jaccard"])

        similarity_layout.addRow(self.u_label, self.u_type)
        self.main_layout.addLayout(similarity_layout)

        self.calculate_button = QPushButton("Calculate combinations")
        self.main_layout.addSpacing(10)
        self.main_layout.addWidget(self.calculate_button)

        self.populate_table()

    def populate_table(self):
        self.table.setRowCount(len(self.prototype))
        self.table.setColumnCount(3)

        self.table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        self.table.setHorizontalHeaderLabels(["System", "Feature", "State"])

        self.table.verticalHeader().setSectionResizeMode(QHeaderView.Fixed)
        self.table.verticalHeader().setDefaultSectionSize(30)

        for row_index, (index, state) in enumerate(self.prototype.items()):
            system, feature = index

            system_item = QTableWidgetItem(system)
            system_item.setFlags(system_item.flags() & ~Qt.ItemIsEditable)
            self.table.setItem(row_index, 0, system_item)

            feature_item = QTableWidgetItem(feature)
            feature_item.setFlags(feature_item.flags() & ~Qt.ItemIsEditable)
            self.table.setItem(row_index, 1, feature_item)

            checkbox = CenteredCheckbox(state=bool(state))
            checkbox.stateChanged(lambda state, index=index: self.on_state_changed(index, state))
            self.table.setCellWidget(row_index, 2, checkbox)

        self.table.cellClicked.connect(self.on_cell_clicked)

    def on_state_changed(self, index, state):
        self.prototype[index] = 1 if state == Qt.Checked else 0

    def on_cell_clicked(self, row, column):
        if column == 2:  # State column
            checkbox = self.table.cellWidget(row, column)
            checkbox.toggle()

    def get_prototype(self):
        return self.prototype

    def set_measure_type(self, measure_type: str):
        if measure_type == "sorensen_dice":
            self.u_type.setCurrentIndex(0)
        elif measure_type == "jaccard":
            self.u_type.setCurrentIndex(1)
        else:
            pass

    def get_similarity_measure_type(self):
        return self.u_type.currentText().replace("-", "_").lower()
