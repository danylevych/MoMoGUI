import sys
from PyQt5.QtWidgets import QApplication
from gui.windows.main_window import MainWindow
from gui.windows.start_window import StartWindow


if __name__ == "__main__":
    app = QApplication(sys.argv)
    start_window = StartWindow()
    start_window.show()
    app.exec_()

    systems_data = start_window.systems_data

    if not systems_data:
        sys.exit()

    main_window = MainWindow(systems_data)
    main_window.show()
    sys.exit(app.exec_())
