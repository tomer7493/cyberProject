# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'client_start.ui'
#
# Created by: PyQt5 UI code generator 5.15.7
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.

import res.client_start_res

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow,client):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(785, 621)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(400, 0, 381, 241))
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap(":/logo/client_imgs/logo-removebg-preview.png"))
        self.label.setObjectName("label")
        self.ip_input = QtWidgets.QLineEdit(self.centralwidget)
        self.ip_input.setGeometry(QtCore.QRect(190, 370, 421, 91))
        font = QtGui.QFont()
        font.setPointSize(36)
        self.ip_input.setFont(font)
        self.ip_input.setAutoFillBackground(False)
        self.ip_input.setInputMethodHints(QtCore.Qt.ImhNone)
        self.ip_input.setMaxLength(15)
        self.ip_input.setObjectName("ip_input")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(190, 320, 371, 41))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.done_button = QtWidgets.QPushButton(self.centralwidget)
        self.done_button.setGeometry(QtCore.QRect(190, 470, 421, 51))
        font = QtGui.QFont()
        font.setPointSize(35)
        font.setBold(True)
        font.setWeight(75)
        self.done_button.setFont(font)
        self.done_button.setObjectName("done_button")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 785, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        # client.ui_input(self.ip_input,self.done_button)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label_2.setText(_translate("MainWindow", "enter the server ip address:"))
        self.done_button.setText(_translate("MainWindow", "done"))
