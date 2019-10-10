from PyQt5.QtGui import  QPixmap
from PyQt5.QtWidgets import *
from DBUtil import *
from PyQt5.QtGui import QIcon, QBrush, QColor,QCursor
from PyQt5.QtCore import Qt
import StringUtil
from TableBuildForm import TableBuildForm
from DataManagerForm import *
class DataClassForm(QWidget):
    def __init__(self):
        super(DataClassForm,self).__init__()
        self.initUi()
    def initUi(self):
        try:
            # 获取显示器分辨率
            self.desktop = QApplication.desktop()
            self.screenRect = self.desktop.screenGeometry()
            self.height = self.screenRect.height()
            self.width = self.screenRect.width()
            self.resize(self.width, self.height)
            self.setWindowTitle("数据分类管理")

            #layout_init
            mainLayout=QHBoxLayout()
            self.setLayout(mainLayout)


            leftLayout = QVBoxLayout()
            self.dataListGroupBox=QGroupBox("分类列表")
            self.datalistLayout=QVBoxLayout()
            self.dataListGroupBox.setLayout(self.datalistLayout)
            self.dataListTree=QTreeWidget()
            self.datalistLayout.addWidget(self.dataListTree)

            self.readDataListButton=QPushButton("读取分类")
            self.readTableButton = QPushButton("读取数据表")

            leftLayout.addWidget(self.dataListGroupBox)

            leftBottomLayout =QHBoxLayout()

            leftBottomLayout.addWidget(self.readDataListButton)
            leftBottomLayout.addWidget(self.readTableButton)
            leftLayout.addLayout(leftBottomLayout)

            centerLayout = QVBoxLayout()
            self.tableListGroupBox = QGroupBox("数据表列表")
            self.tablelistLayout = QVBoxLayout()

            self.tableListGroupBox.setLayout(self.tablelistLayout)
            self.dataTableWidget = QTableWidget()
            self.tablelistLayout.addWidget(self.dataTableWidget)

            centerBottomLayout = QHBoxLayout()
            self.defTableButton = QPushButton("自定义数据表")
            self.TableBrowseButton = QPushButton("数据浏览")
            centerBottomLayout.addWidget(self.defTableButton)
            centerBottomLayout.addWidget(self.TableBrowseButton)
            centerLayout.addWidget(self.tableListGroupBox)
            centerLayout.addLayout(centerBottomLayout)


            mainLayout.addLayout(leftLayout)
            mainLayout.addLayout(centerLayout)

            #tree_init
            self.m_db = DBUtil()
            # 设置列数
            self.dataListTree.setColumnCount(2)
            self.dataListTree.setHeaderLabels(['名称','ID','SJID'])
            # 设置树形控件的列的宽度
            self.dataListTree.setColumnWidth(0, 200)
            self.dataListTree.setColumnWidth(1, 1)
            self.dataListTree.setColumnWidth(2, 1)
            self.dataListTree.hideColumn(1)
            self.dataListTree.hideColumn(2)
            # 设置根节点

            # TODO 优化3 给节点添加响应事件
            #self.subjectListTree.clicked.connect(self.onClicked)

            #self.createRightMenu()
            self.readDataListButton.clicked.connect(self.BuildZlflTree)
            self.readTableButton.clicked.connect(self.ReadDataTable)

            self.dataTableWidget.setColumnCount(4)
            self.dataTableWidget.setHorizontalHeaderLabels(['表名','表简写','表ID','数据ID'])
            self.dataTableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
            self.dataTableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
            self.dataTableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)

            self.defTableButton.clicked.connect(self.TableDefine)
            self.tableBuildForm=TableBuildForm()
            self.dataManagerForm=DataManagerForm()
            self.TableBrowseButton.clicked.connect(self.DataManage)
        except Exception as e:
            print(e.Message)
    def BuildZlflTree(self,flid=""):
        try:
            self.dataListTree.clear()
            if flid==False:
                flxxs = self.m_db.GetFieldValueToStrGroupsFromDb("FLMC,FLID,SJID", "XTGLK.ZLFL_FLS", "where SJID='root' order by FLCC")
                if len(flxxs)>0:
                    flmcs=flxxs[0]
                    flids=flxxs[1]
                    sjids=flxxs[2]

                    for index in range(0,len(flmcs)):

                        root = QTreeWidgetItem(self.dataListTree)
                        root.setText(0, flmcs[index])
                        root.setText(1, flids[index])
                        root.setText(2,sjids[index])
                        # root.setIcon(0, QIcon('./images/root.png'))
                        # todo 优化2 设置根节点的背景颜色
                        brush_red = QBrush(Qt.red)
                        root.setBackground(0, brush_red)
                        brush_blue = QBrush(Qt.white)
                        root.setBackground(1, brush_blue)
                        # 加载根节点的所有属性与子控件
                        self.dataListTree.addTopLevelItem(root)
                        self.BuildSubZlflTree(flids[index],root)
            # 节点全部展开
            #self.dataListTree.expandAll()

        except Exception as e:
            print("读取科目信息时发生错误"+e.Message)

    def BuildSubZlflTree(self,sjid,parentNode):
        try:
            flxxs = self.m_db.GetFieldValueToStrGroupsFromDb("FLMC,FLID,SJID", "XTGLK.ZLFL_FLS", "where SJID='"+sjid+"' order by FLCC")
            if len(flxxs)>0:
                flmcs=flxxs[0]
                flids=flxxs[1]
                sjids=flxxs[2]

                for index in range(0,len(flmcs)):

                    child = QTreeWidgetItem(parentNode)
                    child.setText(0, flmcs[index])
                    child.setText(1, flids[index])
                    child.setText(2,sjids[index])
                    # root.setIcon(0, QIcon('./images/root.png'))
                    self.BuildSubZlflTree(flids[index],child)
        except:
            print("read data class info error!")
    def ReadDataTable(self):
        selectZlflItem=self.dataListTree.currentItem()
        if selectZlflItem==None:
            return
        flid=selectZlflItem.text(1)
        child_ids = self.ReadChildFlids(flid)
        child_ids.append(flid)
        condition = StringUtil.StringUtil.ChangeListToCondition('FLID',child_ids)
        if condition!="":
            condition=" where "+condition
            table_infos=self.m_db.GetFieldValueToStrGroupsFromDb("BMC,BJX,TBID,FLID","XTGLK.ZLFL_MSFF_TAB",condition)
            if len(table_infos) > 0:
                bmcs=table_infos[0]
                bjxs=table_infos[1]
                tbids=table_infos[2]
                flids=table_infos[3]
                if len(bmcs)>0:
                    self.dataTableWidget.setRowCount(len(bmcs))
                    for index in range(0,len(bmcs)):
                        bmc=bmcs[index]
                        bjx=bjxs[index]
                        tbid=tbids[index]
                        flid=flids[index]
                        newitem=QTableWidgetItem(bmc)
                        self.dataTableWidget.setItem(index,0,newitem)
                        newitem = QTableWidgetItem(bjx)
                        self.dataTableWidget.setItem(index, 1, newitem)
                        newitem = QTableWidgetItem(tbid)
                        self.dataTableWidget.setItem(index, 2, newitem)
                        newitem = QTableWidgetItem(flid)
                        self.dataTableWidget.setItem(index, 3, newitem)

    def ReadChildFlids(self, parentFlid):
        try:
            childFLIDs = []
            ids = self.m_db.GetFieldValueToStrListFromDb("FLID", "XTGLK.ZLFL_FLS", "where SJID='" + parentFlid + "'")
            if ids!=None and len(ids) > 0:
                for id in ids:
                    childFLIDs.append(id)
                for id in ids:
                    subIDs = self.ReadChildFlids(id)
                    if len(subIDs) > 0:
                        childFLIDs.append(subIDs)
            return childFLIDs
        except Exception as e:
            print("获取分类子节点时发生错误：" + e.Message)
    def TableDefine(self):
        try:
            selectedRow=self.dataTableWidget.currentIndex().row()
            if selectedRow==-1:
                return
            tbmc=self.dataTableWidget.item(selectedRow,0).text()
            tbjx=self.dataTableWidget.item(selectedRow, 1).text()
            tbid=self.dataTableWidget.item(selectedRow,2).text()
            self.tableBuildForm.table_init(tbid,tbmc,tbjx)
            #tbid=selectedItem.text(2)
            self.tableBuildForm.showMaximized()
        except Exception as e:
            print ("打开自定义数据表时发生错误！",e)

    def DataManage(self):
        try:
            selectedRow=self.dataTableWidget.currentIndex().row()
            if selectedRow == -1:
                return
            self.dataManagerForm = DataManagerForm()
            tbmc=self.dataTableWidget.item(selectedRow,0).text()
            tbjx=self.dataTableWidget.item(selectedRow, 1).text()
            tbid=self.dataTableWidget.item(selectedRow,2).text()
            self.dataManagerForm.data_init(tbid,tbmc,tbjx)
            #tbid=selectedItem.text(2)
            self.dataManagerForm.showMaximized()
        except Exception as e:
            print("进入数据管理模块发生错误！",e)



