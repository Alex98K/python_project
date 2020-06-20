# -*- coding: utf-8 -*-

import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox,QInputDialog,QFileDialog


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(443, 120)
        self.widget = QtWidgets.QWidget(Form)
        self.widget.setGeometry(QtCore.QRect(50, 40, 301, 25))
        self.widget.setObjectName("widget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.widget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.openFileButton = QtWidgets.QPushButton(self.widget)
        self.openFileButton.setObjectName("openFileButton")
        self.horizontalLayout.addWidget(self.openFileButton)
        self.filePathlineEdit = QtWidgets.QLineEdit(self.widget)
        self.filePathlineEdit.setObjectName("filePathlineEdit")
        self.horizontalLayout.addWidget(self.filePathlineEdit)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "QFileDialog打开文件例子"))
        self.openFileButton.setText(_translate("Form", "打开文件"))


class MyMainForm(QMainWindow, Ui_Form):
    def __init__(self, parent=None):
        super(MyMainForm, self).__init__(parent)
        self.setupUi(self)
        self.openFileButton.clicked.connect(self.openFile)

    def openFile(self):
        get_directory_path = QFileDialog.getExistingDirectory(self,
                                    "选取指定文件夹",
                                    "/")
        self.filePathlineEdit.setText(str(get_directory_path))

        # get_filename_path, ok = QFileDialog.getOpenFileName(self,
        #                             "选取单个文件",
        #                            "C:/",
        #                             "All Files (*);;Text Files (*.txt)")
        # if ok:
        #     self.filePathlineEdit.setText(str(get_filename_path))
        #
        # get_filenames_path, ok = QFileDialog.getOpenFileNames(self,
        #                             "选取多个文件",
        #                            "C:/",
        #                             "All Files (*);;Text Files (*.txt)")
        # if ok:
        #     self.filePathlineEdit.setText(str(' '.join(get_filenames_path)))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWin = MyMainForm()
    myWin.show()
    sys.exit(app.exec_())