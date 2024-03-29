from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)


from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)


from PySide6.QtWidgets import (QApplication, QLabel, QLineEdit, QListWidget,
    QListWidgetItem, QMainWindow, QMenuBar, QPushButton,
    QSizePolicy, QStatusBar, QWidget, QFileDialog, QMessageBox, QGridLayout)




class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(480, 400)


        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")


        self.pushButton = QPushButton(self.centralwidget)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.clicked.connect(self.btn_remove)


        self.pushButton_2 = QPushButton(self.centralwidget)
        self.pushButton_2.setObjectName(u"pushButton_2")
        self.pushButton_2.clicked.connect(self.btn_FileLoad)


        self.pushButton_3 = QPushButton(self.centralwidget)
        self.pushButton_3.setObjectName(u"pushButton_3")
        self.pushButton_3.clicked.connect(self.btn_merge)


        self.listWidget = QListWidget(self.centralwidget)
        self.listWidget.setObjectName(u"listWidget")
        self.listWidget.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.listWidget.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)


        self.gridLayout_5 = QGridLayout()
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.gridLayout_5.addWidget(self.pushButton, 0, 1, 1, 1)
        self.gridLayout_5.addWidget(self.pushButton_2, 0, 0, 1, 1)
        self.gridLayout_5.addWidget(self.pushButton_3, 0, 2, 1, 1)
        self.gridLayout_5.addWidget(self.listWidget, 1, 0, 1, 3)


        self.gridLayout_7 = QGridLayout(self.centralwidget)
        self.gridLayout_7.setObjectName(u"gridLayout_7")
        self.gridLayout_7.addLayout(self.gridLayout_5, 0, 0, 1, 1)


        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 480, 22))


        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)


        self.retranslateUi(MainWindow)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi


    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.pushButton.setText(QCoreApplication.translate("MainWindow", u"\uc0ad\uc81c", None))
        self.pushButton_2.setText(QCoreApplication.translate("MainWindow", u"\ud30c\uc77c\ucc3e\uae30", None))
        self.pushButton_3.setText(QCoreApplication.translate("MainWindow", u"\ubcd1\ud569\ud558\uae30", None))
    # retranslateUi

    def btn_FileLoad(self):
        import os

        global file_paths, directory
        file_paths, _ = QFileDialog.getOpenFileNames(self, "파일 목록", 'D:/ubuntu/disks/', 'Hwp File(*.hwp);; All File(*)')

        if file_paths:
            directory = os.path.dirname(file_paths[0])
            for file_path in file_paths:
                filename = os.path.basename(file_path)
                item = QListWidgetItem(filename)
                item.setData(Qt.UserRole, file_path)  # 파일 경로를 저장합니다.
                self.listWidget.addItem(item)
        else:
            pass

    def btn_remove(self):
        selected_items = self.listWidget.selectedItems()
        if len(selected_items) == 0:
            QMessageBox.warning(self, "경고", "삭제할 파일이 선택되지 않았습니다.")
            return

        for item in selected_items:
            self.listWidget.takeItem(self.listWidget.row(item))

    def btn_merge(self):

        import os
        from pathlib import Path

        selected_files = []
        for i in range(self.listWidget.count()):
            item = self.listWidget.item(i)
            path = item.data(Qt.UserRole)  # 파일 경로를 가져옵니다.
            selected_files.append(path)

        if len(selected_files) == 0:
            QMessageBox.warning(self, "경고", "병합할 파일이 선택되지 않았습니다.")
            return

        for file in selected_files:
            ext = Path(file).suffix
            if ext.lower() != ".hwp":
                QMessageBox.warning(self, "경고", "한글 파일 이외의 문서가 포함되었습니다.")
                return

        import win32com.client as win32

        hwp = win32.gencache.EnsureDispatch("HWPFrame.HwpObject")
        hwp.RegisterModule("FilePathCheckDLL", "SecurityModule")

        def 첨부삽입(path):
            hwp.HAction.GetDefault("InsertFile", hwp.HParameterSet.HInsertFile.HSet)
            hwp.HParameterSet.HInsertFile.filename = path
            hwp.HParameterSet.HInsertFile.KeepSection = 1
            hwp.HParameterSet.HInsertFile.KeepCharshape = 1
            hwp.HParameterSet.HInsertFile.KeepParashape = 1
            hwp.HParameterSet.HInsertFile.KeepStyle = 1
            hwp.HAction.Execute("InsertFile", hwp.HParameterSet.HInsertFile.HSet)
            return

        hwp.MovePos(3)

        for path in selected_files:
            첨부삽입(path)
            hwp.MovePos(3)

        hwp.HAction.Run("MoveTopLevelBegin")
        hwp.HAction.Run("DeleteBack")

        hwp.HAction.Run("FileSave")
        hwp.Quit(2)

        # function