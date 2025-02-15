from PyQt5.QtWidgets import QInputDialog, QWidget



class InputText:
    @staticmethod
    def getText(parent: QWidget, title: str, label: str, text: str = "", size: tuple[int, int] = (400, 60)) -> tuple[str, bool]:
        """
        Show input dialog with specified size.

        Args:
            parent: Parent widget
            title: Dialog window title
            label: Input field label
            size: Tuple of (width, height) for dialog size

        Returns:
            Tuple of (input_text, ok_pressed)
        """
        dialog = QInputDialog(parent)
        dialog.setWindowTitle(title)
        dialog.setLabelText(label)
        dialog.setTextValue(text)

        if size:
            dialog.resize(*size)

        ok_pressed = dialog.exec()
        return dialog.textValue(), bool(ok_pressed)
