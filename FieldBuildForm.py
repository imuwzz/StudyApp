from PyQt5.QtGui import  QPixmap
from PyQt5.QtWidgets import *
from DBUtil import *
from PyQt5.QtGui import QIcon, QBrush, QColor,QCursor
from PyQt5.QtCore import Qt
from StringUtil import *

class FieldBuildForm(QWidget):
    def __init__(self):
        super(FieldBuildForm,self).__init__()
        self.initUi()
    def initUi(self):
        # 获取显示器分辨率
        #self.desktop = QApplication.desktop()
        #self.screenRect = self.desktop.screenGeometry()
        self.height = 400
        self.width = 600
        self.resize(self.width, self.height)
        self.setWindowTitle("字段定义")

        mainLayout=QVBoxLayout()
        self.setLayout(mainLayout)

        dataItemLayout=QHBoxLayout()
        sjxmcLabel=QLabel("数据名称")
        self.zdmcLineEdit=QLineEdit()
        self.mcjxLineEdit=QLineEdit()
        dataItemLayout.addWidget(sjxmcLabel)
        dataItemLayout.addWidget(self.zdmcLineEdit)
        dataItemLayout.addWidget(self.mcjxLineEdit)
        mainLayout.addLayout(dataItemLayout)

        zddxLayout=QHBoxLayout()
        zddxLabel=QLabel("字段大小")
        self.zddxComboBox=QComboBox()
        self.zddxComboBox.addItem('8')
        self.zddxComboBox.addItem('16')
        self.zddxComboBox.addItem('24')
        self.zddxComboBox.addItem('32')
        self.zddxComboBox.addItem('48')
        self.zddxComboBox.addItem('64')
        self.zddxComboBox.addItem('128')
        self.zddxComboBox.addItem('256')
        self.zddxComboBox.addItem('512')
        self.zddxComboBox.addItem('1024')
        self.zddxComboBox.addItem('2048')
        self.zddxComboBox.addItem('4096')
        self.zddxComboBox.setEditable(1)
        zddxLayout.addWidget(zddxLabel)
        zddxLayout.addWidget(self.zddxComboBox)
        mainLayout.addLayout(zddxLayout)

        zdlxLayout = QHBoxLayout()
        zdlxLabel = QLabel("字段大小")
        self.zdlxComboBox = QComboBox()
        self.zdlxComboBox.addItem('文本')
        self.zdlxComboBox.addItem('数字')
        self.zdlxComboBox.addItem('日期')
        self.zdlxComboBox.addItem('时间')
        self.zdlxComboBox.addItem('图片')
        self.zdlxComboBox.addItem('音频')
        self.zdlxComboBox.addItem('视频')
        self.zdlxComboBox.addItem('office文档')
        self.zdlxComboBox.addItem('文本文件')
        self.zdlxComboBox.addItem('二进制文件')

        zdlxLayout.addWidget(zdlxLabel)
        zdlxLayout.addWidget(self.zdlxComboBox)
        mainLayout.addLayout(zdlxLayout)

        kzlxLayout = QHBoxLayout()
        kzlxLabel = QLabel("数据类型")
        self.kzlxComboBox = QComboBox()
        self.kzlxComboBox.addItem('0-用户输入')
        self.kzlxComboBox.addItem('1-用户选择')
        self.kzlxComboBox.addItem('2-系统生成')
        self.kzlxComboBox.addItem('3-系统默认')

        kzlxLayout.addWidget(kzlxLabel)
        kzlxLayout.addWidget(self.kzlxComboBox)
        mainLayout.addLayout(kzlxLayout)

        zjLayout = QHBoxLayout()
        zjLabel = QLabel("主键")
        self.zjComboBox = QComboBox()
        self.zjComboBox.addItem('主键')
        self.zjComboBox.addItem('非主键')

        zjLayout.addWidget(zjLabel)
        zjLayout.addWidget(self.zjComboBox)
        mainLayout.addLayout(zjLayout)

        sfwkLayout = QHBoxLayout()
        sfwkLabel = QLabel("是否为空")
        self.sfwkComboBox = QComboBox()
        self.sfwkComboBox.addItem('可以为空')
        self.sfwkComboBox.addItem('不能为空')

        sfwkLayout.addWidget(sfwkLabel)
        sfwkLayout.addWidget(self.sfwkComboBox)
        mainLayout.addLayout(sfwkLayout)

        buttonLayout=QHBoxLayout()
        self.AddButton=QPushButton("确定")
        buttonLayout.addWidget(self.AddButton)
        mainLayout.addLayout(buttonLayout)


        self.zdmcLineEdit.textChanged.connect(self.zdmcChangedEvent)
        self.zdlxComboBox.activated.connect(self.zdlxSelectItemChanged)

    def fieldInit(self,zdmc,mcjx,zdlx,zddx,kzlx,zj,sfwk):
        self.bInit=0
        self.zdmcLineEdit.setText(zdmc)
        self.mcjxLineEdit.setText(mcjx)
        self.zdlxComboBox.setCurrentText(zdlx)

        self.zddxComboBox.setEditText(zddx)
        self.kzlxComboBox.setCurrentText(kzlx)
        self.zjComboBox.setCurrentText(zj)
        self.sfwkComboBox.setCurrentText(sfwk)
        self.bInit=1
    def addItemToTable(self):
        self.fieldinfo=[self.zdmcLineEdit.text(),self.mcjxLineEdit.text(),self.zdlxComboBox.currentText(),self.zddxComboBox.currentText(),self.kzlxComboBox.currentText(),self.zjComboBox.currentText(),self.sfwkComboBox.currentText()]
        self.close()
    def zdmcChangedEvent(self):
        try:
            if self.bInit==1:
                zdmc=self.zdmcLineEdit.text()
                mcjx=StringUtil.getPinyin(zdmc)
                self.mcjxLineEdit.setText(mcjx)
        except Exception :
            print("error")

    def zdlxSelectItemChanged(self):
        zdlx=self.zdlxComboBox.currentText()
        if zdlx!="文本":
            self.zddxComboBox.setCurrentText('0')






