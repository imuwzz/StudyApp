# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'AddPictureForm.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_AddPictureForm(object):
    def setupUi(self, AddPictureForm):
        AddPictureForm.setObjectName("AddPictureForm")
        AddPictureForm.resize(660, 471)
        self.groupBox = QtWidgets.QGroupBox(AddPictureForm)
        self.groupBox.setGeometry(QtCore.QRect(20, 10, 621, 401))
        self.groupBox.setObjectName("groupBox")
        self.graphicsView_da1 = QtWidgets.QGraphicsView(self.groupBox)
        self.graphicsView_da1.setGeometry(QtCore.QRect(10, 20, 601, 371))
        self.graphicsView_da1.setObjectName("graphicsView_da1")
        self.pushButton_answer_zoomin_1 = QtWidgets.QPushButton(AddPictureForm)
        self.pushButton_answer_zoomin_1.setGeometry(QtCore.QRect(40, 420, 21, 21))
        self.pushButton_answer_zoomin_1.setObjectName("pushButton_answer_zoomin_1")
        self.toolButton_da1 = QtWidgets.QToolButton(AddPictureForm)
        self.toolButton_da1.setGeometry(QtCore.QRect(610, 420, 31, 21))
        self.toolButton_da1.setObjectName("toolButton_da1")
        self.pushButton_answer_zoomout_1 = QtWidgets.QPushButton(AddPictureForm)
        self.pushButton_answer_zoomout_1.setGeometry(QtCore.QRect(20, 420, 21, 21))
        self.pushButton_answer_zoomout_1.setObjectName("pushButton_answer_zoomout_1")

        self.retranslateUi(AddPictureForm)
        QtCore.QMetaObject.connectSlotsByName(AddPictureForm)

    def retranslateUi(self, AddPictureForm):
        _translate = QtCore.QCoreApplication.translate
        AddPictureForm.setWindowTitle(_translate("AddPictureForm", "Form"))
        self.groupBox.setTitle(_translate("AddPictureForm", "GroupBox"))
        self.pushButton_answer_zoomin_1.setText(_translate("AddPictureForm", "-"))
        self.toolButton_da1.setText(_translate("AddPictureForm", "..."))
        self.pushButton_answer_zoomout_1.setText(_translate("AddPictureForm", "+"))

