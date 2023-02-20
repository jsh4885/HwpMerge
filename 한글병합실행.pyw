from PySide6.QtWidgets import QApplication, QMainWindow
from 한글병합모듈 import Ui_MainWindow


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, *args, obj=None, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)


app = QApplication()
window = MainWindow()
window.show()
app.exec_()