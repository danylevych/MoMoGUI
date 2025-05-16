from PyQt5.QtCore import pyqtSignal, QTimer, Qt
from PyQt5.QtWidgets import (
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
    """Main widget for the AI assistant chat interface"""

    # Signal emitted when chat window is closed
    finished = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__()

        # Initialize window properties
        self.parent_widget = parent
        self.momo_agent = MoMoAgent()
        self.worker = None
        self.thinking_message = None

        # Setup the thinking animation
        self.thinking_timer = QTimer(self)
        self.thinking_dots = 0

        # Setup UI components
        self.main_layout = QVBoxLayout(self)
        self.stacked_layout = QStackedLayout()
        self.welcome_widget = WelcomeScreenWidget()
        self.chat_widget = ChatScreenWidget()
        self.input_widget = UserInputWidget()

        self._init_ui()

    def _init_ui(self):
        """Initialize the user interface"""
        # Configure input area
        self.input_widget.set_input_placeholder("Ask your question, I am waiting...")
        self.input_widget.text_input.returnPressed.connect(self._send_message)
        self.input_widget.send_button.clicked.connect(self._send_message)

        # Setup stacked layout for welcome and chat screens
        self.stacked_layout.addWidget(self.welcome_widget)
        self.stacked_layout.addWidget(self.chat_widget)

        # Build the main layout
        self.main_layout.addLayout(self.stacked_layout)
        self.main_layout.addWidget(self.input_widget)

        # Apply styling
        self.setStyleSheet(load_momo_agent_style())

    def closeEvent(self, event):
        """Handle window close event"""
        # Clean up background workers
        if self.worker:
            self.worker.terminate()

        # Notify parent that window is closing
        self.finished.emit()
        event.accept()

    def _send_message(self):
        """Handle sending a message from the user"""
        if user_input := self.input_widget.get_user_input():
            # Switch from welcome to chat screen if needed
            if self._is_welcome_screen_active():
                self._switch_to_chat_screen()

            # Add user message to chat
            self._add_chat_bubble(user_input, is_user=True)

            # Add thinking indicator
            self._add_chat_bubble("AI is thinking", is_user=False, is_thinking=True)

            # Start processing the user's message
            self._start_asking(user_input)

    def _is_welcome_screen_active(self):
        """Check if welcome screen is currently displayed"""
        return self.stacked_layout.currentWidget() == self.welcome_widget

    def _switch_to_chat_screen(self):
        """Switch from welcome to chat screen"""
        self.stacked_layout.setCurrentWidget(self.chat_widget)

    def _add_chat_bubble(self, text, is_user, is_thinking=False):
        """Add a chat bubble to the conversation"""
        if is_thinking:
            # Store reference to thinking bubble for animation
            self.thinking_message = ChatBubble(text, is_user, "You" if is_user else "MoMo Assistant")
            self.chat_widget.chat_layout.insertWidget(self.chat_widget.chat_layout.count() - 1, self.thinking_message)
            return

        # Create and add a normal chat bubble
        chat_bubble = ChatBubble(text, is_user, "You" if is_user else "MoMo Assistant")
        self.chat_widget.chat_layout.insertWidget(self.chat_widget.chat_layout.count() - 1, chat_bubble)

    def _start_asking(self, user_input):
        """Start the process of getting a response from the AI"""
        # Setup thinking animation
        self.thinking_timer.timeout.connect(self._update_thinking_message)
        self.thinking_timer.start(500)

        # Create worker to process request in background
        self.worker = ChatbotWorker(self.momo_agent, user_input)
        self.worker.finished.connect(self._display_assistance_response)

        # Load current result data for context
        self._set_current_tab_results()

        # Start worker and clear input
        self.worker.start()
        self.input_widget.clear_input()
        self._scroll_to_bottom()

    def _scroll_to_bottom(self):
        """Scroll the chat area to show the latest messages"""
        v_scroll = self.chat_widget.scroll_area.verticalScrollBar()
        QTimer.singleShot(100, lambda: v_scroll.setValue(v_scroll.maximum()))

    def _set_current_tab_results(self):
        """Set current results data as context for the AI assistant"""
        result_tab = self.parent_widget.get_current_result_tab()

        # Check if we have valid results data
        if not result_tab or result_tab.table_results.empty:
            return

        # Maximum number of rows to send to the AI assistant to avoid overloading
        MAX_ROWS = 35

        # Get the DataFrame with results
        df = result_tab.table_results[:MAX_ROWS]

        # Convert DataFrame to the desired format: list of arrays [alt1, alt2, ..., similarity]
        results_list = []
        for _, row in df.iterrows():
            # Extract all values from the row into a list
            row_data = row.values.tolist()
            results_list.append(row_data)

        # Convert the list to JSON string
        import json
        results_json = json.dumps(results_list)

        # Pass results data to the AI assistant
        self.momo_agent.set_results(
            prototype=result_tab.results.prototype.__str__(),
            results=results_json,
            metric=result_tab.results.similarity_menshure_type.__str__(),
            systems="\n\n".join(result_tab.results.systems)
        )

    def _update_thinking_message(self):
        """Animate the thinking message with dots"""
        self.thinking_dots = (self.thinking_dots + 1) % 4
        dots = '.' * self.thinking_dots
        self.thinking_message.label.setText(f"AI is thinking{dots}")

    def _display_assistance_response(self, response):
        """Display the AI's response in the chat"""
        # Stop thinking animation
        self.thinking_timer.stop()

        # Remove thinking message
        if self.thinking_message:
            self.chat_widget.chat_layout.removeWidget(self.thinking_message)
            self.thinking_message.deleteLater()
            self.thinking_message = None

        # Add the AI's response
        self._add_chat_bubble(response, is_user=False)
        self._scroll_to_bottom()
