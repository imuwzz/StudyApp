import sys
from PyQt5.QtGui import  QPixmap
from PyQt5.QtWidgets import *
from DBUtil import *
from PyQt5.QtGui import QIcon, QBrush, QColor,QCursor
from PyQt5.QtCore import Qt
from SqliteManageUI import Ui_SqliteManage
from SqliteUtil import *
from SqliteTableEditForm import *
class SqliteManageForm(Ui_SqliteManage,QWidget):
    def __init__(self,parent=None):
        super(SqliteManageForm, self).__init__(parent)
        self.setupUi(self)
        self.setWindowTitle("Sqlite数据库管理")

        self.tab_database_structure.setLayout(self.verticalLayout_datastructure)
        #
        self.treeWidget_data_structure.setColumnCount(3)
        self.treeWidget_data_structure.setHeaderLabels(['名称', '类型', '架构'])
        self.treeWidget_data_structure.setColumnWidth(0, 400)

        self.pushButton_newdb.clicked.connect(self.NewDB)
        self.pushButton_opendb.clicked.connect(self.OpenDB)
        self.pushButton_create_database.clicked.connect(self.CreateTable)
    def NewDB(self):
        fileName, ok = QFileDialog.getSaveFileName(None, "输入数据库名称", "","SQLite数据库文件 (*.db)")
        if fileName and ok:
            SqliteUtil.CreateDB(fileName)
    def OpenDB(self):
        try:
            fileName, filetype = QFileDialog.getOpenFileName(None, "打开数据库", "","SQLite数据库文件 (*.db)")
            if fileName:
                talbes=SqliteUtil.GetTablesInDB(fileName)
                self.treeWidget_data_structure.clear()
                root_table = QTreeWidgetItem(self.treeWidget_data_structure)
                root_table.setText(0, '表')
                root_table.setText(1, '')
                root_table.setText(2, '')
                self.treeWidget_data_structure.addTopLevelItem(root_table)
                for talbe in talbes:
                    child_table = QTreeWidgetItem(root_table)
                    child_table.setText(0, talbe[0])
                    child_table.setText(1, '')
                    child_table.setText(2, '')
        except Exception as e:
             print('读取数据库时发生错误',e)
    def CreateTable(self):
        self.sqliteTableEditForm=SqliteTableEditForm()
        self.sqliteTableEditForm.setLayout(self.sqliteTableEditForm.verticalLayout_main)
        self.sqliteTableEditForm.groupBox_table.setLayout(self.sqliteTableEditForm.horizontalLayout_table)
        self.sqliteTableEditForm.groupBox_field.setLayout(self.sqliteTableEditForm.verticalLayout_field)
        self.sqliteTableEditForm.groupBox_sql.setLayout(self.sqliteTableEditForm.verticalLayout_sql)
        self.sqliteTableEditForm.showMaximized()




