from markdown import markdown
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    ###########################
    QVBoxLayout, QWidget, QLabel,
    QSizePolicy, QHBoxLayout
)


class ChatBubble(QWidget):
    def __init__(self, text_markdown, is_user, title):
        super().__init__()

        html_text = self._get_html_text(text_markdown)
        self._init_buble_heart(html_text, title)
        self._handle_user(is_user)

    def _init_buble_heart(self, html_text, title):
        self.label = QLabel()
        self.label.setTextFormat(Qt.RichText)
        self.label.setWordWrap(True)
        self.label.setMidLineWidth(300)
        self.label.setText(html_text)

        self.label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)

        self.outer_layout = QVBoxLayout(self)
        self.outer_layout.setContentsMargins(0, 0, 0, 0)

        self.title_label = QLabel(title)
        self.title_label.setObjectName("title")

        self.bubble_layout = QHBoxLayout()
        self.bubble_layout.setContentsMargins(0, 0, 0, 0)

    def _get_html_text(self, text_markdown):
        table_style = """
            <style>
                table {
                    border: 1px solid black;
                    border-collapse: collapse;
                    width: 100%;
                }
                th, td {
                    border: 1px solid black;
                    padding: 8px;
                    text-align: left;
                }
            </style>
        """

        return table_style + markdown(text_markdown, extensions=['tables'])


    def _handle_user(self, is_user):
        if is_user:
            self._set_user_bubble()
        else:
            self._set_assistant_bubble()

        self.outer_layout.addLayout(self.bubble_layout)

    def _set_user_bubble(self):
        self.label.setStyleSheet(
            """
            QLabel {
                background-color: white;
                color: #333333;
                border: 1px solid #FFFFFF;
                border-radius: 15px;
                padding: 10px;
            }
            """
        )

        self.title_label.setAlignment(Qt.AlignRight)
        self.outer_layout.addWidget(self.title_label)
        self.bubble_layout.addStretch()
        self.bubble_layout.addWidget(self.label)


    def _set_assistant_bubble(self):
        self.label.setStyleSheet(
            """
            QLabel {
                background-color: #E8D8FF;
                color: #5E2D91;
                border: 1px solid #E8D8FF;
                border-radius: 15px;
                padding: 10px;
            }
            """
        )

        self.outer_layout.addWidget(self.title_label)
        self.bubble_layout.addWidget(self.label)
        self.bubble_layout.addStretch()
