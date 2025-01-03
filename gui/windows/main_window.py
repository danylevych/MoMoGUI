import sys
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import (
    ###########################
    QMainWindow,
    QSplitter,
    QTabWidget,
    QWidget,
    QVBoxLayout,
    QSizePolicy,
    QFileDialog,
    QToolButton,
    QTabBar,
    QApplication,
    QDesktopWidget,
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QSize

from gui.widgets.prototype_gui import PrototypeGUI
from gui.widgets.tabs.result_tab import ResultsTab
from gui.widgets.tabs.empty_system_tab import EmptySystemsTab
from gui.widgets.system_table import SystemTable
from gui.widgets.tabs.systems_tab import SystemsTab
from gui.widgets.floating_button import FloatingButton
from gui.styles import load_window_style, load_ask_ai_style
from gui.widgets.ai.chat_widget import ChatAssistantWindow

from src.file_validator import read_systems_data

from momo.system_models.system_models import SystemModel
from momo.model import MoMoModel



class MainWindow(QMainWindow):
    systemsLoaded = pyqtSignal(list)

    def __init__(self, systems_data: list[SystemModel] = None):
        super().__init__()
        self.systems_data = systems_data or []
        self.systems_tab = None
        self.prototype_gui = None
        self.cached_prototype = None
        self.chat_wndow = None

        self.result_tab_data = {
            "systems_names": "",
            "similarity_menshure": "",
            "prototype": "",
            "df": ""
        }

        self._setup_ui()
        self._setup_connections()
        self.setStyleSheet(load_window_style())

    def _setup_ui(self):
        self.splitter = QSplitter(Qt.Horizontal, parent=self)
        self.setCentralWidget(self.splitter)

        self.prototype_widget = QWidget(parent=self)
        self.prototype_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.prototype_widget.setLayout(QVBoxLayout())

        self.splitter.addWidget(self.prototype_widget)

        self.tabs_widget = QTabWidget(parent=self)
        self.splitter.addWidget(self.tabs_widget)

        self._create_systems_tabs()

        self.setWindowTitle("MoMo")
        screen = QDesktopWidget().screenGeometry()
        self.setGeometry(screen.left(), screen.top(), screen.width(), screen.height())
        self.splitter.setSizes(list(map(int, [self.width() * 0.01, self.width() * 0.99])))

        if self.systems_data:
            self._create_prototype_gui()

        self._ask_ai_button()


    def _ask_ai_button(self):
        self.floating_button = FloatingButton(parent=self)
        self.floating_button.setStyleSheet(load_window_style())
        self.floating_button.button.setText("Ask AI")
        self.floating_button.button.setStyleSheet(load_ask_ai_style())
        self.floating_button.button.clicked.connect(self._create_momo_agent_widget)
        self.floating_button.show()


    def _create_momo_agent_widget(self):
        self.chat_wndow = ChatAssistantWindow(parent=self)
        self.chat_wndow.setAttribute(Qt.WA_DeleteOnClose)
        self.chat_wndow.setWindowTitle("MoMo Assistant")
        self.chat_wndow.setGeometry(self.x() + self.width() - 350,
                                    self.y() + self.height() - 370,
                                    350, 400)
        self.floating_button.hide()
        self.chat_wndow.finished.connect(self.floating_button.show)
        self.chat_wndow.show()


    def closeEvent(self, event):
        if self.chat_wndow:
            self.chat_wndow.close()
        event.accept()


    def _setup_connections(self):
        pass

    def _create_systems_tabs(self):
        if not self.systems_data:
            self._init_empty_systems_tab()
        else:
            self._init_filled_systems_tab()

    def _init_filled_systems_tab(self):
        self.systems_tab = SystemsTab(parent=self.tabs_widget, main_window=self, on_content_change=self._update_window)
        self.systems_tab.noTabsLeft.connect(self._reset_to_empty_systems_tab)

        for system_model in self.systems_data:
            table_widget = SystemTable(system_model)
            self.systems_tab.add_system_tab(table_widget)

        self.tabs_widget.addTab(self.systems_tab, "Systems")

    def _init_empty_systems_tab(self):
        self.empty_systems_tab = EmptySystemsTab(self.tabs_widget)
        index = self.tabs_widget.insertTab(0, self.empty_systems_tab.tabs, "Systems")
        self.tabs_widget.setCurrentIndex(index)

        self.empty_systems_tab.add_tab_button.clicked.connect(self._create_first_system_tab)
        self.empty_systems_tab.upload_file_button.clicked.connect(self._upload_file)

    def _add_tab(self, tab, title, closeable=False):
        index = self.tabs_widget.addTab(tab, title)

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
            close_button.clicked.connect(lambda: self.tabs_widget.removeTab(index))
            self.tabs_widget.tabBar().setTabButton(index, QTabBar.RightSide, close_button)

            self.tabs_widget.setCurrentIndex(index)  # Set the window focus to the new Result tab

    def _create_prototype_gui(self):
        if not self.systems_data:
            return

        prototype = MoMoModel(self.systems_data).get_prototype()

        if self.cached_prototype is not None and not self.cached_prototype.empty:
            overlapping_idx = prototype.index.intersection(self.cached_prototype.index)
            prototype.loc[overlapping_idx] = self.cached_prototype.loc[overlapping_idx]

        self.prototype_gui = PrototypeGUI(prototype)
        self.prototype_gui.calculate_button.clicked.connect(self._calculate_combinations)
        self.prototype_widget.layout().addWidget(self.prototype_gui)
        self.splitter.setSizes(list(map(int, [self.width() * 0.28, self.width() * 0.72])))

    def _create_first_system_tab(self):
        self.systems_tab = SystemsTab(parent=self.tabs_widget, main_window=self, on_content_change=self._update_window)
        self.systems_tab.noTabsLeft.connect(self._reset_to_empty_systems_tab)

        if self.systems_tab.add_system_tab_via_dialog_window():
            self._remove_old_system_tab_and_insert_new(self.systems_tab)

    def _reset_to_empty_systems_tab(self):
        self.tabs_widget.removeTab(0)
        self._init_empty_systems_tab()
        self.tabs_widget.setCurrentIndex(0)

        if self.prototype_gui:
            try:
                self.prototype_gui.calculate_button.clicked.disconnect(self._calculate_combinations)
            except TypeError:
                print("Already disconnected")

            self.prototype_widget.layout().removeWidget(self.prototype_gui)
            self.prototype_gui.hide()
            self.prototype_gui.deleteLater()
            self.prototype_gui = None
            self.cached_prototype = None

            QApplication.processEvents()

        self.splitter.setSizes(list(map(int, [self.width() * 0.01, self.width() * 0.99])))

    def _remove_old_system_tab_and_insert_new(self, new_tab):
        self.tabs_widget.removeTab(0)
        self.tabs_widget.insertTab(0, new_tab, "Systems")
        self.tabs_widget.setCurrentIndex(0)

    def _update_window(self):
        self.tabs_widget.setCurrentIndex(0)

        if not self.systems_tab:
            return

        if self.prototype_gui:
            self.cached_prototype = self.prototype_gui.get_prototype()

        if hasattr(self, 'systems_tab'):
            self.systems_data = []
            for i in range(self.systems_tab.tabs.count()):
                tab_widget = self.systems_tab.tabs.widget(i)
                if isinstance(tab_widget, SystemTable):
                    self.systems_data.append(tab_widget.to_system_model())

        self.systemsLoaded.emit(self.systems_data)
        self._recreate_prototype_gui()

    def _recreate_prototype_gui(self):
        if self.prototype_gui:
            self.prototype_widget.layout().removeWidget(self.prototype_gui)
            self.prototype_gui.deleteLater()
            self.prototype_gui = None

        if self.systems_data:
            self._create_prototype_gui()

    def _upload_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Open File", "", "Excel Files (*.xlsx *.xls)")

        if not file_path:
            return

        self.systems_data = read_systems_data(file_path)
        self.systems_tab = SystemsTab(parent=self.tabs_widget, main_window=self, on_content_change=self._update_window)
        self.systems_tab.noTabsLeft.connect(self._reset_to_empty_systems_tab)
        self._remove_old_system_tab_and_insert_new(self.systems_tab)

        for system_model in self.systems_data:
            self.systems_tab.add_system_tab(SystemTable(system_model))

        self._recreate_prototype_gui()

    def _calculate_combinations(self):
        if not self.systems_data:
            return

        prototype = self.prototype_gui.get_prototype()
        model = MoMoModel(self.systems_data, prototype)
        model.u = self.prototype_gui.get_similarity_measure_type()




        import pandas as pd
        data = model.get_similarity_measures()
        columns = list(model.system_models_.get_system_names()) + ["Similarity"]
        results = [(*list(key), value) for key, value in data.items()]
        df = pd.DataFrame(results, columns=columns).sort_values(by="Similarity", ascending=False)[:30]

        self.result_tab_data = {
            "systems_names": model.system_models_.get_system_names(),
            "similarity_menshure": model.get_similarity_measures(),
            "prototype": model.get_prototype(),
            "df": df
        }

        self._add_tab(ResultsTab(self.result_tab_data), "Results", closeable=True)

