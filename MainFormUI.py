# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'MainForm.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(974, 702)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(190, 70, 54, 12))
        self.label.setObjectName("label")
        self.styleComboBox = QtWidgets.QComboBox(self.centralwidget)
        self.styleComboBox.setGeometry(QtCore.QRect(250, 66, 171, 22))
        self.styleComboBox.setObjectName("styleComboBox")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 974, 23))
        self.menubar.setObjectName("menubar")
        self.menu = QtWidgets.QMenu(self.menubar)
        self.menu.setObjectName("menu")
        self.menu_2 = QtWidgets.QMenu(self.menubar)
        self.menu_2.setObjectName("menu_2")
        self.menu_3 = QtWidgets.QMenu(self.menubar)
        self.menu_3.setObjectName("menu_3")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.MenuItem_PaperEdit = QtWidgets.QAction(MainWindow)
        self.MenuItem_PaperEdit.setObjectName("MenuItem_PaperEdit")
        self.MenuItem_PaperManager = QtWidgets.QAction(MainWindow)
        self.MenuItem_PaperManager.setObjectName("MenuItem_PaperManager")
        self.MenuItem_DataClass = QtWidgets.QAction(MainWindow)
        self.MenuItem_DataClass.setObjectName("MenuItem_DataClass")
        self.actionSqlite = QtWidgets.QAction(MainWindow)
        self.actionSqlite.setObjectName("actionSqlite")
        self.menu.addAction(self.MenuItem_PaperEdit)
        self.menu.addAction(self.MenuItem_PaperManager)
        self.menu_3.addAction(self.MenuItem_DataClass)
        self.menu_3.addAction(self.actionSqlite)
        self.menubar.addAction(self.menu.menuAction())
        self.menubar.addAction(self.menu_2.menuAction())
        self.menubar.addAction(self.menu_3.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "窗口风格"))
        self.menu.setTitle(_translate("MainWindow", "题库管理"))
        self.menu_2.setTitle(_translate("MainWindow", "试卷管理"))
        self.menu_3.setTitle(_translate("MainWindow", "系统管理"))
        self.MenuItem_PaperEdit.setText(_translate("MainWindow", "试卷管理"))
        self.MenuItem_PaperManager.setText(_translate("MainWindow", "试题管理"))
        self.MenuItem_DataClass.setText(_translate("MainWindow", "数据分类"))
        self.actionSqlite.setText(_translate("MainWindow", "Sqlite数据库管理"))

