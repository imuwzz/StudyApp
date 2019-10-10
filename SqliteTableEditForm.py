import sys
from PyQt5.QtGui import  QPixmap
from PyQt5.QtWidgets import *
from DBUtil import *
from PyQt5.QtGui import QIcon, QBrush, QColor,QCursor
from PyQt5.QtCore import Qt
from SqliteTableEditUI import Ui_SqliteTableEdit
from SqliteUtil import *

class SqliteTableEditForm(Ui_SqliteTableEdit,QWidget):
    def __init__(self,parent=None):
        super(SqliteTableEditForm, self).__init__(parent)
        self.setupUi(self)
        self.setWindowTitle("Sqlite数据表管理")

        #self.tab_database_structure.setLayout(self.verticalLayout_datastructure)
        #
        #self.treeWidget_data_structure.setColumnCount(3)
        #self.treeWidget_data_structure.setHeaderLabels(['名称', '类型', '架构'])
        #self.treeWidget_data_structure.setColumnWidth(0, 400)

        #self.pushButton_newdb.clicked.connect(self.NewDB)
        #self.pushButton_opendb.clicked.connect(self.OpenDB)
        #self.pushButton_create_database.clicked.connect(self.CreateTable)

        #创建字段列表
        self.tableWidget_field.setColumnCount(9)
        self.tableWidget_field.setHorizontalHeaderLabels(['名称','类型','非空','主键','值自增','值唯一','默认值','检查','外键'])
        self.tableWidget_field.setColumnWidth(8,200)
        self.pushButton_addfield.clicked.connect(self.AddField)
        self.lineEdit_tablename.textChanged.connect(self.TableNameChanged)
        self.treeWidget_sql.clear()
        self.treeWidget_sql.setColumnCount(1)
        self.treeWidget_sql.setHeaderHidden(True)
        self.root=QTreeWidgetItem(self.treeWidget_sql)
        self.root.setText(0,'CREATE TABLE \'\' (')

        endroot=QTreeWidgetItem(self.treeWidget_sql)
        endroot.setText(0,');')
        self.primaryKeyNode=None
        self.autoincreMentCheckBox=None
        self.primeKeyCheckBoxes=[]
    def AddField(self):
        fieldCount=self.tableWidget_field.rowCount()
        self.tableWidget_field.setRowCount(fieldCount+1)
        fieldname="Field"+str(fieldCount+1)
        newItem=QTableWidgetItem(fieldname)
        if self.primaryKeyNode!=None:
            index=self.tableWidget_field.indexFromItem(self.primaryKeyNode)
            self.tableWidget_field.setItem(fieldCount,0,newItem)
        fieldtypeComboBox = QComboBox()
        fieldtypeComboBox.addItems(['INTEGER', 'TEXT', 'BLOB', 'REAL', 'NUMERIC'])
        fieldtypeComboBox.setStyleSheet("QComboBox{margin:3px};")


        checkBox_null = QCheckBox()
        checkBox_null.setStyleSheet("QCheckBox{margin:3px};")
        checkBox_pk = QCheckBox()
        checkBox_pk.setObjectName(fieldname)
        checkBox_pk.setStyleSheet("QCheckBox{margin:3px};")
        checkBox_ai = QCheckBox()
        checkBox_ai.setStyleSheet("QCheckBox{margin:3px};")
        checkBox_unique = QCheckBox()
        checkBox_unique.setStyleSheet("QCheckBox{margin:3px};")
        checkBox_pk.objectName()


        self.tableWidget_field.setCellWidget(fieldCount,1,fieldtypeComboBox)
        self.tableWidget_field.setCellWidget(fieldCount, 2, checkBox_null)
        self.tableWidget_field.setCellWidget(fieldCount, 3, checkBox_pk)
        self.tableWidget_field.setCellWidget(fieldCount, 4, checkBox_ai)
        self.tableWidget_field.setCellWidget(fieldCount, 5, checkBox_unique)

        fieldnode=QTreeWidgetItem(self.root)
        fieldnode.setText(0,fieldname+" INTEGER,")

        self.tableWidget_field.itemChanged.connect(lambda: self.FieldNameChanged(fieldnode, fieldtypeComboBox,checkBox_null,checkBox_pk,checkBox_ai,checkBox_unique))
        fieldtypeComboBox.currentIndexChanged.connect(lambda: self.FieldTypeChanged(fieldnode, fieldtypeComboBox,checkBox_null,checkBox_pk,checkBox_ai,checkBox_unique))
        checkBox_null.stateChanged.connect(lambda: self.FieldNameChanged(fieldnode, fieldtypeComboBox,checkBox_null,checkBox_pk,checkBox_ai,checkBox_unique))
        checkBox_pk.stateChanged.connect(lambda: self.PrimaryKeyChanged(fieldnode, fieldtypeComboBox, checkBox_null, checkBox_pk,checkBox_ai, checkBox_unique))
        checkBox_ai.stateChanged.connect(lambda: self.AutoIncreMentChanged(fieldnode, fieldtypeComboBox, checkBox_null, checkBox_pk,checkBox_ai, checkBox_unique))
        checkBox_unique.stateChanged.connect(lambda: self.FieldNameChanged( fieldnode, fieldtypeComboBox, checkBox_null, checkBox_pk,checkBox_ai, checkBox_unique))

        self.treeWidget_sql.expandAll()

    def TableNameChanged(self):
        tablename=self.lineEdit_tablename.text()
        self.root.setText(0,"CREATE TABLE '"+tablename+"' (")
    def FieldNameChanged(self,fieldnode, fieldtypeComboBox,checkBox_null,checkBox_pk,checkBox_ai,checkBox_uniqu):
        try:
            fieldtype = fieldtypeComboBox.currentText()
            selectedRow = self.tableWidget_field.currentIndex().row()
            if selectedRow == -1:
                return
            fieldname=self.tableWidget_field.item(selectedRow,0).text()
            mrz=''
            if self.tableWidget_field.item(selectedRow,6)!=None:
                mrz=self.tableWidget_field.item(selectedRow,6).text()
            fieldinfo = fieldname + " " + fieldtype
            if checkBox_null.isChecked():
                fieldinfo+=" NOT NULL "
            if checkBox_ai.isChecked():
                fieldinfo+=" PRIMARY KEY AUTOINCREMENT "
            else:
                if checkBox_pk.isChecked():
                    #创建PrimaryKey节点，并修改其内容
                    if self.primaryKeyNode==None:
                        self.primaryKeyNode=QTreeWidgetItem(self.root)
                        self.primaryKeyNode.setText(0,"PRIMARY KEY ('"+fieldname+"')")
                    else:
                        #修改标题
                        if len(self.primeKeyCheckBoxes) >1:
                            primekey_info=""
                            for checkbox in self.primeKeyCheckBoxes:
                                objname=checkbox.objectName()
                                if primekey_info=='':
                                    primekey_info+="'"+objname+"'"
                                else:
                                    primekey_info+=",'"+objname+"'"
                            primekey_info="PRIMARY KEY ("+primekey_info+")"
                            self.primaryKeyNode.setText(0, primekey_info)
                        elif len(self.primeKeyCheckBoxes) > 0:
                            self.primaryKeyNode.setText(0, "PRIMARY KEY ('" + fieldname + "')")
                else:
                    #没有选中主键
                    if len(self.primeKeyCheckBoxes)==0:
                        if self.primaryKeyNode!=None:
                            #删除当前主键节点
                            self.root.removeChild(self.primaryKeyNode)
                            self.primaryKeyNode=None
                        else:
                            pass
                    elif len(self.primeKeyCheckBoxes)==1:
                        primarykey = self.primeKeyCheckBoxes[0].objectName()
                        if self.primaryKeyNode == None:
                            self.primaryKeyNode = QTreeWidgetItem(self.root)
                            self.primaryKeyNode.setText(0, "PRIMARY KEY ('" + primarykey + "')")
                        else:
                            # 修改标题
                            self.primaryKeyNode.setText(0, "PRIMARY KEY ('" + fieldname + "')")
                    elif len(self.primeKeyCheckBoxes) > 1:
                        primekey_info = ""
                        for checkbox in self.primeKeyCheckBoxes:
                            objname = checkbox.objectName()
                            if primekey_info == '':
                                primekey_info += "'" + objname + "'"
                            else:
                                primekey_info += ",'" + objname + "'"
                        primekey_info = "PRIMARY KEY (" + primekey_info + ")"
                        self.primaryKeyNode.setText(0, primekey_info)



            #处理默认值
            if mrz!='':
                if fieldtype=='TEXT':
                    fieldinfo+=" DEFAULT '"+mrz+"'"
                elif fieldtype=='INTEGER' or fieldtype=='REAL' or fieldtype=='NUMERIC':
                    fieldinfo+='DEFAULT '+mrz

            if checkBox_uniqu.isChecked():
                fieldinfo+=" UNIQUE "

            fieldinfo+=","
            fieldnode.setText(0,fieldinfo)
        except Exception as e:
            print("更新字段信息发生异常：",e)
    def FieldTypeChanged(self, fieldnode, fieldtypeComboBox,checkBox_null,checkBox_pk,checkBox_ai,checkBox_uniqu):
        try:
            #只有整型可作为自增类型
            fieldtype=fieldtypeComboBox.currentText()
            if fieldtype!='INTEGER':
                checkBox_ai.setChecked(False)
            self.FieldNameChanged(fieldnode, fieldtypeComboBox,checkBox_null,checkBox_pk,checkBox_ai,checkBox_uniqu)
        except Exception as e:
            print("字段类型变化时发生异常：",e)
    def PrimaryKeyChanged(self, fieldnode, fieldtypeComboBox,checkBox_null,checkBox_pk,checkBox_ai,checkBox_uniqu):
        try:
            if checkBox_ai.isChecked():
                checkBox_pk.setChecked(True)
                return

            selectedRow = self.tableWidget_field.currentIndex().row()
            if selectedRow == -1:
                return
            fieldname = self.tableWidget_field.item(selectedRow, 0).text()
            if checkBox_pk.isChecked():
               found=False
               for pkCB in self.primeKeyCheckBoxes:
                   pkName=pkCB.objectName()
                   if pkName==fieldname:
                       found=True
                       break
                   else:
                       pass
               if found==False:
                   self.primeKeyCheckBoxes.append(checkBox_pk)
            else:
                for pkCB in self.primeKeyCheckBoxes:
                    if pkCB.objectName()==fieldname:
                        self.primeKeyCheckBoxes.remove(pkCB)
                        break
                if self.autoincreMentCheckBox != None:
                    self.autoincreMentCheckBox.setChecked(False)
                    self.autoincreMentCheckBox = None
            #主键个数为1，可设置自增
            if len(self.primeKeyCheckBoxes)==1:
                pass

            #主键个数>1,不可自增
            # 取消值自增的状态
            elif len(self.primeKeyCheckBoxes)>1:
                if self.autoincreMentCheckBox != None:
                    self.autoincreMentCheckBox.setChecked(False)
                    self.autoincreMentCheckBox=None
            self.FieldNameChanged(fieldnode, fieldtypeComboBox, checkBox_null, checkBox_pk, checkBox_ai, checkBox_uniqu)
        except Exception as e:
            print("更新主键状态时发生异常：",e)
    def AutoIncreMentChanged(self, fieldnode, fieldtypeComboBox,checkBox_null,checkBox_pk,checkBox_ai,checkBox_uniqu):
        # 如果值递增，一定是整型，且默认主键
        try:
            if checkBox_ai.isChecked():
                #只能有一个字段为自增类型
                if self.autoincreMentCheckBox!=None:
                    self.autoincreMentCheckBox.setChecked(False)
                self.autoincreMentCheckBox=checkBox_ai
                for pkCB in self.primeKeyCheckBoxes:
                    pkCB.setChecked(False)
                self.primeKeyCheckBoxes.clear()
                self.primeKeyCheckBoxes.append(checkBox_pk)
                # 设置当前字段为主键
                checkBox_pk.setChecked(True)
                fieldtypeComboBox.setCurrentText('INTEGER')
                self.root.removeChild(self.primaryKeyNode)
                self.primaryKeyNode=None
            else:
                self.autoincreMentCheckBox = None
            self.FieldNameChanged(fieldnode, fieldtypeComboBox, checkBox_null, checkBox_pk, checkBox_ai, checkBox_uniqu)
        except Exception as e:
            print('值自增时发生错误：',e)

    def FieldInfoChanged(self,fieldname, fieldnode, fieldtypeComboBox,checkBox_null,checkBox_pk,checkBox_ai,checkBox_uniqu):

        #如果值递增，一定是整型，且默认主键
        if checkBox_ai.isChecked():
            #取消其他主键
            if len(self.primeKeyCheckBoxes)>0 and self.primeKeyCheckBoxes.index(checkBox_pk)<0:
                for checkBox in self.primeKeyCheckBoxes:
                    checkBox.setChecked(False)
            #设置当前字段为主键
            checkBox_pk.setChecked(True)
            #清理所有的其他键
            self.primeKeyCheckBoxes.clear()
            self.primeKeyCheckBoxes.append(checkBox_pk)

            fieldtypeComboBox.setCurrentText('INTEGER')
            #取消其他所有主键
            if self.primaryKeyNode!=None:
                self.root.removeChild(self.primaryKeyNode)
                self.primaryKeyNode=None
            #取消值自增的状态
            if self.autoincreMentCheckBox!=None:
                self.autoincreMentCheckBox.setChecked(False)
            self.autoincreMentCheckBox=checkBox_ai
        else:
            #不是自增型
            pass

        fieldtype = fieldtypeComboBox.currentText()
        fieldinfo = fieldname + " " + fieldtype
        if checkBox_null.isChecked():
            fieldinfo+=" NOT NULL "
        if checkBox_ai.isChecked():
            fieldinfo+=" PRIMARY KEY AUTOINCREMENT "
        else:
            if checkBox_pk.isChecked():
                #创建PrimaryKey节点，并修改其内容
                if self.primaryKeyNode==None:
                    self.primaryKeyNode=QTreeWidgetItem(self.root)
                    self.primaryKeyNode.setText(0,"PRIMARY KEY ('"+fieldname+"')")
                else:
                    #修改标题
                    if len(self.primeKeyCheckBoxes) >1:
                        primekey_info=""
                        for checkbox in self.primeKeyCheckBoxes:
                            objname=checkbox.objectName()
                            if primekey_info=='':
                                primekey_info+="'"+objname+"'"
                            else:
                                primekey_info+=",'"+objname+"'"
                        primekey_info="PRIMARY KEY ("+primekey_info+")"
                        self.primaryKeyNode.setText(0, primekey_info)
                    elif len(self.primeKeyCheckBoxes) > 0:
                        self.primaryKeyNode.setText(0, "PRIMARY KEY ('" + fieldname + "')")


        if checkBox_uniqu.isChecked():
            fieldinfo+=" UNIQUE "
        fieldinfo+=","
        fieldnode.setText(0,fieldinfo)
