from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtWidgets import QMainWindow, QSplitter, QTextEdit, QTabWidget, QWidget, QVBoxLayout, QLabel, QPushButton, QInputDialog, QMenu, QAction
from gui.widgets.system_table import SystemTable


class SystemsTab(QWidget):
    def __init__(self, parent, main_window):
        super().__init__()

        self.main_window = main_window
        self.parent = parent
        self.systems_tab = QTabWidget()
        self.init_ui()

    def init_ui(self):
        systems_layout = QVBoxLayout()

        add_tab_button = QPushButton('+')
        add_tab_button.clicked.connect(self.add_new_system_tab)
        self.systems_tab.setCornerWidget(add_tab_button, Qt.TopRightCorner)
        self.systems_tab.tabBar().setContextMenuPolicy(Qt.CustomContextMenu)
        self.systems_tab.tabBar().customContextMenuRequested.connect(self._show_context_menu)

        self.systems_tab.setLayout(systems_layout)


    def add_new_system_tab(self):
        tab_name, ok = QInputDialog.getText(self.parent, "New Tab", "Enter the name of the new tab:")

        if ok and tab_name:
            self._create_new_system_tab(tab_name)
            return True
        return False


    def _create_new_system_tab(self, name):
        new_tab, layout, system = (QWidget(), QVBoxLayout(), SystemTable())

        system._name = name
        layout.addWidget(system)
        new_tab.setLayout(layout)

        self.systems_tab.addTab(new_tab, name)
        self.systems_tab.setCurrentIndex(self.systems_tab.count() - 1)


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
        delete_action.triggered.connect(lambda: self._close_tab(tab_index))
        menu.addAction(delete_action)

        menu.exec_(tab_bar.mapToGlobal(pos))

    def _rename_tab(self, index):
        new_name, ok = QInputDialog.getText(self.parent, "Rename System", "Enter new tab name:", text=self.systems_tab.tabBar().tabText(index))
        if ok and new_name:
            self.systems_tab.tabBar().setTabText(index, new_name)

    def _close_tab(self, index):
        self.systems_tab.removeTab(index)

        if self.systems_tab.count() == 0:
            self.main_window._reset_to_empty_systems_tab()


class EmptySystemsTab(QWidget):
    def __init__(self, parent):
        super().__init__()

        self.parent = parent
        self.systems_tab = QWidget()
        self.init_ui()

    def init_ui(self):
        systems_layout = QVBoxLayout()

        empty_label = QLabel("The systems tab is empty. Click the button below to add a new tab.")
        self.add_tab_button = QPushButton("Add")
        self.add_tab_button.setFixedWidth(100)

        systems_layout.addWidget(empty_label)
        systems_layout.addWidget(self.add_tab_button, alignment=Qt.AlignCenter)
        systems_layout.setAlignment(Qt.AlignCenter)

        self.systems_tab.setLayout(systems_layout)


    def connect_action_to_add_button(self, action):
        self.add_tab_button.clicked.connect(action)

