from PyQt5.QtWidgets import QCheckBox


def create_centered_checkbox(state:bool = False) -> QCheckBox:
    checkbox = QCheckBox()
    checkbox.setChecked(bool(state))
    checkbox.setStyleSheet("margin-left:40%; margin-right:50%; margin-top:5px; margin-bottom:5px;")

    return checkbox
