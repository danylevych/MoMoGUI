def load_window_style():
    with open("gui/styles/window_styles.qss", "r") as file:
        return file.read()
