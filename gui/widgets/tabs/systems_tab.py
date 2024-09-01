from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QTabWidget, QSplitter, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QInputDialog, QMenu, QAction, QFileDialog, QMessageBox
from gui.widgets.system_table import SystemTable
from src.file_saver import ExcelSaver
from momo.system_models.system_models import SystemModel


class SystemsTab(QWidget):
    def __init__(self, parent, main_window, action_when_empty=None):
        super().__init__()

        self.parent = parent
        self.main_window = main_window
        self.action_when_empty = action_when_empty
        self.init_ui()

    def init_ui(self):
        spliter = QSplitter()
        spliter.setSizes([[170], [500]])

        main_layout = QVBoxLayout()
        button_layout = QHBoxLayout()

        add_button = QPushButton('Add')
        add_button.clicked.connect(self.add_system_tab_via_dialog_window)
        button_layout.addWidget(add_button)

        read_button = QPushButton('Read from File')
        # read_button.clicked.connect(self._read_from_file)
        button_layout.addWidget(read_button)

        calculate_button = QPushButton('Calculate Combinations')
        # calculate_button.clicked.connect(self._calculate_combinations)
        button_layout.addWidget(calculate_button)

        delete_button = QPushButton('Delete')
        delete_button.clicked.connect(self._confirm_delete_selected_tab)
        button_layout.addWidget(delete_button)

        self.systems_tab = QTabWidget()
        main_layout.addLayout(button_layout)
        main_layout.addWidget(self.systems_tab)

        self.setLayout(main_layout)

        self.systems_tab.tabBar().setContextMenuPolicy(Qt.CustomContextMenu)
        self.systems_tab.tabBar().customContextMenuRequested.connect(self._show_context_menu)

    def add_system_tab(self, system: SystemTable):
        self.systems_tab.addTab(system, system._name)
        self.systems_tab.setCurrentIndex(self.systems_tab.count() - 1)

    def add_system_tab_via_dialog_window(self):
        tab_name, ok = QInputDialog.getText(self.parent, "New Tab", "Enter the name of the new tab:")

        if ok and tab_name:
            self.add_system_tab(SystemTable(SystemModel(name=tab_name)))
            return True
        return False

    def _show_context_menu(self, pos):
        tab_bar = self.systems_tab.tabBar()
        tab_index = tab_bar.tabAt(pos)

        if tab_index == -1:
            return

        menu = QMenu(self)

        rename_action = QAction("Rename")
        rename_action.triggered.connect(lambda: self._rename_tab(tab_index))
        menu.addAction(rename_action)

        delete_action = QAction("Delete")
        delete_action.triggered.connect(lambda: self._confirm_delete_tab(tab_index))
        menu.addAction(delete_action)

        save_action = QAction("Save")
        save_action.triggered.connect(lambda: self._save_tab(tab_index))
        menu.addAction(save_action)
        menu.exec_(tab_bar.mapToGlobal(pos))

    def _rename_tab(self, index):
        new_name, ok = QInputDialog.getText(self.parent, "Rename System", "Enter new tab name:",
                                            text=self.systems_tab.tabBar().tabText(index))
        if ok and new_name:
            self.systems_tab.tabBar().setTabText(index, new_name)

    def _confirm_delete_tab(self, index):
        reply = QMessageBox.question(self, 'Confirm Delete', "Are you sure you want to delete this tab?",
                                     QMessageBox.Yes | QMessageBox.No,
                                     QMessageBox.No)
        if reply == QMessageBox.Yes:
            self._delete_tab(index)

    def _delete_tab(self, index):
        self.systems_tab.removeTab(index)

        if self.systems_tab.count() == 0 and self.action_when_empty:
            self.action_when_empty()

    def _save_tab(self, index):
        tab = self.systems_tab.widget(index)
        data = tab.to_system_model().data

        file_path, _ = QFileDialog.getSaveFileName(self, "Save Tab as Excel", "", "Excel Files (*.xlsx)")

        if file_path:
            saver = ExcelSaver(file_path)
            saver.save_tab(self.systems_tab.tabText(index), data)

    def _confirm_delete_selected_tab(self):
        tab_index = self.systems_tab.currentIndex()
        if tab_index != -1:
            self._confirm_delete_tab(tab_index)
