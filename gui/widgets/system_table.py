from gui.widgets.centered_checkbox import CenteredCheckBox

from random import randint
from PyQt5.QtCore import Qt
from momo.system_models.system_models import SystemModel
from anahiepro.models.model import Model
from anahiepro.nodes import Problem, Criteria, Alternative
from PyQt5.QtWidgets import QTableWidget, QHBoxLayout, QVBoxLayout, QWidget, QInputDialog, QMenu, QTableWidgetItem, QPushButton
from gui.windows.pairwise_comparison_window import ComparisonMatrixWindow

class SystemTable(QWidget):
    def __init__(self, system: SystemModel | None = None, parent=None):
        super().__init__(parent=parent)

        self.anahiepro_model = None

        # Create table widget
        self.table_widget = QTableWidget()

        if system:
            self._constructor_system(system)
        else:
            self._constructor_empty()
            self._name = "system_model" + str(randint(0, 10000))

        self._connect_handlers()

        # Create buttons
        self.add_feature_button = QPushButton("Add Feature")
        self.add_alternative_button = QPushButton("Add Alternative")

        self.add_feature_button.clicked.connect(self.add_feature)
        self.add_alternative_button.clicked.connect(self.add_alternative)

        # Layout
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.add_feature_button)
        button_layout.addWidget(self.add_alternative_button)

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.table_widget)
        main_layout.addLayout(button_layout)
        self.setLayout(main_layout)


    def _constructor_system(self, system: SystemModel):
        self.table_widget.setRowCount(len(system.data.index))
        self.table_widget.setColumnCount(len(system.data.columns))
        self.table_widget.setHorizontalHeaderLabels(system.data.columns)
        self.table_widget.setVerticalHeaderLabels(system.data.index)
        self._name = system.name
        self._fill_table(system)


    def _fill_table(self, system: SystemModel):
        for i, row in enumerate(system.data.iterrows()):
            for j, value in enumerate(row[1]):
                checkbox = CenteredCheckBox(state=Qt.Checked if value else Qt.Unchecked)
                self.table_widget.setCellWidget(i, j, checkbox)


    def _constructor_empty(self):
        self.table_widget.clearContents()
        self.table_widget.setRowCount(0)
        self.table_widget.setColumnCount(0)


    def _connect_handlers(self):
        self.table_widget.cellClicked.connect(self.on_cell_clicked)

        self.table_widget.horizontalHeader().setContextMenuPolicy(Qt.CustomContextMenu)
        self.table_widget.horizontalHeader().customContextMenuRequested.connect(self.show_column_context_menu)

        self.table_widget.verticalHeader().setContextMenuPolicy(Qt.CustomContextMenu)
        self.table_widget.verticalHeader().customContextMenuRequested.connect(self.show_row_context_menu)

        self.table_widget.horizontalHeader().sectionDoubleClicked.connect(self._edit_column_header)
        self.table_widget.verticalHeader().sectionDoubleClicked.connect(self._edit_row_header)


    def on_cell_clicked(self, row, column):
        self.table_widget.cellWidget(row, column).toggle()


    def _edit_row_header(self, index):
        current_text = self.table_widget.verticalHeaderItem(index).text()
        new_text, ok = QInputDialog.getText(self, 'Edit Row Header', 'Enter new header text:', text=current_text)
        if ok:
            self.table_widget.verticalHeaderItem(index).setText(new_text)


    def _edit_column_header(self, index):
        current_text = self.table_widget.horizontalHeaderItem(index).text()
        new_text, ok = QInputDialog.getText(self, 'Edit Column Header', 'Enter new header text:', text=current_text)
        if ok:
            self.table_widget.horizontalHeaderItem(index).setText(new_text)


    def delete_row(self, index):
        self.table_widget.removeRow(index)
        self._check_empty_table()


    def delete_column(self, index):
        self.table_widget.removeColumn(index)
        self._check_empty_table()


    def show_column_context_menu(self, pos):
        menu = QMenu()
        edit_action = menu.addAction("Edit")
        insert_action = menu.addAction("Add Alternative")
        delete_action = menu.addAction("Delete")

        action = menu.exec_(self.table_widget.horizontalHeader().mapToGlobal(pos))

        if action == edit_action:
            self._edit_column_header(self.table_widget.horizontalHeader().logicalIndexAt(pos))
        elif action == delete_action:
            self.delete_column(self.table_widget.horizontalHeader().logicalIndexAt(pos))
        elif action == insert_action:
            self.add_alternative()


    def show_row_context_menu(self, pos):
        menu = QMenu()
        edit_action = menu.addAction("Edit")
        insert_action = menu.addAction("Add Feature")
        delete_action = menu.addAction("Delete")

        action = menu.exec_(self.table_widget.verticalHeader().mapToGlobal(pos))

        if action == edit_action:
            self._edit_row_header(self.table_widget.verticalHeader().logicalIndexAt(pos))
        elif action == delete_action:
            self.delete_row(self.table_widget.verticalHeader().logicalIndexAt(pos))
        elif action == insert_action:
            self.add_feature()


    def add_feature(self):
        name, ok = self._get_name_for("feature")

        if ok and name:
            index = self.table_widget.currentRow() + 1
            self._add_and_fill("feature", name, index)


    def add_alternative(self):
        name, ok = self._get_name_for("alternative")

        if ok and name:
            index = self.table_widget.currentColumn() + 1
            self._add_and_fill("alternative", name, index)


    def _get_name_for(self, type):
        name, ok = QInputDialog.getText(self, f'Add {type}', f'Enter new {type} name:')
        return name, ok


    def _add_and_fill(self, type, name, index):
        if type == "alternative":
            self.table_widget.insertColumn(index)
            self.table_widget.setHorizontalHeaderItem(index, QTableWidgetItem(name))

            for i in range(self.table_widget.rowCount()):
                self.table_widget.setCellWidget(i, index, CenteredCheckBox())

        elif type == "feature":
            self.table_widget.insertRow(index)
            self.table_widget.setVerticalHeaderItem(index, QTableWidgetItem(name))

            for i in range(self.table_widget.columnCount()):
                self.table_widget.setCellWidget(index, i, CenteredCheckBox())


    def _check_empty_table(self):
        if self.table_widget.rowCount() == 0 and self.table_widget.columnCount() == 0:
            self.table_widget.clearContents()


    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Delete:
            self.delete_selected()


    def delete_selected(self):
        selected_rows = self.table_widget.selectionModel().selectedRows()
        selected_columns = self.table_widget.selectionModel().selectedColumns()

        if selected_rows:
            for index in sorted(selected_rows, reverse=True):
                self.table_widget.removeRow(index.row())

        if selected_columns:
            for index in sorted(selected_columns, reverse=True):
                self.table_widget.removeColumn(index.column())

        self._check_empty_table()


    def to_system_model(self):
        data = []
        for i in range(self.table_widget.rowCount()):
            row = []
            for j in range(self.table_widget.columnCount()):
                row.append(int(self.table_widget.cellWidget(i, j).checkbox.isChecked()))
            data.append(row)

        features = [self.table_widget.verticalHeaderItem(i).text() for i in range(self.table_widget.rowCount())]
        alternatives = [self.table_widget.horizontalHeaderItem(i).text() for i in range(self.table_widget.columnCount())]

        return SystemModel(self._name, data, features=features, alternatives=alternatives)

    def open_anahiepro_window(self):
        if self.anahiepro_model is None or len(self.anahiepro_model.alternatives) != self.table_widget.columnCount():
            problem = Problem(self._name)
            alternatives = [Alternative(self.table_widget.horizontalHeaderItem(i).text()) for i in range(self.table_widget.columnCount())]
            self.anahiepro_model = Model(problem=problem, criterias=[], alternatives=alternatives)

        self.anahiepro_window = ComparisonMatrixWindow(self.anahiepro_model)
        self.anahiepro_window.show()

