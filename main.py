import sys
from PyQt5.QtWidgets import QApplication
from gui.windows.main_window import MainWindow
from gui.windows.start_window import StartWindow


if __name__ == "__main__":
    app = QApplication(sys.argv)
    # start_window = StartWindow()
    # start_window.show()
    # app.exec_()

    # systems_data = start_window.systems_data
    # print("Systems data:", systems_data)

    main_window = MainWindow([])
    main_window.show()
    sys.exit(app.exec_())


# from src.ai import MoMoAgent


# agent = MoMoAgent()

# print(agent.ask("hello"))
# print("\n"*4)
# print(agent.ask("What can you help me with?"))
# print("\n"*4)
# print(agent.memory)
# print("\n"*4)
# print(agent.ask("What is Morfological Method?"))

