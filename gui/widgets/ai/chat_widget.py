from PyQt5.QtCore import QThread, pyqtSignal, QTimer
from PyQt5.QtWidgets import (
    ###########################
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QWidget,
    QScrollArea,
)

from gui.widgets.ai.chat_bubble import ChatBubble
from gui.styles import load_momo_agent_style
from src.assistant import MoMoAgent


class ChatbotWorker(QThread):
    finished = pyqtSignal(str)

    def __init__(self, agent, user_input):
        super().__init__()
        self.agent = agent
        self.user_input = user_input

    def run(self):
        response = self.agent.ask(self.user_input)
        self.finished.emit(response['text'])


class ChatbotApp(QWidget):
    finished = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__()

        self.parent_widget = parent

        layout = QVBoxLayout()

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)

        self.chat_widget = QWidget()
        self.chat_layout = QVBoxLayout(self.chat_widget)
        self.chat_layout.addStretch()
        self.scroll_area.setWidget(self.chat_widget)

        layout.addWidget(self.scroll_area)

        self.text_input = QLineEdit(self)
        self.text_input.returnPressed.connect(self.send_message)
        layout.addWidget(self.text_input)

        send_button = QPushButton("Send", self)
        send_button.clicked.connect(self.send_message)
        layout.addWidget(send_button)
        self.setLayout(layout)

        self.setStyleSheet(load_momo_agent_style())

        self.momo_agent = MoMoAgent()
        self.worker = None
        self.thinking_message = None
        self.thinking_timer = QTimer(self)
        self.thinking_dots = 0


    def closeEvent(self, event):
        self.finished.emit()
        event.accept()

    def send_message(self):
        user_input = self.text_input.text().strip()

        if user_input:
            u_msg = ChatBubble(f"{user_input}", True, "You")
            self.chat_layout.insertWidget(self.chat_layout.count() - 1, u_msg)

            self.thinking_message = ChatBubble("AI is thinking", False, "MoMo Assistant")
            self.chat_layout.insertWidget(self.chat_layout.count() - 1, self.thinking_message)

            self.thinking_timer.timeout.connect(self.update_thinking_message)
            self.thinking_timer.start(500)

            self.worker = ChatbotWorker(self.momo_agent, user_input)
            self.worker.finished.connect(self.display_bot_response)


            self.momo_agent.results(
                prototype=self.parent_widget.result_tab_data["prototype"].__str__(),
                results=self.parent_widget.result_tab_data["df"].__str__(),
            )

            self.worker.start()

            self.text_input.clear()

            v_scroll = self.scroll_area.verticalScrollBar()
            QTimer.singleShot(100, lambda: v_scroll.setValue(v_scroll.maximum()))


    def update_thinking_message(self):
        self.thinking_dots = (self.thinking_dots + 1) % 4
        dots = '.' * self.thinking_dots
        self.thinking_message.label.setText(f"AI is thinking{dots}")


    def display_bot_response(self, response):
        self.thinking_timer.stop()
        if self.thinking_message:
            self.chat_layout.removeWidget(self.thinking_message)
            self.thinking_message.deleteLater()
            self.thinking_message = None

        ai_msg = ChatBubble(f"{response}", False, "MoMo Assistant")
        self.chat_layout.insertWidget(self.chat_layout.count() - 1, ai_msg)

        v_scroll = self.scroll_area.verticalScrollBar()
        QTimer.singleShot(100, lambda: v_scroll.setValue(v_scroll.maximum()))
