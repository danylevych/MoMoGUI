from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import (
    ##########################
        QHeaderView,
        QTableWidget,
        QWidget,
        QPushButton,
        QHBoxLayout,
        QVBoxLayout,
        QMenu,
        QInputDialog,
        QTableWidgetItem,
        QMessageBox
    )

from momo.system_models.system_models import SystemModel
from gui.widgets.centered_checkbox import CenteredCheckbox

from .utils import InputText



class SystemTable(QWidget):
    dataChanged = pyqtSignal()

    def __init__(self, system: SystemModel | None = None, parent=None):
        super().__init__(parent=parent)
        self.table_widget = QTableWidget()

        if system:
            self._constructor_system(system)
        else:
            self._constructor_empty()

        self._init_ui()
        self._connect_handlers()

    def _notify_data_change(self):
        self.dataChanged.emit()

    def _init_ui(self):
        self.add_feature_button = QPushButton("Add Feature")
        self.add_alternative_button = QPushButton("Add Alternative")
        self.add_feature_button.clicked.connect(self.add_feature)
        self.add_alternative_button.clicked.connect(self.add_alternative)

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
        header = self.table_widget.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeToContents)

        self._name = system.name
        self._fill_table(system)

    def _fill_table(self, system: SystemModel):
        for i, row in enumerate(system.data.iterrows()):
            for j, value in enumerate(row[1]):
                self.table_widget.setCellWidget(i, j, CenteredCheckbox(value))

        self._notify_data_change()

    def _constructor_empty(self):
        self.table_widget.clearContents()
        self.table_widget.setRowCount(0)
        self.table_widget.setColumnCount(0)
        self._name = "system_model"

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
        self._notify_data_change()

    def _edit_row_header(self, index):
        current_text = self.table_widget.verticalHeaderItem(index).text()
        new_text, ok = InputText.getText(self, 'Edit Row Header', 'Enter new header text:', text=current_text)

        if ok and new_text:
            self.table_widget.verticalHeaderItem(index).setText(new_text)
            self._notify_data_change()

    def _edit_column_header(self, index):
        current_text = self.table_widget.horizontalHeaderItem(index).text()
        new_text, ok = InputText.getText(self, 'Edit Column Header', 'Enter new header text:', text=current_text)

        if ok and new_text:
            self.table_widget.horizontalHeaderItem(index).setText(new_text)
            self._notify_data_change()

    def delete_row(self, index):
        self.table_widget.removeRow(index)
        self._notify_data_change()

    def delete_column(self, index):
        self.table_widget.removeColumn(index)
        self._notify_data_change()

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
            self._notify_data_change()

    def add_alternative(self):
        name, ok = self._get_name_for("alternative")

        if ok and name:
            index = self.table_widget.currentColumn() + 1
            self._add_and_fill("alternative", name, index)
            self._notify_data_change()

    def _get_name_for(self, type):
        existing_names = set()

        if type == "alternative":
            existing_names = {self.table_widget.horizontalHeaderItem(i).text() for i in range(self.table_widget.columnCount())}
        elif type == "feature":
            existing_names = {self.table_widget.verticalHeaderItem(i).text() for i in range(self.table_widget.rowCount())}

        while True:
            name, ok = InputText.getText(self, f'Add {type}', f'Enter new {type} name:')

            if not ok or not name:
                return None, False

            if name in existing_names:
                QMessageBox.warning(self, 'Error', f'The {type} name must be unique! Try again.')
            else:
                return name, ok

    def _add_and_fill(self, type, name, index):
        if type == "alternative":
            self.table_widget.insertColumn(index)
            self.table_widget.setHorizontalHeaderItem(index, QTableWidgetItem(name))
            for i in range(self.table_widget.rowCount()):
                self.table_widget.setCellWidget(i, index, CenteredCheckbox())
            self._notify_data_change()
        elif type == "feature":
            self.table_widget.insertRow(index)
            self.table_widget.setVerticalHeaderItem(index, QTableWidgetItem(name))
            for i in range(self.table_widget.columnCount()):
                self.table_widget.setCellWidget(index, i, CenteredCheckbox())
            self._notify_data_change()

    def is_empty(self):
        return self.table_widget.rowCount() == 0 and self.table_widget.columnCount() == 0

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Delete:
            self.delete_selected()

    def delete_selected(self):
        selected_rows = self.table_widget.selectionModel().selectedRows()
        selected_columns = self.table_widget.selectionModel().selectedColumns()

        if selected_rows:
            for index in sorted(selected_rows, reverse=True):
                self.table_widget.removeRow(index.row())
            self._notify_data_change()

        if selected_columns:
            for index in sorted(selected_columns, reverse=True):
                self.table_widget.removeColumn(index.column())
            self._notify_data_change()

    def to_system_model(self):
        if self.is_empty():
            return SystemModel(self._name)

        data = []
        for i in range(self.table_widget.rowCount()):
            row = []
            for j in range(self.table_widget.columnCount()):
                row.append(int(self.table_widget.cellWidget(i, j).isChecked()))
            data.append(row)

        features = [self.table_widget.verticalHeaderItem(i).text() for i in range(self.table_widget.rowCount())]
        alternatives = [self.table_widget.horizontalHeaderItem(i).text() for i in range(self.table_widget.columnCount())]

        return SystemModel(self._name, data, features=features, alternatives=alternatives)
