# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'SqliteManageUI.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_SqliteManage(object):
    def setupUi(self, SqliteManage):
        SqliteManage.setObjectName("SqliteManage")
        SqliteManage.resize(922, 769)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(SqliteManage)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.pushButton_newdb = QtWidgets.QPushButton(SqliteManage)
        self.pushButton_newdb.setObjectName("pushButton_newdb")
        self.horizontalLayout.addWidget(self.pushButton_newdb)
        self.pushButton_opendb = QtWidgets.QPushButton(SqliteManage)
        self.pushButton_opendb.setObjectName("pushButton_opendb")
        self.horizontalLayout.addWidget(self.pushButton_opendb)
        self.pushButton_writeupdate = QtWidgets.QPushButton(SqliteManage)
        self.pushButton_writeupdate.setObjectName("pushButton_writeupdate")
        self.horizontalLayout.addWidget(self.pushButton_writeupdate)
        self.pushButton_rollbackupdate = QtWidgets.QPushButton(SqliteManage)
        self.pushButton_rollbackupdate.setObjectName("pushButton_rollbackupdate")
        self.horizontalLayout.addWidget(self.pushButton_rollbackupdate)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.tabWidget = QtWidgets.QTabWidget(SqliteManage)
        self.tabWidget.setObjectName("tabWidget")
        self.tab_database_structure = QtWidgets.QWidget()
        self.tab_database_structure.setObjectName("tab_database_structure")
        self.verticalLayoutWidget_2 = QtWidgets.QWidget(self.tab_database_structure)
        self.verticalLayoutWidget_2.setGeometry(QtCore.QRect(20, 12, 861, 661))
        self.verticalLayoutWidget_2.setObjectName("verticalLayoutWidget_2")
        self.verticalLayout_datastructure = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_2)
        self.verticalLayout_datastructure.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_datastructure.setObjectName("verticalLayout_datastructure")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.pushButton_create_database = QtWidgets.QPushButton(self.verticalLayoutWidget_2)
        self.pushButton_create_database.setObjectName("pushButton_create_database")
        self.horizontalLayout_2.addWidget(self.pushButton_create_database)
        self.pushButton_create_index = QtWidgets.QPushButton(self.verticalLayoutWidget_2)
        self.pushButton_create_index.setObjectName("pushButton_create_index")
        self.horizontalLayout_2.addWidget(self.pushButton_create_index)
        self.pushButton_repair_table = QtWidgets.QPushButton(self.verticalLayoutWidget_2)
        self.pushButton_repair_table.setObjectName("pushButton_repair_table")
        self.horizontalLayout_2.addWidget(self.pushButton_repair_table)
        self.pushButton_delete_table = QtWidgets.QPushButton(self.verticalLayoutWidget_2)
        self.pushButton_delete_table.setObjectName("pushButton_delete_table")
        self.horizontalLayout_2.addWidget(self.pushButton_delete_table)
        self.verticalLayout_datastructure.addLayout(self.horizontalLayout_2)
        self.treeWidget_data_structure = QtWidgets.QTreeWidget(self.verticalLayoutWidget_2)
        self.treeWidget_data_structure.setObjectName("treeWidget_data_structure")
        self.treeWidget_data_structure.headerItem().setText(0, "1")
        self.verticalLayout_datastructure.addWidget(self.treeWidget_data_structure)
        self.tabWidget.addTab(self.tab_database_structure, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.verticalLayoutWidget_3 = QtWidgets.QWidget(self.tab_2)
        self.verticalLayoutWidget_3.setGeometry(QtCore.QRect(20, 10, 751, 591))
        self.verticalLayoutWidget_3.setObjectName("verticalLayoutWidget_3")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_3)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.label = QtWidgets.QLabel(self.verticalLayoutWidget_3)
        self.label.setObjectName("label")
        self.horizontalLayout_5.addWidget(self.label)
        self.comboBox = QtWidgets.QComboBox(self.verticalLayoutWidget_3)
        self.comboBox.setObjectName("comboBox")
        self.horizontalLayout_5.addWidget(self.comboBox)
        self.pushButton_2 = QtWidgets.QPushButton(self.verticalLayoutWidget_3)
        self.pushButton_2.setObjectName("pushButton_2")
        self.horizontalLayout_5.addWidget(self.pushButton_2)
        self.pushButton_3 = QtWidgets.QPushButton(self.verticalLayoutWidget_3)
        self.pushButton_3.setObjectName("pushButton_3")
        self.horizontalLayout_5.addWidget(self.pushButton_3)
        self.pushButton = QtWidgets.QPushButton(self.verticalLayoutWidget_3)
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout_5.addWidget(self.pushButton)
        self.verticalLayout_3.addLayout(self.horizontalLayout_5)
        self.tableWidget = QtWidgets.QTableWidget(self.verticalLayoutWidget_3)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)
        self.verticalLayout_3.addWidget(self.tableWidget)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.pushButton_5 = QtWidgets.QPushButton(self.verticalLayoutWidget_3)
        self.pushButton_5.setObjectName("pushButton_5")
        self.horizontalLayout_4.addWidget(self.pushButton_5)
        self.pushButton_6 = QtWidgets.QPushButton(self.verticalLayoutWidget_3)
        self.pushButton_6.setObjectName("pushButton_6")
        self.horizontalLayout_4.addWidget(self.pushButton_6)
        self.label_2 = QtWidgets.QLabel(self.verticalLayoutWidget_3)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_4.addWidget(self.label_2)
        self.pushButton_7 = QtWidgets.QPushButton(self.verticalLayoutWidget_3)
        self.pushButton_7.setObjectName("pushButton_7")
        self.horizontalLayout_4.addWidget(self.pushButton_7)
        self.pushButton_8 = QtWidgets.QPushButton(self.verticalLayoutWidget_3)
        self.pushButton_8.setObjectName("pushButton_8")
        self.horizontalLayout_4.addWidget(self.pushButton_8)
        self.pushButton_4 = QtWidgets.QPushButton(self.verticalLayoutWidget_3)
        self.pushButton_4.setObjectName("pushButton_4")
        self.horizontalLayout_4.addWidget(self.pushButton_4)
        self.lineEdit = QtWidgets.QLineEdit(self.verticalLayoutWidget_3)
        self.lineEdit.setObjectName("lineEdit")
        self.horizontalLayout_4.addWidget(self.lineEdit)
        self.verticalLayout_3.addLayout(self.horizontalLayout_4)
        self.tabWidget.addTab(self.tab_2, "")
        self.tab_3 = QtWidgets.QWidget()
        self.tab_3.setObjectName("tab_3")
        self.tabWidget.addTab(self.tab_3, "")
        self.verticalLayout.addWidget(self.tabWidget)
        self.horizontalLayout_3.addLayout(self.verticalLayout)

        self.retranslateUi(SqliteManage)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(SqliteManage)

    def retranslateUi(self, SqliteManage):
        _translate = QtCore.QCoreApplication.translate
        SqliteManage.setWindowTitle(_translate("SqliteManage", "Form"))
        self.pushButton_newdb.setText(_translate("SqliteManage", "新建数据库"))
        self.pushButton_opendb.setText(_translate("SqliteManage", "打开数据库"))
        self.pushButton_writeupdate.setText(_translate("SqliteManage", "写入更改"))
        self.pushButton_rollbackupdate.setText(_translate("SqliteManage", "倒退更改"))
        self.pushButton_create_database.setText(_translate("SqliteManage", "创建表"))
        self.pushButton_create_index.setText(_translate("SqliteManage", "创建索引"))
        self.pushButton_repair_table.setText(_translate("SqliteManage", "修改表"))
        self.pushButton_delete_table.setText(_translate("SqliteManage", "删除表"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_database_structure), _translate("SqliteManage", "数据库结构"))
        self.label.setText(_translate("SqliteManage", "表"))
        self.pushButton_2.setText(_translate("SqliteManage", "刷新"))
        self.pushButton_3.setText(_translate("SqliteManage", "新建记录"))
        self.pushButton.setText(_translate("SqliteManage", "删除记录"))
        self.pushButton_5.setText(_translate("SqliteManage", "第一页"))
        self.pushButton_6.setText(_translate("SqliteManage", " 上一页"))
        self.label_2.setText(_translate("SqliteManage", "0 - 0 / 0"))
        self.pushButton_7.setText(_translate("SqliteManage", "下一页"))
        self.pushButton_8.setText(_translate("SqliteManage", "最后一页"))
        self.pushButton_4.setText(_translate("SqliteManage", "转到"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("SqliteManage", "浏览数据"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), _translate("SqliteManage", "执行SQL"))

