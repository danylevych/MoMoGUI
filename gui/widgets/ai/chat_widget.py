from PyQt5.QtCore import pyqtSignal, QTimer, Qt, QEvent
from PyQt5.QtWidgets import (
    ###########################
    QVBoxLayout,
    QStackedLayout,
    QWidget,
)

from .chat_bubble import ChatBubble
from .chat_components.utils import ChatbotWorker
from .chat_components.widgets import (
    WelcomeScreenWidget, ChatScreenWidget, UserInputWidget
)

from src.assistant import MoMoAgent
from gui.widgets.tabs.result_tab import ResultsTab
from gui.styles import load_momo_agent_style


class ChatAssistantWindow(QWidget):
    finished = pyqtSignal()
    mimimized = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__()

        self.parent_widget = parent
        self.momo_agent = MoMoAgent()
        self.worker = None
        self.thinking_message = None
        self.thinking_timer = QTimer(self)
        self.thinking_dots = 0

        self.main_layout = QVBoxLayout(self)
        self.stacked_layout = QStackedLayout()
        self.welcome_widget = WelcomeScreenWidget()
        self.chat_widget = ChatScreenWidget()
        self.input_widget = UserInputWidget()

        self._init_ui()

    def _init_ui(self):
        self.input_widget.set_input_placeholder("Ask your question, I am waiting...")
        self.input_widget.text_input.returnPressed.connect(self._send_message)
        self.input_widget.send_button.clicked.connect(self._send_message)

        self.stacked_layout.addWidget(self.welcome_widget)
        self.stacked_layout.addWidget(self.chat_widget)
        self.main_layout.addLayout(self.stacked_layout)
        self.main_layout.addWidget(self.input_widget)

        self.setStyleSheet(load_momo_agent_style())

    def closeEvent(self, event):
        if self.worker:
            self.worker.terminate()
        self.finished.emit()
        event.accept()


    # def changeEvent(self, event):
    #     if event.type() == QEvent.WindowStateChange:
    #         if self.windowState() & Qt.WindowMinimized:
    #             self.mimimized.emit()
    #     super().changeEvent(event)

    def _send_message(self):
        if user_input := self.input_widget.get_user_input():
            if self._is_welcome_screen_active():
                self._switch_to_chat_screen()

            self._add_chat_bubble(user_input, is_user=True)
            self._add_chat_bubble("AI is thinking", is_user=False, is_thinking=True)
            self._start_asking(user_input)


    def _is_welcome_screen_active(self):
        return self.stacked_layout.currentWidget() == self.welcome_widget


    def _switch_to_chat_screen(self):
        self.stacked_layout.setCurrentWidget(self.chat_widget)


    def _add_chat_bubble(self, text, is_user, is_thinking=False):
        if is_thinking:
            self.thinking_message = ChatBubble(text, is_user, "You" if is_user else "MoMo Assistant")
            self.chat_widget.chat_layout.insertWidget(self.chat_widget.chat_layout.count() - 1, self.thinking_message)
            return

        chat_bubble = ChatBubble(text, is_user, "You" if is_user else "MoMo Assistant")
        self.chat_widget.chat_layout.insertWidget(self.chat_widget.chat_layout.count() - 1, chat_bubble)


    def _start_asking(self, user_input):
        self.thinking_timer.timeout.connect(self._update_thinking_message)
        self.thinking_timer.start(500)

        self.worker = ChatbotWorker(self.momo_agent, user_input)
        self.worker.finished.connect(self._display_assistance_response)

        self._set_current_tab_results()

        self.worker.start()
        self.input_widget.clear_input()
        self._scroll_to_bottom()


    def _scroll_to_bottom(self):
        v_scroll = self.chat_widget.scroll_area.verticalScrollBar()
        QTimer.singleShot(100, lambda: v_scroll.setValue(v_scroll.maximum()))


    def _set_current_tab_results(self):
        result_tab :ResultsTab = self.parent_widget.get_current_result_tab()

        if not result_tab:
            return

        if result_tab.table_results.empty:
            return

        self.momo_agent.results(
            prototype=result_tab.results.prototype.__str__(),
            results=result_tab.table_results[:35].__str__(),
            metric=result_tab.results.similarity_menshure_type.__str__()
        )


    def _update_thinking_message(self):
        self.thinking_dots = (self.thinking_dots + 1) % 4
        dots = '.' * self.thinking_dots
        self.thinking_message.label.setText(f"AI is thinking{dots}")


    def _display_assistance_response(self, response):
        self.thinking_timer.stop()
        if self.thinking_message:
            self.chat_widget.chat_layout.removeWidget(self.thinking_message)
            self.thinking_message.deleteLater()
            self.thinking_message = None

        self._add_chat_bubble(response, is_user=False)
        self._scroll_to_bottom()
