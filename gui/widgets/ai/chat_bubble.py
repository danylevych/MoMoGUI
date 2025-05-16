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
        self.label.setTextInteractionFlags(Qt.TextSelectableByMouse)

        self.label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)

        self.outer_layout = QVBoxLayout(self)
        self.outer_layout.setContentsMargins(10, 10, 10, 10)

        self.title_label = QLabel(title)
        self.title_label.setObjectName("title")

        self.bubble_layout = QHBoxLayout()
        self.bubble_layout.setContentsMargins(0, 0, 0, 0)


    def _get_html_text(self, text_markdown):
        table_style = """
        <style>
        body {
            font-family: 'Arial', sans-serif;
            font-size: 16px;
            line-height: 1.8;
            color: #2C2C2C;
            background-color: #F8F8F8;
            padding: 20px;
        }

        .container {
            background: white;
            padding: 25px;
            border-radius: 12px;
            box-shadow: 2px 2px 12px rgba(0, 0, 0, 0.1);
            max-width: 800px;
            margin: 0 auto;
        }

        h1, h2, h3 {
            color: #5E2D91;
            font-weight: bold;
            margin-top: 20px;
        }

        h1 {
            font-size: 24px;
            border-bottom: 3px solid #7A4F9A;
            padding-bottom: 8px;
        }

        h2 {
            font-size: 20px;
            border-bottom: 2px solid #A57CC5;
            padding-bottom: 6px;
        }

        h3 {
            font-size: 18px;
        }

        table {
            width: 100%;
            margin: 15px 0;
            margin-left: 20px;
            border-radius: 10px;
            border: 2px solid gray;
        }

        th {
            background-color: #7A4F9A;
            color: white;
            font-weight: bold;
            padding: 8px;
            font-size: 14px;
            text-align: center;
        }

        td {
            font-size: 12px;
            padding: 12px;
            text-align: center;
            border-bottom: 1px solid #D3B1E0;
            background-color: transparent;
        }

        ul {
            margin-left: 5px;
            padding-left: 5px;
        }

        ul li {
            margin-bottom: 8px;
        }

        ul ul {
            margin-left: 10px;
            padding-left: 12px;
            list-style-type: "— ";
        }

        code {
            font-family: "Courier New", monospace;
            background-color: #EEE;
            padding: 4px 8px;
            border-radius: 5px;
            font-size: 14px;
            color: #5E2D91;
        }

        pre {
            background-color: #EEE;
            padding: 12px;
            border-radius: 6px;
            overflow-x: auto;
            font-size: 14px;
            line-height: 1.6;
        }
        </style>
        """
        # return table_style + text_markdown


        return table_style + markdown(text_markdown, extensions=['extra', 'tables'])


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
                border: 1px solid #DDDDDD;
                border-radius: 15px;
                padding: 14px;
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
                background-color: #D0BFFF;
                color: #4B0082;
                border: 2px solid #5E2D91;
                border-radius: 15px;
                padding: 14px;
            }
            """
        )

        self.outer_layout.addWidget(self.title_label)
        self.bubble_layout.addWidget(self.label)
        self.bubble_layout.addStretch()
