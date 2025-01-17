from PyQt5.QtWidgets import (
    ##########################
    QWidget,
    QLineEdit,
    QPushButton,
    QHBoxLayout
)


class UserInputWidget(QWidget):
    """
    A widget that contains a QLineEdit and a QPushButton for user input.
    """
    def __init__(self):
        """
        Initializes the UserInputWidget.
        """
        super().__init__()
        self.text_input = QLineEdit(self)
        self.send_button = QPushButton("Send", self)

        layout = QHBoxLayout()
        layout.addWidget(self.text_input)
        layout.addWidget(self.send_button)
        self.setLayout(layout)

    def get_user_input(self):
        """
        Returns the text from the input field.
        """
        return self.text_input.text().strip()

    def clear_input(self):
        """
        Clears the input field.
        """
        self.text_input.clear()

    def set_input(self, text):
        """
        Sets the text of the input field.

        Parameters:
            text (str): The text to set.
        """
        self.text_input.setText(text)

    def set_input_placeholder(self, text):
        """
        Sets the placeholder text of the input field.

        Parameters:
            text (str): The placeholder text to set.
        """
        self.text_input.setPlaceholderText(text)

    def is_input_empty(self):
        """
        Returns True if the input field is empty, False otherwise.
        """
        return not self.text_input.text().strip()
