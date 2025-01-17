from PyQt5.QtWidgets import QTabWidget, QToolButton, QTabBar, QWidget
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QSize, Qt

from gui.widgets.tabs.result_tab import ResultsTab
from gui.widgets.tabs.systems_tab import SystemsTab
from gui.widgets.tabs.empty_system_tab import EmptySystemsTab


class TabManager(QTabWidget):
    def __init__(self, parent):
        super().__init__(parent=parent)
        self.result_index = 1


    def add_result_tab(self, tab: ResultsTab, title: str=None, closeable: bool=True):
        if title is None:
            title = f"Result {self.result_index}"
            self.result_index += 1

        self.add_tab(tab, title, closeable)


    def add_tab(self, tab: QWidget, title: str, closeable: bool):
        index = self.addTab(tab, title)

        if closeable:
            close_button = QToolButton()
            close_button.setIcon(QIcon.fromTheme("window-close"))
            close_button.setIconSize(QSize(12, 12))
            close_button.setStyleSheet("""
                QToolButton {
                    background-color: transparent;
                    border: none;
                    padding: 0px;
                }
                QToolButton:hover {
                    background-color: #f44336;
                    border-radius: 10px;
                }
            """)
            close_button.setCursor(Qt.ArrowCursor)
            close_button.setAutoRaise(True)
            close_button.clicked.connect(lambda: self.removeTab(index))
            self.tabBar().setTabButton(index, QTabBar.RightSide, close_button)

        self.setCurrentIndex(index)  # Set the window focus to the new Result tab)


    def insert_system_tab(self, tab: SystemsTab | EmptySystemsTab, title: str="Systems", index: int=0):
        index_ = self.insertTab(index, tab, title)
        self.setCurrentIndex(index_)


    def insert_tab(self, tab, title, where):
        index = self.insertTab(where, tab, title)
        self.setCurrentIndex(index)


    def remove_tab(self, index: int):
        self.removeTab(index)


    def remove_insert_tab(self, tab: SystemsTab | EmptySystemsTab | ResultsTab, title: str, index: int):
        self.remove_tab(index)
        self.insert_tab(tab, title, index)
        self.setCurrentIndex(index)


    def get_current_result_tab(self):
        if self.count() <= 1:
            return None

        current_tab = self.get_current_tab()

        if isinstance(current_tab, ResultsTab):
            return current_tab

        return None


    def get_current_tab(self):
        return self.currentWidget()
