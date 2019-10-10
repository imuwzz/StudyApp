from PyQt5.QtGui import  QPixmap
from PyQt5.QtWidgets import *
from DBUtil import *
from PyQt5.QtGui import QIcon, QBrush, QColor,QCursor
from PyQt5.QtCore import Qt
import StringUtil
from DataClassForm import *
class PaperManagerForm(QWidget):
    def __init__(self):
        super(PaperManagerForm,self).__init__()
        self.initUi()
    def initUi(self):
        try:
            # 获取显示器分辨率
            self.desktop = QApplication.desktop()
            self.screenRect = self.desktop.screenGeometry()
            self.height = self.screenRect.height()
            self.width = self.screenRect.width()
            self.resize(self.width, self.height)
            self.setWindowTitle("试题管理")

            #layout_init
            mainLayout=QHBoxLayout()
            self.setLayout(mainLayout)
            leftLayout = QVBoxLayout()
            self.subjectListGroupBox=QGroupBox("科目列表")
            self.subjectlistLayout=QVBoxLayout()
            self.subjectListGroupBox.setLayout(self.subjectlistLayout)
            self.subjectListTree=QTreeWidget()
            self.subjectlistLayout.addWidget(self.subjectListTree)

            self.readSubejctButton=QPushButton("读取科目")
            self.readQuestionButton = QPushButton("读取试题")
            self.dataClassButton=QPushButton("DataClss")
            leftLayout.addWidget(self.subjectListGroupBox)

            leftBottomLayout =QHBoxLayout()

            leftBottomLayout.addWidget(self.readSubejctButton)
            leftBottomLayout.addWidget(self.readQuestionButton)
            leftBottomLayout.addWidget(self.dataClassButton)
            leftLayout.addLayout(leftBottomLayout)

            centerLayout = QVBoxLayout()
            self.questionListGroupBox = QGroupBox("试题列表")
            self.questionlistLayout = QVBoxLayout()

            self.questionListGroupBox.setLayout(self.questionlistLayout)
            self.questionTable = QTableWidget()
            self.questionlistLayout.addWidget(self.questionTable)
            centerLayout.addWidget(self.questionListGroupBox)

            mainLayout.addLayout(leftLayout)
            mainLayout.addLayout(centerLayout)

            #tree_init
            self.m_db = DBUtil()
            # 设置列数
            self.subjectListTree.setColumnCount(2)
            self.subjectListTree.setHeaderLabels(['科目','ID'])
            # 设置树形控件的列的宽度
            self.subjectListTree.setColumnWidth(0, 150)

            # 设置根节点

            # TODO 优化3 给节点添加响应事件
            #self.subjectListTree.clicked.connect(self.onClicked)

            self.createRightMenu()
            self.readSubejctButton.clicked.connect(self.ReadSubject)
            self.readQuestionButton.clicked.connect(self.ReadQuestion)

            self.dataClassButton.clicked.connect(self.DataClassManage)
            self.dataClassForm=DataClassForm()


        except Exception as e:
            print(e.Message)
    def ReadSubject(self):
        try:
            self.subjectListTree.clear()
            kms = self.m_db.GetFieldValueToStrListFromDb("SJMC", "XXFZK.SJBM", "where SJLX=1 order by SXH")
            for km in kms:
                root = QTreeWidgetItem(self.subjectListTree)
                root.setText(0, km)
                root.setText(1, km + '_root')
                # root.setIcon(0, QIcon('./images/root.png'))
                # todo 优化2 设置根节点的背景颜色
                brush_red = QBrush(Qt.red)
                root.setBackground(0, brush_red)
                brush_blue = QBrush(Qt.white)
                root.setBackground(1, brush_blue)
                # 加载根节点的所有属性与子控件
                self.subjectListTree.addTopLevelItem(root)
                self.BuildSubjectTree(km + '_root', root)
            # 节点全部展开
            self.subjectListTree.expandAll()

        except Exception as e:
            print("读取科目信息时发生错误",e.Message)

    def createRightMenu(self):
        self.subjectListTree.setContextMenuPolicy(Qt.CustomContextMenu)
        self.subjectListTree.customContextMenuRequested.connect(self.showRightMenu)
        self.rightMenu=QMenu(self.subjectListTree)

        addChapterMenuItem = self.rightMenu.addAction("添加科目")
        addChapterMenuItem.triggered.connect(self.AddSubjectAct)
        addChapterMenuItem = self.rightMenu.addAction("添加章节")
        addChapterMenuItem.triggered.connect(self.AddChapterAct)
        addChapterMenuItem = self.rightMenu.addAction("删除")
        addChapterMenuItem.triggered.connect(self.DelChapterAct)
    def showRightMenu(self,pos):
        try:
            self.rightMenu.exec(QCursor.pos())
            self.rightMenu.show()
        except:
            print("error")
    def AddChapterAct(self):
        selectItem=self.subjectListTree.currentItem()
        nodeID=selectItem.text(1)
        nodeText=selectItem.text(0)
        parentItem = selectItem.parent()
        while 1:
            if parentItem==None:
                break
            parentItem=selectItem.parent()
        if parentItem==None:
            km=nodeText
        else:
            km=parentItem.text(0)

        text, ok = QInputDialog.getText(None, "输入章节名称", "章节名称:", QLineEdit.Normal,"")
        if ok and text:
            bExist = self.m_db.TestDataExist("select * from XXFZK.ZJ where KM='"+km+"' and MC='" + text + "'")
            if bExist > 0:
                QMessageBox.information(self, "添加章节", "章节已经存在", QMessageBox.Yes | QMessageBox.No)
                return
            fieldvaluelist=[text,km,nodeID]
            id=self.m_db.InsertToOracle("XXFZK.ZJ",fieldvaluelist)

            child = QTreeWidgetItem(selectItem)
            child.setText(0, text)
            child.setText(1, id)

    def AddSubjectAct(self):
        text, ok = QInputDialog.getText(None, "输入科目名称", "科目名称:", QLineEdit.Normal,"")
        if ok and text:
            #判断是否存在科目
            bExist=self.m_db.TestDataExist("select * from XXFZK.SJBM where SJLX=1 and SJMC='"+text+"'")
            if bExist>0:
                QMessageBox.information(self, "添加科目", "科目已经存在", QMessageBox.Yes | QMessageBox.No)
                return

            sxh=self.m_db.GetFieldValueToSingleStrFromDb('max(SXH)','XXFZK.SJBM','where SJLX=1')
            if sxh==None:
                sxh=0
            sxh+=1
            fieldvaluelist=['1','科目',str(sxh),text,'']
            self.m_db.InsertToOracle("XXFZK.SJBM",fieldvaluelist)

            root = QTreeWidgetItem(self.subjectListTree)
            root.setText(0, text)
            root.setText(1, text + '_root')
            # root.setIcon(0, QIcon('./images/root.png'))
            # todo 优化2 设置根节点的背景颜色
            brush_red = QBrush(Qt.red)
            root.setBackground(0, brush_red)
            brush_blue = QBrush(Qt.white)
            root.setBackground(1, brush_blue)
            # 加载根节点的所有属性与子控件
            self.subjectListTree.addTopLevelItem(root)

    def BuildSubjectTree(self,sjid,parentItem):
        try:
            zjs=self.m_db.GetFieldValueToStrGroupsFromDb("MC,ID","XXFZK.ZJ","where SJID='"+sjid+"'")
            if len(zjs)!=0:
                mcs=zjs[0]
                ids=zjs[1]
                if len(mcs)!=0:
                    for index in range(0,len(mcs)):
                        mc=mcs[index]
                        id=ids[index]
                        # 设置子节点3
                        child = QTreeWidgetItem(parentItem)
                        child.setText(0, mc)
                        child.setText(1, id)
                        #child.setIcon(0, QIcon('./images/music.png'))
                        self.BuildSubjectTree(id,child)
        except Exception as e:
            print(e.Message)
    def DelChapterAct(self):
        try:
            selectItem = self.subjectListTree.currentItem()
            nodeID = selectItem.text(1)
            nodeText = selectItem.text(0)
            if nodeID==nodeText+"_root":
                MESSAGE = "确认删除当前的科目吗？"
                reply = QMessageBox.question(None, "QMessageBox.question()", MESSAGE,QMessageBox.Yes | QMessageBox.No )
                if reply == QMessageBox.No:
                    return
                self.m_db.UpdateTable("delete from XXFZK.SJBM where SJLX=1 and SJMC='"+nodeText+"'")
                index=self.subjectListTree.indexOfTopLevelItem(selectItem)
                selectItem.takeChildren()
                self.subjectListTree.takeTopLevelItem(index)
                #删除此根节点下所有章节
                self.m_db.UpdateTable("delete from XXFZK.ZJ where KM='"+nodeText+"'")
            else:
                MESSAGE = "确认删除当前的章节吗？"
                reply = QMessageBox.question(None, "QMessageBox.question()", MESSAGE, QMessageBox.Yes | QMessageBox.No)
                if reply == QMessageBox.No:
                    return
                self.m_db.UpdateTable("delete from XXFZK.ZJ where MC='" + nodeText + "'")
                index=selectItem.parent().indexOfChild(selectItem)
                selectItem.parent().takeChild(index)
                #删除此节点下所有节点

        except Exception as e:
            print(e.Message)
    def ReadQuestion(self):
        try:
            selectItem = self.subjectListTree.currentItem()
            nodeID = selectItem.text(1)
            nodeText = selectItem.text(0)
            #获取父节点
            parentItem = selectItem.parent()
            while 1:
                if parentItem == None:
                    break
                parentItem = selectItem.parent()
            if parentItem == None:
                km = nodeText
            else:
                km = parentItem.text(0)

            child_ids=self.ReadChildIDs(nodeID)
            child_ids.append(nodeID)
            condition=StringUtil.ChangeListToCondition(child_ids)
            #if condition=="":



        except Exception as e:
            print("读取试题发生错误："+e.Message)
    def ReadChildIDs(self,sjid):
        try:
            childIDs=[]
            ids=self.m_db.GetFieldValueToStrListFromDb("ID","XXFZK.ZJ","where SJID='"+sjid+"'")
            if len(ids)>0:
                childIDs.append(ids)
                for id in ids:
                    subIDs=self.ReadChildIDs(id)
                    if len(subIDs)>0:
                        childIDs.append(subIDs)
            return childIDs
        except Exception as e:
            print("获取子节点时发生错误："+e.Message)


    def DataClassManage(self):
        self.dataClassForm.show()





