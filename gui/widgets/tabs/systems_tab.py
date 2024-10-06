from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QApplication, QTabWidget, QSplitter, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QInputDialog, QMenu, QAction, QFileDialog, QMessageBox, QAbstractSpinBox
)
from PyQt5.QtGui import QIcon, QPixmap
from gui.widgets.system_table import SystemTable
from src.file_saver import ExcelSaver
from momo.system_models.system_models import SystemModel

class SystemsTab(QWidget):
    def __init__(self, parent, main_window, action_when_empty=None):
        super().__init__()

        self.parent = parent
        self.main_window = main_window
        self.systems_tabs = QTabWidget()
        self.action_when_empty = action_when_empty
        self._init_ui()

    def _init_ui(self):
        buttons_layout = QHBoxLayout()
        for button in self._init_buttons():
            buttons_layout.addWidget(button)
        buttons_layout.setAlignment(Qt.AlignLeft)

        main_layout = QVBoxLayout()
        main_layout.addLayout(buttons_layout)
        main_layout.addWidget(self.systems_tabs)

        self.setLayout(main_layout)

        self.systems_tabs.tabBar().setContextMenuPolicy(Qt.CustomContextMenu)
        self.systems_tabs.tabBar().customContextMenuRequested.connect(self._show_context_menu)


    def _init_buttons(self):
        def create_button(pixmap, size=(40, 30), hint=None, action=None):
            button = QPushButton()
            button.setIcon(QIcon(pixmap))
            button.setIconSize(pixmap.size())
            button.setFixedSize(*size)

            if action:
                button.clicked.connect(action)

            if hint:
                button.setToolTip(hint)
            return button

        pixmap = QPixmap('resources/img/buttons/add.png')
        add_button = create_button(pixmap, hint='Add new system',  action=self.add_system_tab_via_dialog_window)

        pixmap = QPixmap('resources/img/buttons/import.png')
        read_button = create_button(pixmap, hint='Read system from Excel', action=None)

        pixmap = QPixmap('resources/img/buttons/calculate.png')
        calculate_button = create_button(pixmap, hint='Calculate combination', action=None)

        pixmap = QPixmap('resources/img/buttons/save.png')
        save_button = create_button(pixmap, hint='Save selected system', action=self._save_tab)

        pixmap = QPixmap('resources/img/buttons/matrix.png')
        matrix_button = create_button(pixmap, hint='Create pairvise comparison matrix', action=self._hierarchy_analisys)

        pixmap = QPixmap('resources/img/buttons/delete.png')
        delete_button = create_button(pixmap, hint='Delete selected system', action=self._confirm_delete_selected_tab)

        return [add_button, read_button, calculate_button, save_button, matrix_button, delete_button]


    def add_system_tab(self, system: SystemTable):
        self.systems_tabs.addTab(system, system._name)
        self.systems_tabs.setCurrentIndex(self.systems_tabs.count() - 1)


    def add_system_tab_via_dialog_window(self):
        tab_name, ok = QInputDialog.getText(self.parent, "New Tab", "Enter the name of the new tab:")

        if ok and tab_name:
            self.add_system_tab(SystemTable(SystemModel(name=tab_name)))
            return True
        return False


    def _show_context_menu(self, pos):
        tab_bar = self.systems_tabs.tabBar()
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
                                            text=self.systems_tabs.tabBar().tabText(index))
        if ok and new_name:
            self.systems_tabs.tabBar().setTabText(index, new_name)


    def _confirm_delete_tab(self, index):
        reply = QMessageBox.question(self, 'Confirm Delete', "Are you sure you want to delete this tab?",
                                     QMessageBox.Yes | QMessageBox.No,
                                     QMessageBox.No)
        if reply == QMessageBox.Yes:
            self._delete_tab(index)


    def _delete_tab(self, index):
        self.systems_tabs.removeTab(index)

        if self.systems_tabs.count() == 0 and self.action_when_empty:
            self.action_when_empty()


    def _save_tab(self, index):
        #TODO: Check if tab is empty
        tab = self.systems_tabs.widget(index)
        data = tab.to_system_model().data

        file_path, _ = QFileDialog.getSaveFileName(self, "Save Tab as Excel", "", "Excel Files (*.xlsx)")

        if file_path:
            saver = ExcelSaver(file_path)
            saver.save_tab(self.systems_tabs.tabText(index), data)


    def _confirm_delete_selected_tab(self):
        tab_index = self.systems_tabs.currentIndex()
        if tab_index != -1:
            self._confirm_delete_tab(tab_index)

    def _hierarchy_analisys(self):
        tab_index = self.systems_tabs.currentIndex()
        if tab_index != -1:
            tab = self.systems_tabs.widget(tab_index)
            tab.open_anahiepro_window()
