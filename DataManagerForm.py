from PyQt5.QtGui import  QPixmap
from PyQt5.QtWidgets import *
from DBUtil import *
from PyQt5.QtGui import QIcon, QBrush, QColor,QCursor,QIntValidator
from PyQt5.QtCore import Qt
import StringUtil
from RowEditForm import *

class DataManagerForm(QWidget):
    def __init__(self):
        super(DataManagerForm,self).__init__()
        self.initUi()
    def initUi(self):
        # 获取显示器分辨率
        self.desktop = QApplication.desktop()
        self.screenRect = self.desktop.screenGeometry()
        self.height = self.screenRect.height()
        self.width = self.screenRect.width()
        self.resize(self.width, self.height)
        self.setWindowTitle("数据管理")

        mainLayout=QVBoxLayout()
        centerLayout=QVBoxLayout()
        self.bottomLayout=QHBoxLayout()
        mainLayout.addLayout(centerLayout)
        mainLayout.addLayout(self.bottomLayout)

        self.dataTableWidget = QTableWidget()
        centerLayout.addWidget(self.dataTableWidget)

        self.m_db=DBUtil()
        self.setLayout(mainLayout)

        self.dataTableWidget.setContextMenuPolicy(Qt.CustomContextMenu)
        self.dataTableWidget.customContextMenuRequested.connect(self.GenerateMenu)


    def data_init(self,tbid,tbmc,tbjx):
        self.tbid=tbid
        self.tbjx=tbjx
        self.tbmc=tbmc
        self.fieldnamelist=self.m_db.GetFieldValueToStrListFromDb("ZDMC","XTGLK.ZLFL_MSFF_FIELD","where TBID='"+tbid+"' and MCJX not in('FLID','MJ','SJLY','SJSJ','LRSJ') order by SXH")
        self.fieldlist=self.m_db.GetFieldValueToStrListFromDb("MCJX","XTGLK.ZLFL_MSFF_FIELD","where TBID='"+tbid+"' and MCJX not in('FLID','MJ','SJLY','SJSJ','LRSJ') order by SXH")
        self.field_kzlx_list=self.m_db.GetFieldValueToStrListFromDb("KZLX","XTGLK.ZLFL_MSFF_FIELD","where TBID='"+tbid+"' and MCJX not in('FLID','ID','MJ','SJLY','SJSJ','LRSJ') order by SXH")
        self.field_zdlx_list = self.m_db.GetFieldValueToStrListFromDb("ZDLX", "XTGLK.ZLFL_MSFF_FIELD", "where TBID='" + tbid + "' and MCJX not in('FLID','ID','MJ','SJLY','SJSJ','LRSJ') order by SXH")
        self.link_field_list=[]
        for fieldindex in range(0,len(self.fieldlist)):
            link_field=self.m_db.GetFieldValueToSingleStrFromDb('NBGLZD','XTGLK.ZLFL_MSFF_FIELD_INFO',"where TBID='" + tbid + "' and ZDMC='"+self.fieldlist[fieldindex]+"'")
            if link_field==None:
                link_field=''
            self.link_field_list.append(link_field)
        mrzinfo_list=self.m_db.GetFieldValueToStrGroupsFromDb('ZDMC,MRZ',"XTGLK.ZLFL_MSFF_FIELD_INFO", "where TBID='" + tbid + "'")
        self.mrzd_list=mrzinfo_list[0]
        self.mrz_list=mrzinfo_list[1]
        self.fieldvalue_list=[]
        for fieldindex in range(0,len(self.fieldlist)):
            self.fieldvalue_list.append('')
        for fieldindex in range(0,len(self.fieldlist)):
            fieldname=self.fieldlist[fieldindex]
            mrzd_index=self.mrzd_list.index(fieldname)
            if mrzd_index!=None:
                mrz=self.mrz_list[mrzd_index]
                if mrz!=None:
                    self.fieldvalue_list[fieldindex]=mrz

        fieldcount=len(self.fieldnamelist)
        self.dataTableWidget.setColumnCount(fieldcount)
        self.dataTableWidget.setHorizontalHeaderLabels(self.fieldnamelist)
        self.dataTableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.dataTableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.dataTableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)

        self.dataCount=self.m_db.GetRowCount("select * from "+tbjx)
        self.setWindowTitle(self.tbmc+"（共有"+str(self.dataCount)+"条记录）")
        self.rowcount_page=5
        self.page_count=self.dataCount//self.rowcount_page
        self.currentPageIndex=1
        page_rest=self.dataCount%self.rowcount_page
        if page_rest>0:
            self.page_count+=1
        self.page10_count=self.page_count//10
        page10_rest=self.page_count%10
        if page10_rest>0:
            self.page10_count+=1
        self.current_10PageIndex=1

        self.pageButton_forword=QPushButton(str("<<"))
        self.bottomLayout.addWidget(self.pageButton_forword)
        self.pageButton_forword.clicked.connect(lambda :self.readData(self.pageButton_forword))
        self.pageButton_forword.setFixedWidth(30)

        self.pageButton_first=QPushButton(str("|<"))
        self.bottomLayout.addWidget(self.pageButton_first)
        self.pageButton_first.clicked.connect(lambda :self.readData(self.pageButton_first))
        self.pageButton_first.setFixedWidth(30)

        self.pageButton_before=QPushButton(str("<"))
        self.bottomLayout.addWidget(self.pageButton_before)
        self.pageButton_before.clicked.connect(lambda :self.readData(self.pageButton_before))
        self.pageButton_before.setFixedWidth(30)


        self.pageButton1=QPushButton(str("1"))
        self.bottomLayout.addWidget(self.pageButton1)
        self.pageButton1.clicked.connect(lambda :self.readData(self.pageButton1))
        self.pageButton1.setFixedWidth(30)

        self.pageButton2=QPushButton(str("2"))
        self.bottomLayout.addWidget(self.pageButton2)
        self.pageButton2.clicked.connect(lambda :self.readData(self.pageButton2))
        self.pageButton2.setFixedWidth(30)

        self.pageButton3=QPushButton(str("3"))
        self.bottomLayout.addWidget(self.pageButton3)
        self.pageButton3.clicked.connect(lambda :self.readData(self.pageButton3))
        self.pageButton3.setFixedWidth(30)

        self.pageButton4=QPushButton(str("4"))
        self.bottomLayout.addWidget(self.pageButton4)
        self.pageButton4.clicked.connect(lambda :self.readData(self.pageButton4))
        self.pageButton4.setFixedWidth(30)

        self.pageButton5=QPushButton(str("5"))
        self.bottomLayout.addWidget(self.pageButton5)
        self.pageButton5.clicked.connect(lambda :self.readData(self.pageButton5))
        self.pageButton5.setFixedWidth(30)

        self.pageButton6=QPushButton(str("6"))
        self.bottomLayout.addWidget(self.pageButton6)
        self.pageButton6.clicked.connect(lambda :self.readData(self.pageButton6))
        self.pageButton6.setFixedWidth(30)

        self.pageButton7=QPushButton(str("7"))
        self.bottomLayout.addWidget(self.pageButton7)
        self.pageButton7.clicked.connect(lambda :self.readData(self.pageButton7))
        self.pageButton7.setFixedWidth(30)

        self.pageButton8=QPushButton(str("8"))
        self.bottomLayout.addWidget(self.pageButton8)
        self.pageButton8.clicked.connect(lambda :self.readData(self.pageButton8))
        self.pageButton8.setFixedWidth(30)

        self.pageButton9=QPushButton(str("9"))
        self.bottomLayout.addWidget(self.pageButton9)
        self.pageButton9.clicked.connect(lambda :self.readData(self.pageButton9))
        self.pageButton9.setFixedWidth(30)

        self.pageButton10=QPushButton(str("10"))
        self.bottomLayout.addWidget(self.pageButton10)
        self.pageButton10.clicked.connect(lambda :self.readData(self.pageButton10))
        self.pageButton10.setFixedWidth(30)

        self.pageButton_next=QPushButton(str(">"))
        self.bottomLayout.addWidget(self.pageButton_next)
        self.pageButton_next.clicked.connect(lambda :self.readData(self.pageButton_next))
        self.pageButton_next.setFixedWidth(30)

        self.pageButton_end=QPushButton(str(">|"))
        self.bottomLayout.addWidget(self.pageButton_end)
        self.pageButton_end.clicked.connect(lambda :self.readData(self.pageButton_end))
        self.pageButton_end.setFixedWidth(30)

        self.pageButton_backword=QPushButton(str(">>"))
        self.bottomLayout.addWidget(self.pageButton_backword)
        self.pageButton_backword.clicked.connect(lambda :self.readData(self.pageButton_backword))
        self.pageButton_backword.setFixedWidth(30)

        self.pageButtons=[self.pageButton1,self.pageButton2,self.pageButton3,self.pageButton4,self.pageButton5,self.pageButton6,self.pageButton7,self.pageButton8,self.pageButton9,self.pageButton10]

        for page_index in range(0,11):
            if self.page_count>=page_index:
                self.pageButtons[page_index-1].setEnabled(1)
            else:
                self.pageButtons[page_index-1].setEnabled(0)

        perPageLabel=QLabel("每页")
        self.perPageLineEdit=QLineEdit()
        perPageRowLabel=QLabel("行")

        self.bottomLayout.addWidget(perPageLabel)
        self.bottomLayout.addWidget(self.perPageLineEdit)
        self.bottomLayout.addWidget(perPageRowLabel)
        self.perPageLineEdit.textChanged.connect(self.RowPerPageChanged)
        self.perPageLineEdit.setText('5')

        pIntValidator=QIntValidator(self)
        pIntValidator.setRange(1,100)
        self.perPageLineEdit.setValidator(pIntValidator)
        self.perPageLineEdit.setFixedWidth(40)


        whichPageLabel=QLabel("第")
        self.whichPageComboBox=QComboBox()
        whichPageRowLabel=QLabel("页")

        self.bottomLayout.addWidget(whichPageLabel)
        self.bottomLayout.addWidget(self.whichPageComboBox)
        self.bottomLayout.addWidget(whichPageRowLabel)
        self.whichPageComboBox.currentIndexChanged.connect(self.PageSelectChanged)

        for page in range(1,self.page_count+1):
            self.whichPageComboBox.addItem(str(page))

        pIntValidator=QIntValidator(self)
        pIntValidator.setRange(1,100)
        self.perPageLineEdit.setValidator(pIntValidator)
        self.perPageLineEdit.setFixedWidth(40)

        self.addRowButton=QPushButton("添加")
        self.delRowButton=QPushButton("删除")
        self.editRowButton=QPushButton("编辑")
        self.clearRowButton=QPushButton("清空")

        self.bottomLayout.addWidget(self.addRowButton)
        self.bottomLayout.addWidget(self.editRowButton)
        self.bottomLayout.addWidget(self.delRowButton)
        self.bottomLayout.addWidget(self.clearRowButton)

        self.addRowButton.clicked.connect(self.AddNewRow)
        self.editRowButton.clicked.connect(self.EditRow)
        self.delRowButton.clicked.connect(self.DelRow)
        self.clearRowButton.clicked.connect(self.ClearRows)



    def readData(self,btn):
        try:
            self.dataTableWidget.setRowCount(0)
            page=btn.text()
            #转到上一个10页
            if page=="<<":
                self.Go_Forward()
            elif page=="|<":
                self.Go_First()
            elif page=="<":
                if self.currentPageIndex>1:
                    self.currentPageIndex-=1
                    start_page=(self.current_10PageIndex-1)*10+1
                    end_page=self.current_10PageIndex*10
                    if self.currentPageIndex<start_page:
                        self.current_10PageIndex-=1
                        start_page=(self.current_10PageIndex-1)*10+1
                        end_page=self.current_10PageIndex*10
                        for page_index in range(start_page,end_page):
                            self.pageButtons[page_index-1].setText(str(page_index))
                        for page_index in range(0,11):
                            if self.page_count>=page_index:
                                self.pageButtons[page_index-1].setEnabled(1)
                            else:
                                self.pageButtons[page_index-1].setEnabled(0)
                    self.ReadDataInPage(str(self.currentPageIndex))
            elif page==">>":
                self.Go_Backward()
            elif page==">|":
                self.Go_Last()
            elif page==">":
                if self.currentPageIndex<self.page_count:
                    self.currentPageIndex+=1
                    start_page=(self.current_10PageIndex-1)*10+1
                    end_page=self.current_10PageIndex*10
                    if self.currentPageIndex>end_page:
                        self.current_10PageIndex+=1
                        start_page=(self.current_10PageIndex-1)*10+1
                        end_page=self.current_10PageIndex*10

                        for page_index in range(start_page,end_page):
                            self.pageButtons[page_index-1].setText(str(page_index))
                        for page_index in range(0,11):
                            if self.page_count>=page_index:
                                self.pageButtons[page_index-1].setEnabled(1)
                            else:
                                self.pageButtons[page_index-1].setEnabled(0)
                    self.ReadDataInPage(str(self.currentPageIndex))
            else:
                self.ReadDataInPage(page)
        except Exception as e:
            print("读取数据发生错误",e)
    def ReadDataInPage(self,page):
        iPage=int(page)
        self.currentPageIndex=iPage
        field=','.join(self.fieldlist)
        minrow=(iPage-1)*self.rowcount_page

        maxrow=iPage*self.rowcount_page
        fieldinfo=self.m_db.GetFieldValueToStrGroupsFromDbByRange(field,self.tbjx,"",minrow,maxrow)
        if fieldinfo!=None:
            if len(fieldinfo)>0:
                if len(fieldinfo[0])>0:
                    self.dataTableWidget.setRowCount(len(fieldinfo[0]))
                    for fieldvalueindex in range(0,len(fieldinfo[0])):
                        for fieldindex in range(0,len(self.fieldlist)):
                            fieldvalues=fieldinfo[fieldindex]
                            if len(fieldvalues)>0:
                                newitem=QTableWidgetItem(str(fieldvalues[fieldvalueindex]))
                                self.dataTableWidget.setItem(fieldvalueindex,fieldindex,newitem)

    def Go_Forward(self):
        try:
            if self.page_count<=10:
                    return
            else:
                if self.page10_count-self.current_10PageIndex>0:
                    self.current_10PageIndex+=1
                    start_page=(self.current_10PageIndex-1)*10+1
                    end_page=self.current_10PageIndex*10
                    for page_index in range(start_page,end_page):
                        self.pageButtons[page_index-1].setText(str(page_index))
                    for page_index in range(0,11):
                        if self.page_count>=page_index:
                            self.pageButtons[page_index-1].setEnabled(1)
                        else:
                            self.pageButtons[page_index-1].setEnabled(0)
                else:
                    return
        except Exception as e:
            print("向前翻页发生错误！")

    def Go_Backward(self):
        try:
            if self.page_count<=10:
                    return
            else:
                if self.current_10PageIndex>1:
                    self.current_10PageIndex-=1
                    start_page=(self.current_10PageIndex-1)*10+1
                    end_page=self.current_10PageIndex*10
                    for page_index in range(start_page,end_page):
                        self.pageButtons[page_index-1].setText(str(page_index))
                    for page_index in range(0,11):
                        if self.page_count>=page_index:
                            self.pageButtons[page_index-1].setEnabled(1)
                        else:
                            self.pageButtons[page_index-1].setEnabled(0)
                else:
                    return
        except Exception as e:
            print("向前翻页发生错误！")
    def Go_Last(self):
        self.ReadDataInPage(str(self.page_count))
        self.currentPageIndex=self.page_count
        self.current_10PageIndex=self.page10_count
        start_page=(self.current_10PageIndex-1)*10+1
        end_page=self.current_10PageIndex*10

        for page_index in range(start_page,end_page):
            self.pageButtons[page_index-1].setText(str(page_index))
        for page_index in range(0,11):
            if self.page_count>=page_index:
                self.pageButtons[page_index-1].setEnabled(1)
            else:
                self.pageButtons[page_index-1].setEnabled(0)
    def Go_First(self):
        self.ReadDataInPage("1")
        self.currentPageIndex=1
        self.current_10PageIndex=1
        start_page=(self.current_10PageIndex-1)*10+1
        end_page=self.current_10PageIndex*10

        for page_index in range(start_page,end_page):
            self.pageButtons[page_index-1].setText(str(page_index))
        for page_index in range(0,11):
            if self.page_count>=page_index:
                self.pageButtons[page_index-1].setEnabled(1)
            else:
                self.pageButtons[page_index-1].setEnabled(0)
    def RowPerPageChanged(self):
        try:
            rowperpage=self.perPageLineEdit.text()
            if rowperpage!='':
                self.rowcount_page=int(self.perPageLineEdit.text())
                self.page_count=self.dataCount//self.rowcount_page
                self.currentPageIndex=1
                page_rest=self.dataCount%self.rowcount_page
                if page_rest>0:
                    self.page_count+=1
                self.page10_count=self.page_count//10
                page10_rest=self.page_count%10
                if page10_rest>0:
                    self.page10_count+=1
                self.current_10PageIndex=1
                start_page=(self.current_10PageIndex-1)*10+1
                end_page=self.current_10PageIndex*10
                for page_index in range(start_page,end_page):
                    self.pageButtons[page_index-1].setText(str(page_index))
                for page_index in range(0,11):
                    if self.page_count>=page_index:
                        self.pageButtons[page_index-1].setEnabled(1)
                    else:
                        self.pageButtons[page_index-1].setEnabled(0)
        except Exception as e:
            print("更改每页行数发生错误",e)
    def PageSelectChanged(self):
        page=self.whichPageComboBox.currentText()
        if page!='':
            self.ReadDataInPage(page)
    def AddNewRow(self):
        try:
            fieldnames=[]
            for field in self.fieldlist:
                if field!='ID':
                    fieldnames.append(field)
            rowid=self.m_db.InsertToTable_NotFullField(self.tbjx,fieldnames,self.fieldvalue_list)
            if rowid!=None or rowid!='':
                self.refreshDataInfo()
                self.Go_First()
            else:
                print("数据添加失败！")
        except Exception as e:
            print("添加数据行时发生错误！",e)
    def EditRow(self):
        try:
            selectedRow=self.dataTableWidget.currentIndex().row()
            if selectedRow==None:
                return
            fieldvalues=[]
            for fieldindex in range(0,len(self.fieldnamelist)):
                rowvalue=self.dataTableWidget.item(selectedRow,fieldindex).text()
                fieldvalues.append(rowvalue)
            self.rowEditForm=RowEditForm()
            self.rowEditForm.row_init(self.fieldnamelist,self.fieldlist,self.field_zdlx_list,fieldvalues,self.field_kzlx_list,self.tbjx,self.tbid)
            self.rowEditForm.showMaximized()

        except Exception as e:
            print("编辑数据行时发生错误！",e)
    def DelRow(self):
        try:
            selectedRow=self.dataTableWidget.currentIndex().row()
            if selectedRow==None:
                return
            rowid=self.dataTableWidget.item(selectedRow,len(self.fieldlist)-1).text()

            MESSAGE = "疑问"
            reply = QMessageBox.question(None,MESSAGE, "确认删除当前选中的数据行吗？",QMessageBox.Yes | QMessageBox.No)
            if reply == QMessageBox.Yes:
                self.m_db.UpdateTable("delete from "+self.tbjx+" where ID='"+rowid+"'")
                self.refreshDataInfo()
                self.Go_Last()

        except Exception as e:
            print("删除数据行时发生错误！",e)
    def ClearRows(self):
        try:
            MESSAGE = "疑问"
            reply = QMessageBox.question(None, "确认删除所有数据吗？",MESSAGE,QMessageBox.Yes | QMessageBox.No)
            if reply == QMessageBox.Yes:
                self.m_db.UpdateTable("delete from "+self.tbjx)
                self.refreshDataInfo()
                self.dataTableWidget.setRowCount(0)

        except Exception as e:
            print("清空数据行时发生错误！",e)
    def refreshDataInfo(self):
        self.dataCount=self.m_db.GetRowCount("select * from "+self.tbjx)
        self.setWindowTitle(self.tbmc+"（共有"+str(self.dataCount)+"条记录）")
        self.page_count=self.dataCount//self.rowcount_page
        self.currentPageIndex=1
        page_rest=self.dataCount%self.rowcount_page
        if page_rest>0:
            self.page_count+=1
        self.page10_count=self.page_count//10
        page10_rest=self.page_count%10
        if page10_rest>0:
            self.page10_count+=1
        self.current_10PageIndex=1

        for page_index in range(0,11):
            if self.page_count>=page_index:
                self.pageButtons[page_index-1].setEnabled(1)
            else:
                self.pageButtons[page_index-1].setEnabled(0)
        self.whichPageComboBox.clear()
        for page_count in range(0,self.page_count):
            self.whichPageComboBox.addItem(str(page_count+1))
    def GenerateMenu(self,pos):
        menu=QMenu()
        addMenuItem=menu.addAction(u"添加")
        editMenuItem=menu.addAction(u"编辑")
        delMenuItem=menu.addAction(u"删除")
        action=menu.exec_(self.dataTableWidget.mapToGlobal(pos))
        if action==addMenuItem:
            self.AddNewRow()
        elif action==delMenuItem:
            self.DelRow()
        elif action==editMenuItem:
            self.EditRow()
        else:
            return