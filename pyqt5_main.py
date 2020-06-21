import sys
from PyQt5.QtWidgets import QWidget, QApplication, QMainWindow, QFileDialog
from PyQt5.QtCore import pyqtSignal, QObject
from untitled import Ui_MainWindow    #上面的界面文件
from PyQt5.QtGui import QTextCursor


class EmittingStr(QObject):
    textWritten = pyqtSignal(str)  # 定义一个发送str的信号

    def write(self, text):
        self.textWritten.emit(str(text))


class XXX(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(XXX, self).__init__()
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.textEdit.textChanged.connect(self.show_text)
        self.pushButton.clicked.connect(self.file)

        # 下面将输出重定向到textBrowser中
        sys.stdout = EmittingStr(textWritten=self.outputWritten)
        sys.stderr = EmittingStr(textWritten=self.outputWritten)
        # self.pushButton.clicked.connect(self.bClicked)

    def outputWritten(self, text):
        cursor = self.textBrowser_3.textCursor()
        cursor.movePosition(QTextCursor.End)
        cursor.insertText(text)
        self.textBrowser_3.setTextCursor(cursor)
        self.textBrowser_3.ensureCursorVisible()

    def show_text(self):
        self.textBrowser.setText(self.textEdit.toPlainText())

    def file(self):
        gile_path, _ = QFileDialog.getOpenFileName(self, 'lala', '/')
        print(gile_path)
        self.textBrowser_2.setText(str(gile_path))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = XXX()
    mainWindow.show()
    sys.exit(app.exec_())