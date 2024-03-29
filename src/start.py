# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'start.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets

from src.ui import ApiMakerUi


class StartApp(QtWidgets.QWidget):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(400, 300)
        self.horizontalLayoutWidget = QtWidgets.QWidget(Form)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(10, 100, 371, 80))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.new = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.new.setObjectName("New")
        self.horizontalLayout.addWidget(self.new)
        self.open = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.open.setObjectName("Open")
        self.horizontalLayout.addWidget(self.open)
        self.exit = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.exit.setObjectName("Exit")
        self.horizontalLayout.addWidget(self.exit)
        self.open.clicked.connect(self.callOpen)
        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def callOpen(self):
        openFile = ApiMakerUi(self)
        openFile.show()
    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.new.setText(_translate("Form", "New"))
        self.open.setText(_translate("Form", "open"))
        self.exit.setText(_translate("Form", "exit"))
