import sys
from PyQt5.QtWidgets import QWidget, QApplication, QMainWindow, QFileDialog
from PyQt5.QtCore import pyqtSignal, QObject
from ui import Ui_MainWindow
from PyQt5.QtGui import QTextCursor
from copy_file import CopyFile


class EmittingStr(QObject):
    textWritten = pyqtSignal(str)  # 定义一个发送str的信号

    def write(self, text):
        self.textWritten.emit(str(text))


class XXX(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(XXX, self).__init__()
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.path_ore = None
        self.path_des = None
        self.pushButton_1.clicked.connect(self.openfile1)
        self.pushButton_2.clicked.connect(self.openfile2)
        self.pushButton_3.clicked.connect(self.run)

        # 下面将输出重定向到textBrowser中
        # sys.stdout = EmittingStr(textWritten=self.output_written)
        # sys.stderr = EmittingStr(textWritten=self.output_written)

    def run(self):
        if self.path_ore and self.path_des:
            do = CopyFile(self.path_ore, self.path_des)
            do.main()
            # do.all_size
            # do.sum_size
            self.textBrowser_3.setText(do.__repr__())

    def output_written(self, text):
        cursor = self.textBrowser_3.textCursor()
        cursor.movePosition(QTextCursor.End)
        cursor.insertText(text)
        self.textBrowser_3.setTextCursor(cursor)
        self.textBrowser_3.ensureCursorVisible()

    def openfile1(self):
        get_directory_path = QFileDialog.getExistingDirectory(self, "选取指定文件夹", "/")
        self.textBrowser_1.setText(str(get_directory_path))
        self.path_ore = str(get_directory_path)

    def openfile2(self):
        get_directory_path = QFileDialog.getExistingDirectory(self, "选取指定文件夹", "/")
        self.textBrowser_2.setText(str(get_directory_path))
        self.path_des = str(get_directory_path)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = XXX()
    mainWindow.show()
    sys.exit(app.exec_())
