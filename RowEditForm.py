from PyQt5.QtGui import  QPixmap
from PyQt5.QtWidgets import *
from DBUtil import *
from PyQt5.QtGui import QIcon, QBrush, QColor,QCursor,QIntValidator
from PyQt5.QtCore import Qt
import StringUtil

class RowEditForm(QWidget):
    def __init__(self):
        super(RowEditForm,self).__init__()
        self.initUi()
    def initUi(self):
        # 获取显示器分辨率
        self.desktop = QApplication.desktop()
        self.screenRect = self.desktop.screenGeometry()
        self.height = self.screenRect.height()
        self.width = self.screenRect.width()
        self.resize(self.width, self.height)
        self.setWindowTitle("数据编辑")

        self.mainLayout=QFormLayout()
        self.setLayout(self.mainLayout)
        self.inputControls=[]
        self.m_db = DBUtil()
    def row_init(self,fieldnames,fieldlist,fieldtypes,fieldvalues,fieldsources,tbjx,tbid):
        try:
            fieldcount=len(fieldnames)-1
            self.rowid=fieldvalues[fieldcount]
            self.tbid=tbid
            self.tbjx=tbjx
            self.fieldnames=fieldnames
            self.fieldlist=fieldlist
            self.fieldtypes=fieldtypes
            self.fieldsources=fieldsources
            for fieldindex in range(0,fieldcount):
                fieldname=fieldnames[fieldindex]
                field=fieldlist[fieldindex]
                fieldtype=fieldtypes[fieldindex]
                fieldvalue=fieldvalues[fieldindex]
                fieldsource=fieldsources[fieldindex]
                label_fieldname=QLabel(fieldname)
                if fieldtype=='文本':
                    if fieldsource=='用户定义' or fieldsource=='用户选择':
                        input_combobox=QComboBox()
                        input_combobox.setObjectName(field)
                        self.mainLayout.addRow(label_fieldname,input_combobox)
                        self.inputControls.append(input_combobox)
                        input_combobox.setEditText(fieldvalue)
                        input_combobox.currentTextChanged.connect(self.DataChanged)
                        #读取选择值
                    elif fieldsource=="用户输入":
                        input_lineEdit=QLineEdit()
                        input_lineEdit.setObjectName(field)
                        self.mainLayout.addRow(label_fieldname,input_lineEdit)
                        self.inputControls.append(input_lineEdit)
                        input_lineEdit.setText(fieldvalue)
                        input_lineEdit.textChanged.connect(self.DataChanged)
                    else:
                        input_lineEdit=QLineEdit()
                        input_lineEdit.setObjectName(field)
                        self.mainLayout.addRow(label_fieldname,input_lineEdit)
                        self.inputControls.append(input_lineEdit)
                        input_lineEdit.setText(fieldvalue)
                        input_lineEdit.textChanged.connect(self.DataChanged)
                        #系统生成值处理
                elif fieldtype=='数字':
                    input_lineEdit=QLineEdit()
                    input_lineEdit.setObjectName(field)
                    self.mainLayout.addRow(label_fieldname,input_lineEdit)
                    self.inputControls.append(input_lineEdit)
                    input_lineEdit.setText(fieldvalue)
                    input_lineEdit.textChanged.connect(self.DataChanged)
                elif fieldtype=='日期':
                    input_dateEdit=QDateEdit(fieldvalue)
                    input_dateEdit.setObjectName(field)
                    self.mainLayout.addRow(label_fieldname,input_dateEdit)
                    self.inputControls.append(input_dateEdit)
                    input_dateEdit.currentTextChanged.connect(self.DataChanged)
                elif fieldtype=="时间":
                    input_timeEdit=QTimeEdit(fieldvalue)
                    input_timeEdit.setObjectName(field)
                    self.mainLayout.addRow(label_fieldname,input_timeEdit)
                    self.inputControls.append(input_timeEdit)
                    input_timeEdit.currentTextChanged.connect(self.DataChanged)
                else:
                    input_file=QLineEdit()
                    input_file.setObjectName(field)
                    input_button=QPushButton('...')
                    input_button.setFixedWidth(30)
                    self.mainLayout.addRow(label_fieldname,input_file,input_button)
                    self.inputControls.append(input_file)
                    input_lineEdit.setText(fieldtype)
                    input_lineEdit.textChanged.connect(self.DataChanged)
            controlLayout=QHBoxLayout()
            updateButton=QPushButton("更新")
            closeButton=QPushButton('关闭')
            self.mainLayout.addRow(controlLayout)
            controlLayout.addStretch(0)
            controlLayout.addWidget(updateButton)
            controlLayout.addWidget(closeButton)
            closeButton.clicked.connect(self.close)
            updateButton.clicked.connect(self.UpdateData)
            self.DataChanged=0

        except Exception as e:
            print('行初始化失败',e)
    def UpdateData(self):
        try:
            if self.DataChanged==0:
                return
            if self.rowid=='':
                MESSAGE = "信息"
                reply = QMessageBox.information(self, "行ID为空！", MESSAGE)
                return
            bSaveSuc=0
            upSql=''
            for fieldindex in range(0,len(self.fieldlist)):
                fieldname=self.fieldlist[fieldindex]
                fieldmc=self.fieldnames[fieldindex]
                if fieldname in ['FLID','ID','MJ','SJLY','SJSJ','LRSJ']:
                    continue
                fieldtype=self.fieldtypes[fieldindex]
                fieldvalue=self.inputControls[fieldindex].text()
                if fieldvalue==None:
                    fieldvalue=''
                if fieldtype=='数字':
                    if upSql!='':
                        upSql+=','
                    upSql+=fieldname+"='"+fieldvalue+"'"
                elif fieldtype=='日期' or fieldtype=='时间':
                    if upSql!='':
                        upSql+=","
                    if fieldvalue!='':
                        upSql+=fieldname+"=to_date('"+fieldvalue+"','YYYY/MM/DD HH24:MI:SS')"
                    else:
                        upSql+=fieldname+"=to_date('1000-01-01 00:00:00','YYYY/MM/DD HH24:MI:SS')"
                elif fieldtype=='文本':
                    if upSql!='':
                        upSql+=','
                    upSql+=fieldname+"='"+fieldvalue+"'"
            result=self.m_db.UpdateTable("update "+self.tbjx+" set "+upSql+" where ID='"+self.rowid+"'")
            MESSAGE = "数据保存成功！"
            reply = QMessageBox.information(self, "信息", MESSAGE)
        except Exception as e:
            print("保存数据发生错误！",e)

    def DataChanged(self):
        self.DataChanged=1





