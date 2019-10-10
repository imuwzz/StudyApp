from PyQt5.QtGui import  QPixmap
from PyQt5.QtWidgets import *
from DBUtil import *
from PyQt5.QtGui import QIcon, QBrush, QColor,QCursor
from PyQt5.QtCore import Qt
import StringUtil
from FieldBuildForm import *
class TableBuildForm(QWidget):
    def __init__(self):
        super(TableBuildForm,self).__init__()
        self.initUi()
    def initUi(self):
        # 获取显示器分辨率
        self.desktop = QApplication.desktop()
        self.screenRect = self.desktop.screenGeometry()
        self.height = self.screenRect.height()
        self.width = self.screenRect.width()
        self.resize(self.width, self.height)
        self.setWindowTitle("数据表定义")

        mainLayout=QHBoxLayout()
        centerLayout=QVBoxLayout()
        rightLayout=QVBoxLayout()

        mainLayout.addLayout(centerLayout)
        mainLayout.addLayout(rightLayout)
        self.setLayout(mainLayout)

        centerTopLayout=QHBoxLayout()
        centerCenterLayout=QVBoxLayout()
        centerBottomLayout=QHBoxLayout()

        centerLayout.addLayout(centerTopLayout)
        centerLayout.addLayout(centerCenterLayout)
        centerLayout.addLayout(centerBottomLayout)

        zlkmcLabel=QLabel("资料库名称")
        self.zlkmcLineEdit=QLineEdit()
        bmcLabel=QLabel('数据表名称')
        self.bmcLineEdit=QLineEdit()
        bjxLabel=QLabel('内部名称')
        self.bjxLineText=QLineEdit()

        centerTopLayout.addWidget(zlkmcLabel)
        centerTopLayout.addWidget(self.zlkmcLineEdit)
        centerTopLayout.addWidget(bmcLabel)
        centerTopLayout.addWidget(self.bmcLineEdit)
        centerTopLayout.addWidget(bjxLabel)
        centerTopLayout.addWidget(self.bjxLineText)

        self.dataTableWidget = QTableWidget()
        centerCenterLayout.addWidget(self.dataTableWidget)

        self.dataTableWidget.setColumnCount(7)
        self.dataTableWidget.setHorizontalHeaderLabels(['数据项名称', '字段名称', '数据类型', '数据大小','数据来源','主键','是否为空'])
        self.dataTableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.dataTableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.dataTableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)

        centerCenterLayout.addWidget(self.dataTableWidget)

        testTableExistButton=QPushButton("数据表检测")
        reBuildTabelButton=QPushButton("替换数据表")
        addTableButton=QPushButton("添加数据表")
        replaceTableButton=QPushButton("替换数据表")

        centerBottomLayout.addWidget(testTableExistButton)
        centerBottomLayout.addWidget(reBuildTabelButton)
        centerBottomLayout.addWidget(addTableButton)
        centerBottomLayout.addWidget(replaceTableButton)

        self.m_db = DBUtil()
        self.dataTableWidget.setContextMenuPolicy(Qt.CustomContextMenu)
        self.dataTableWidget.customContextMenuRequested.connect(self.GenerateRightMenu)
        self.fieldBuildForm=FieldBuildForm()
        self.fieldBuildForm.AddButton.clicked.connect(self.EditTableRow)
        testTableExistButton.clicked.connect(self.TestTableExist)
        reBuildTabelButton.clicked.connect(self.ReBuildTable)
        addTableButton.clicked.connect(self.AddTable)
        replaceTableButton.clicked.connect(self.ReplaceTable)
    def table_init(self,tbid,tbmc,tbjx):
        self.tbid=tbid
        self.tbmc=tbmc
        self.tbjx=tbjx
        self.bmcLineEdit.setText(tbmc)
        self.bjxLineText.setText(tbjx)
        #读取数据表信息
        field_info=self.m_db.GetFieldValueToStrGroupsFromDb("ZDMC,MCJX,ZDLX,ZDDX,KZLX","XTGLK.ZLFL_MSFF_FIELD","where TBID='"+self.tbid+"'")
        if field_info!=None:
            if len(field_info[0])>0:
                self.dataTableWidget.setRowCount(len(field_info[0]))
                for index in range(0,len(field_info[0])):
                    zdmc=field_info[0][index]
                    mcjx=field_info[1][index]
                    zdlx=field_info[2][index]
                    zddx=str(field_info[3][index])
                    kzlx=field_info[4][index]

                    if kzlx=='0':
                        kzlx="0-用户输入"
                    elif kzlx=='1':
                        kzlx="1-用户选择"
                    elif kzlx=='2':
                        kzlx="2-系统生成"
                    elif kzlx=='3':
                        kzlx="3-系统默认"
                    else:
                        kzlx=""

                    zjs=self.m_db.GetFieldValueToStrListFromDb("ZDMC","XTGLK.ZLFL_MSFF_FIELD_KEY","where TBID='"+self.tbid+"'")
                    zj=''
                    if len(zjs)>0:
                        if zjs.index(mcjx)>=0:
                            zj="主键"
                        else:
                            zj="非主键"
                    else:
                        zj="非主键"

                    sfwk=self.m_db.GetFieldValueToSingleStrFromDb("SFWK","XTGLK.ZLFL_MSFF_FIELD_INFO","where TBID='"+self.tbid+"' and ZDMC='"+mcjx+"'")
                    if sfwk=="0":
                        sfwk="可以为空"
                    else:
                        sfwk="不能为空"

                    newitem = QTableWidgetItem(zdmc)
                    self.dataTableWidget.setItem(index, 0, newitem)
                    newitem = QTableWidgetItem(mcjx)
                    self.dataTableWidget.setItem(index, 1, newitem)
                    newitem = QTableWidgetItem(zdlx)
                    self.dataTableWidget.setItem(index, 2, newitem)
                    newitem = QTableWidgetItem(zddx)
                    self.dataTableWidget.setItem(index, 3, newitem)
                    newitem = QTableWidgetItem(kzlx)
                    self.dataTableWidget.setItem(index, 4, newitem)
                    newitem = QTableWidgetItem(zj)
                    self.dataTableWidget.setItem(index, 5, newitem)
                    newitem = QTableWidgetItem(sfwk)
                    self.dataTableWidget.setItem(index, 6, newitem)
    def GenerateRightMenu(self,pos):
        menu=QMenu()
        editItem=menu.addAction(u'编辑')
        preInsertItem=menu.addAction(u'前置插入')
        backInsertItem=menu.addAction(u'后置插入')
        deleteItem=menu.addAction(u'删除数据项')
        clearItem = menu.addAction(u'清除数据项')
        deleteMrItem = menu.addAction(u'删除默认数据项')

        action=menu.exec_(QCursor.pos())
        if action==editItem:
            self.ShowEditItemForm()
        elif action==preInsertItem:
            pass
        elif action==backInsertItem:
            pass
        elif action==deleteItem:
            pass
        elif action==clearItem:
            pass
        elif action==deleteMrItem:
            pass
    def ShowEditItemForm(self):
        selectedRow = self.dataTableWidget.currentIndex().row()
        if selectedRow!=None:
            zdmc = self.dataTableWidget.item(selectedRow, 0).text()
            mcjx = self.dataTableWidget.item(selectedRow, 1).text()
            zdlx = self.dataTableWidget.item(selectedRow, 2).text()
            zddx = self.dataTableWidget.item(selectedRow, 3).text()
            kzlx = self.dataTableWidget.item(selectedRow, 4).text()
            zj = self.dataTableWidget.item(selectedRow, 5).text()
            sfwk = self.dataTableWidget.item(selectedRow, 6).text()
            self.fieldBuildForm.fieldInit(zdmc,mcjx,zdlx,zddx,kzlx,zj,sfwk)
            self.fieldBuildForm.setWindowModality(Qt.ApplicationModal)
            self.fieldBuildForm.show()
    def EditTableRow(self):
        self.fieldinfo=[self.fieldBuildForm.zdmcLineEdit.text(),self.fieldBuildForm.mcjxLineEdit.text(),self.fieldBuildForm.zdlxComboBox.currentText(),self.fieldBuildForm.zddxComboBox.currentText(),self.fieldBuildForm.kzlxComboBox.currentText(),self.fieldBuildForm.zjComboBox.currentText(),self.fieldBuildForm.sfwkComboBox.currentText()]
        self.fieldBuildForm.hide()
        selectedRow = self.dataTableWidget.currentIndex().row()
        if selectedRow!=None:
            for index in range(0,len(self.fieldinfo)):
                newitem = QTableWidgetItem(self.fieldinfo[index])
                self.dataTableWidget.setItem(selectedRow,index,newitem)

    def TestTableExist(self):
        tbinfos=self.tbjx.split('.')
        bExistTable=self.m_db.TestDataExist("select count(*) from dba_tables where Owner='"+tbinfos[0]+"' and table_name='"+tbinfos[1]+"'")
        if bExistTable>0:
            QMessageBox.information(self, "数据表检测", "数据表存在！", QMessageBox.Yes)
        else:
            QMessageBox.information(self, "数据表检测", "数据表存在！", QMessageBox.Yes)
    def ReBuildTable(self):
        pass
    def AddTable(self):
        pass
    def ReplaceTable(self):
        pass

