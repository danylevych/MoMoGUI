from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import QMainWindow, QSplitter, QTabWidget, QWidget, QVBoxLayout, QSizePolicy, QFileDialog
from gui.widgets.prototype_gui import PrototypeGUI
from gui.widgets.tabs.result_tab import ResultsTab
from gui.widgets.tabs.empty_system_tab import EmptySystemsTab
from gui.widgets.system_table import SystemTable
from gui.widgets.tabs.systems_tab import SystemsTab
from momo.system_models.system_models import SystemModel
from momo.model import MoMoModel
from src.file_validator import read_systems_data
from gui.styles import load_window_style


class MainWindow(QMainWindow):
    systemsLoaded = pyqtSignal(list)

    def __init__(self, systems_data: list[SystemModel] = None):
        super().__init__()
        self.systems_data = systems_data or []
        self.systems_tab = None
        self.prototype_gui = None
        self.chashe_prototype = None

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
        self._create_results_tab()

        self.setWindowTitle("MoMo")
        self.resize(800, 600)
        self.splitter.setSizes(list(map(int, [self.width() * 0.01, self.width() * 0.99])))

        if self.systems_data:
            self._create_prototype_gui()

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

    def _create_results_tab(self):
        self.resultsTab = ResultsTab()
        self.tabs_widget.addTab(self.resultsTab, "Results")

    def _create_prototype_gui(self):
        prototype = MoMoModel(self.systems_data).get_prototype()

        if self.chashe_prototype is not None and not self.chashe_prototype.empty:
            overlapping_idx = prototype.index.intersection(self.chashe_prototype.index)
            prototype.loc[overlapping_idx] = self.chashe_prototype.loc[overlapping_idx]

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

    def _remove_old_system_tab_and_insert_new(self, new_tab):
        self.tabs_widget.removeTab(0)
        self.tabs_widget.insertTab(0, new_tab, "Systems")
        self.tabs_widget.setCurrentIndex(0)

    def _update_window(self):
        self.tabs_widget.setCurrentIndex(0)

        if not self.systems_tab:
            return

        if self.prototype_gui:
            self.chashe_prototype = self.prototype_gui.get_prototype()

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
        print(model.u)


