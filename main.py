import logging
from PySide6.QtWidgets import QApplication, QMainWindow
from module import Ui_MainWindow

logging.basicConfig(filename='log.txt', level=logging.DEBUG)
logger = logging.getLogger(__name__)

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, *args, obj=None, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        try:
            self.setupUi(self)
        except ValueError as e:
            logger.warning("An error occurred while setting up UI: %s", e, exc_info=True)

if __name__ == '__main__':
    app = QApplication()
    window = MainWindow()
    window.show()
    app.exec_()
