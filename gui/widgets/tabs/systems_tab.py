from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QIcon, QPixmap
from gui.widgets.system_table import SystemTable
from src.file_saver import ExcelSaver
from momo.system_models.system_models import SystemModel
from PyQt5.QtWidgets import (
    ##########################
        QWidget,
        QHBoxLayout,
        QVBoxLayout,
        QTabWidget,
        QPushButton,
        QInputDialog,
        QMenu,
        QAction,
        QFileDialog,
        QMessageBox
    )


class SystemsTab(QWidget):
    noTabsLeft = pyqtSignal()

    def __init__(self, parent, main_window=None, on_content_change=None):
        super().__init__(parent)
        self.main_window = main_window
        self.on_content_change = on_content_change
        self.tabs = QTabWidget()
        self._init_ui()

    def _init_ui(self):
        buttons_layout = QHBoxLayout()

        for btn in self._create_toolbar_buttons():
            buttons_layout.addWidget(btn)

        buttons_layout.setAlignment(Qt.AlignLeft)
        main_layout = QVBoxLayout(self)
        main_layout.addLayout(buttons_layout)
        main_layout.addWidget(self.tabs)

        self.setLayout(main_layout)

        self.tabs.tabBar().setContextMenuPolicy(Qt.CustomContextMenu)
        self.tabs.tabBar().customContextMenuRequested.connect(self._show_context_menu)

    def _create_toolbar_buttons(self):
        def create_button(icon_path, tooltip, size=(60, 30), action=None):
            btn = QPushButton()
            pixmap = QPixmap(icon_path)
            btn.setIcon(QIcon(pixmap))
            btn.setIconSize(pixmap.size())
            btn.setFixedSize(*size)
            btn.setToolTip(tooltip)

            if action:
                btn.clicked.connect(action)
            return btn

        # TODO: Add actions to buttons
        add_button = create_button('resources/img/buttons/add.png', 'Add new system', action=self.add_system_tab_via_dialog_window)
        read_button = create_button('resources/img/buttons/import.png', 'Read system from Excel')
        save_button = create_button('resources/img/buttons/save.png', 'Save selected system', action=self._save_selected_tab)
        delete_button = create_button('resources/img/buttons/delete.png', 'Delete selected system', action=self._confirm_delete_selected_tab)

        return [add_button, read_button, save_button, delete_button]

    def add_system_tab(self, system_table: SystemTable):
        self.tabs.addTab(system_table, system_table._name)
        self.tabs.setCurrentIndex(self.tabs.count() - 1)

        if self.on_content_change is not None:
            system_table.dataChanged.connect(self.on_content_change)
            self.on_content_change()

    def add_system_tab_via_dialog_window(self) -> bool:
        tab_name, ok = QInputDialog.getText(self, "New Tab", "Enter the name of the new tab:")

        if ok and tab_name.strip():
            system_model = SystemModel(name=tab_name)
            table_widget = SystemTable(system_model)
            self.add_system_tab(table_widget)
            return True
        return False

    def _show_context_menu(self, pos):
        tab_index = self.tabs.tabBar().tabAt(pos)
        if tab_index == -1:
            return

        menu = QMenu(self)
        rename_action = QAction("Rename", self)
        rename_action.triggered.connect(lambda: self._rename_tab(tab_index))
        menu.addAction(rename_action)

        delete_action = QAction("Delete", self)
        delete_action.triggered.connect(lambda: self._confirm_delete_tab(tab_index))
        menu.addAction(delete_action)

        save_action = QAction("Save", self)
        save_action.triggered.connect(lambda: self._save_tab(tab_index))
        menu.addAction(save_action)

        menu.exec_(self.tabs.tabBar().mapToGlobal(pos))

    def _rename_tab(self, index):
        old_name = self.tabs.tabText(index)
        new_name, ok = QInputDialog.getText(self, "Rename System", "Enter new tab name:", text=old_name)

        if ok and new_name.strip():
            self.tabs.setTabText(index, new_name)
            self.tabs.widget(index)._name = new_name

            if self.on_content_change is not None:
                self.on_content_change()

    def _confirm_delete_tab(self, index):
        reply = QMessageBox.question(self, 'Confirm Delete', "Are you sure you want to delete this tab?",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            self._delete_tab(index)

            if self.on_content_change is not None:
                self.on_content_change()

    def _delete_tab(self, index):
        self.tabs.removeTab(index)
        if self.tabs.count() == 0:
            self.noTabsLeft.emit()

    def _confirm_delete_selected_tab(self):
        tab_index = self.tabs.currentIndex()
        if tab_index != -1:
            self._confirm_delete_tab(tab_index)

    def _save_selected_tab(self):
        tab_index = self.tabs.currentIndex()
        if tab_index != -1:
            self._save_tab(tab_index)

    def _save_tab(self, index):
        tab_widget = self.tabs.widget(index)
        if not tab_widget:
            return

        if tab_widget.is_empty():
            QMessageBox.warning(self, "No data", "This tab is empty. Nothing to save.")
            return

        data = tab_widget.to_system_model().data
        file_path, _ = QFileDialog.getSaveFileName(self, "Save Tab as Excel", "", "Excel Files (*.xlsx)")
        if file_path:
            saver = ExcelSaver(file_path)
            saver.save_tab(self.tabs.tabText(index), data)
