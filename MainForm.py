import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QMessageBox,QFileDialog,QGraphicsPixmapItem,QGraphicsScene,QErrorMessage,QWidget,QMainWindow,QMenuBar,QMenu,QAction,QApplication
from PyQt5.QtCore import  pyqtSignal
from MainFormUI import Ui_MainWindow
from DBUtil import *
from DataClassForm import *
from EditPictureAnswerForm import EditPictureAnswerForm
from PaperManagerForm import PaperManagerForm
from PaperEditForm import *
from SqliteManageForm import *
import  qdarkstyle
class MainForm(Ui_MainWindow,QMainWindow):
    def __init__(self,parent=None):
        super(MainForm, self).__init__(parent)
        self.setupUi(self)
        self.m_db=DBUtil()
        self.paperEditForm=PaperEditForm()
        self.paperManagerForm=PaperManagerForm()
        self.dataClassForm=DataClassForm()
        self.sqliteManageForm=SqliteManageForm()
        self.MenuItem_PaperEdit.triggered.connect(self.OpenPaperEdit)
        self.MenuItem_PaperManager.triggered.connect(self.OpenPaperManager)
        self.MenuItem_DataClass.triggered.connect(self.OpenDataClass)
        self.actionSqlite.triggered.connect(self.OpenSqliteManage)
        #获取显示器分辨率
        #self.desktop=QApplication.desktop()
        #self.screenRect=self.desktop.screenGeometry()
        #self.height=self.screenRect.height()
        #self.width=self.screenRect.width()
        #self.resize(self.width,self.height)
        #self.setFixedSize(self.width,self.height)
        self.setWindowTitle("学习辅助系统")

        self.styleComboBox.addItems(QStyleFactory.keys())
        self.styleComboBox.activated[str].connect(self.styleChanged)

    def OpenPaperEdit(self,qaction):
        self.paperEditForm.show()
    def OpenPaperManager(self):
        self.paperManagerForm.show()
    def OpenDataClass(self):
        self.dataClassForm.showMaximized()
    def styleChanged(self,style):
        QApplication.setStyle(style)
    def OpenSqliteManage(self):
        self.sqliteManageForm.showMaximized()
if __name__=="__main__":
    app=QtWidgets.QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    main=MainForm()
    main.showMaximized()
    sys.exit(app.exec_())