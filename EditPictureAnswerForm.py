from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QMessageBox,QFileDialog,QGraphicsPixmapItem,QGraphicsScene,QErrorMessage,QApplication,QMainWindow
from PaperEditUI import Ui_PaperEditForm
from DBUtil import *
from PyQt5.QtCore import  pyqtSignal
from AddPictureForm import Ui_AddPictureForm
from DBUtil import *

class EditPictureAnswerForm(QtWidgets.QWidget,Ui_AddPictureForm):
    childclicked = pyqtSignal(str)
    id=""
    def __init__(self, parent=None):
        super(EditPictureAnswerForm, self).__init__(parent)
        self.m_db = DBUtil()
        self.setupUi(self)
        self.toolButton_da1.clicked.connect(self.AddPictureAnswer)
        self.pushButton_answer_zoomout_1.clicked.connect(self.PictureAnswerZoomout)
        self.pushButton_answer_zoomin_1.clicked.connect(self.PictureAnswerZoomin)
    def AddPictureAnswer(self):
        try:
            if self.id == "":
                reply = QMessageBox.information(self, "标题", "试题标识不能为空，请先添加试题！", QMessageBox.Yes)
                return
            else:
                fileName, filetype = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "",
                                                                 "图片文件(*.jpg);")
                # 将选中的文件入库
                self.m_db.WriteFileToBlob("TPDA", "XXFZK.TKB", "where ID='" + self.id + "'", fileName)
                self.m_db.UpdateTable("update XXFZK.TKB set ZQDALX='图片' where ID='"+self.id+"'")
                # 显示图片
                image = QPixmap()
                image.load(fileName)
                scene = QGraphicsScene()
                self.picture_answer_item = QGraphicsPixmapItem(image)
                scene.addItem(self.picture_answer_item)
                self.graphicsView_da1.setScene(scene)
                self.picture_answer_zoomscale = 1
        except Exception as e:
            print("添加图片答案时发错误！"+e)

    def PictureAnswerZoomout(self):
        self.picture_answer_zoomscale = self.picture_answer_zoomscale + 0.05
        if self.picture_answer_zoomscale >= 1.2:
            self.picture_answer_zoomscale = 1.2
        self.picture_answer_item.setScale(self.picture_answer_zoomscale)

    def PictureAnswerZoomin(self):
        try:
            self.picture_answer_zoomscale = self.picture_answer_zoomscale - 0.05
            if self.picture_answer_zoomscale <= 0:
                self.picture_answer_zoomscale = 0.2
            self.picture_answer_item.setScale(self.picture_answer_zoomscale)
        except:
            print("缩小图片答案1时发生错误")


