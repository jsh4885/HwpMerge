from PySide6.QtWidgets import QApplication, QMainWindow, QListWidgetItem
from moduleA import Ui_MainWindow
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QListWidget, QListWidgetItem
from PySide6.QtCore import Qt, QMimeData
from PySide6.QtGui import QDrag


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, *args, obj=None, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        try:
            self.setupUi(self)
            self.setAcceptDrops(True)
        except ValueError as e:
            pass

        # 드래그 앤 드롭
        self.listWidget.setDragDropMode(QListWidget.InternalMove)  # 수정된 부분
        self.setWindowTitle("HanMerge_1.0")

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        if event.mimeData().hasUrls():
            event.setDropAction(Qt.CopyAction)
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        if event.mimeData().hasUrls():
            event.setDropAction(Qt.CopyAction)
            event.accept()
            urls = [url.toLocalFile() for url in event.mimeData().urls()]
            for url in urls:
                self.listWidget.addItem(QListWidgetItem(url))
        else:
            event.ignore()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            item = self.listWidget.currentItem()
            if item is not None:
                drag = QDrag(self)
                mime_data = QMimeData()
                mime_data.setUrls([item.text()])
                drag.setMimeData(mime_data)
                drag.exec_(Qt.CopyAction)

    def dropEvent(self, event):  # 수정된 부분
        if event.mimeData().hasUrls():
            event.setDropAction(Qt.CopyAction)
            event.accept()
            urls = [url.toLocalFile() for url in event.mimeData().urls()]
            for url in urls:
                item = QListWidgetItem(url)
                self.listWidget.addItem(item)

        else:
            item = self.listWidget.currentItem()
            if item is not None:
                row = self.listWidget.row(item)
                self.listWidget.takeItem(row)
                self.listWidget.insertItem(event.row(), item)
                event.accept()
            else:
                event.ignore()


if __name__ == '__main__':
    app = QApplication()
    window = MainWindow()
    window.show()
    app.exec_()
