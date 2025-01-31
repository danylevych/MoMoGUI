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
    QApplication,
    QDesktopWidget,
)
from PyQt5.QtCore import Qt

from gui.widgets.prototype_gui import PrototypeGUI
from gui.widgets.tabs.result_tab import ResultsTab
from gui.widgets.tabs.empty_system_tab import EmptySystemsTab
from gui.widgets.system_table import SystemTable
from gui.widgets.tabs.systems_tab import SystemsTab
from gui.widgets.floating_button import FloatingButton
from gui.styles import load_window_style, load_ask_ai_style
from gui.widgets.ai.chat_widget import ChatAssistantWindow
from gui.windows.utils.tab_manager import TabManager

from src.file_validator import read_systems_data
from src.dtypes import ResultsMap

from momo.system_models.system_models import SystemModel
from momo.model import MoMoModel


class MainWindow(QMainWindow):
    systemsLoaded = pyqtSignal(list)

    def __init__(self, systems_data: list[SystemModel] = None):
        super().__init__()
        self.systems_data = systems_data or []
        self.systems_tab = None
        self.empty_systems_tab = None
        self.prototype_gui = None
        self.cached_prototype = None
        self.chat_window = None

        self._setup_ui()
        self.setStyleSheet(load_window_style())

    def _setup_ui(self):
        self.splitter = QSplitter(Qt.Horizontal, parent=self)
        self.prototype_widget = QWidget(parent=self)
        self.tabs_manager = TabManager(parent=self)

        self.setCentralWidget(self.splitter)

        self.prototype_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.prototype_widget.setLayout(QVBoxLayout())

        self.splitter.addWidget(self.prototype_widget)

        self.splitter.addWidget(self.tabs_manager)

        self._create_systems_tabs()

        self.setWindowTitle("MoMo")
        self.setGeometry(*QDesktopWidget().screenGeometry().getRect())

        if self.systems_data:
            self._resize_splitter()
        else:
            self._resize_splitter(left_ratio=0, right_ratio=1)

        self._ask_ai_button()


    def _ask_ai_button(self):
        self.ask_ai_button = FloatingButton(parent=self)
        self.ask_ai_button.setStyleSheet(load_window_style())
        self.ask_ai_button.button.setText("Ask AI")
        self.ask_ai_button.button.setStyleSheet(load_ask_ai_style())
        self.ask_ai_button.button.clicked.connect(self._show_momo_agent_widget)
        self.ask_ai_button.show()


    def _show_momo_agent_widget(self):
        self.chat_window = ChatAssistantWindow(parent=self)
        self.chat_window.setWindowTitle("MoMo Assistant")
        self.chat_window.setWindowFlags(Qt.Dialog | Qt.WindowCloseButtonHint | Qt.WindowMinimizeButtonHint)

        self.chat_window.setGeometry(self.x() + self.width() - 350,
                                    self.y() + self.height() - 360,
                                    350, 400)
        self.ask_ai_button.hide()
        self.chat_window.finished.connect(self.ask_ai_button.show)

        self.chat_window.show()


    def closeEvent(self, event):
        if self.chat_window:
            self.chat_window.close()
        event.accept()

    def _resize_splitter(self, left_ratio=0.28, right_ratio=0.72):
        self.splitter.setSizes(list(map(int, [self.width() * left_ratio, self.width() * right_ratio])))


    def _create_systems_tabs(self):
        if not self.systems_data:
            self._init_empty_systems_tab()
            self.tabs_manager.insert_system_tab(self.empty_systems_tab)
        else:
            self._init_filled_systems_tab()
            self.tabs_manager.insert_system_tab(self.systems_tab)


    def _init_filled_systems_tab(self):
        self.systems_tab = SystemsTab(parent=self.tabs_manager, main_window=self, on_content_change=self._update_window)
        self.systems_tab.noTabsLeft.connect(self._reset_to_empty_systems_tab)

        for system_model in self.systems_data:
            table_widget = SystemTable(system_model)
            self.systems_tab.add_system_table(table_widget)


    def _init_empty_systems_tab(self):
        self.empty_systems_tab = EmptySystemsTab(parent=self.tabs_manager)
        self.empty_systems_tab.add_tab_button.clicked.connect(self._create_first_system_tab)
        self.empty_systems_tab.upload_file_button.clicked.connect(self._upload_file)


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
        self._resize_splitter()


    def _create_first_system_tab(self):
        self.systems_tab = SystemsTab(parent=self.tabs_manager, main_window=self, on_content_change=self._update_window)
        self.systems_tab.noTabsLeft.connect(self._reset_to_empty_systems_tab)

        if self.systems_tab.add_system_tab_via_dialog_window():
            self.tabs_manager.remove_insert_tab(self.systems_tab, "Systems", 0)


    def _reset_to_empty_systems_tab(self):
        self._init_empty_systems_tab()
        self.tabs_manager.remove_insert_tab(self.empty_systems_tab, "Systems", 0)

        if self.prototype_gui:
            try:
                self.prototype_gui.calculate_button.clicked.disconnect(self._calculate_combinations)
            except TypeError:
                print("Already disconnected")
                pass

            self.prototype_widget.layout().removeWidget(self.prototype_gui)
            self.prototype_gui.hide()
            self.prototype_gui.deleteLater()
            self.prototype_gui = None
            self.cached_prototype = None

            QApplication.processEvents()

        self._resize_splitter(left_ratio=0.01, right_ratio=0.99)


    def _update_window(self):
        self.tabs_manager.setCurrentIndex(0)

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

        self.systems_tab = SystemsTab(parent=self.tabs_manager, main_window=self, on_content_change=self._update_window)
        self.systems_tab.noTabsLeft.connect(self._reset_to_empty_systems_tab)
        self.tabs_manager.remove_insert_tab(self.systems_tab, "Systems", 0)

        for system_model in self.systems_data:
            self.systems_tab.add_system_table(SystemTable(system_model))

        self._recreate_prototype_gui()


    def _read_from_excel(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Open File", "", "Excel Files (*.xlsx *.xls)")

        if not file_path:
            return

        self.systems_data = read_systems_data(file_path)

        for system_model in self.systems_data:
            self.systems_tab.add_system_table(SystemTable(system_model))

        self._recreate_prototype_gui()


    def _calculate_combinations(self):
        if not self.systems_data:
            return

        prototype = self.prototype_gui.get_prototype()
        model = MoMoModel(self.systems_data, prototype)
        model.u = self.prototype_gui.get_similarity_measure_type()

        reults_map = ResultsMap(
            systems_names=model.system_models_.get_system_names(),
            similarity_menshure=model.get_similarity_measures(),
            prototype=prototype,
            similiraty_menshure_type=self.prototype_gui.get_similarity_measure_type()
        )

        self.tabs_manager.add_result_tab(ResultsTab(results=reults_map))


    def get_current_result_tab(self):
        return self.tabs_manager.get_current_result_tab()
