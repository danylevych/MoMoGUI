import sys
import asyncio
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QWindow
from qasync import QEventLoop

from gui.windows.start_window import StartWindow
from gui.windows.main_window import MainWindow


async def wait_for_close(widget: QWindow):
    while widget.isVisible():
        await asyncio.sleep(0.1)


async def run_app(systems_data=None, results_map=None):
    if not systems_data:
        return

    main_window = MainWindow(systems_data=systems_data, results_map=results_map)
    main_window.show()

    await wait_for_close(main_window)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    start_window = StartWindow()
    start_window.show()
    app.exec_()

    loop = QEventLoop(app)
    asyncio.set_event_loop(loop)
    with loop:
        try:
            loop.run_until_complete(
                run_app(
                    systems_data=start_window.systems_data,
                    results_map=start_window.results_map
                )
            )
        except RuntimeError:
            loop.stop()
