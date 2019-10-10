import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QMessageBox,QFileDialog,QGraphicsPixmapItem,QGraphicsScene,QErrorMessage,QWidget
from PyQt5.QtCore import  pyqtSignal
from PaperEditUI import Ui_PaperEditForm
from DBUtil import *
from EditPictureAnswerForm import EditPictureAnswerForm
class PaperEditForm(Ui_PaperEditForm,QWidget):
    parentclicked=pyqtSignal(str)
    def __init__(self,parent=None):
        super(PaperEditForm, self).__init__(parent)
        self.setupUi(self)
        self.m_db=DBUtil()
        kms=self.m_db.GetFieldValueToStrListFromDb("SJMC","XXFZK.SJBM","where SJLX=1 order by SXH")
        for km in kms:
            self.comboBox_km.addItem(km)
        stlxs=self.m_db.GetFieldValueToStrListFromDb("SJMC","XXFZK.SJBM","where SJLX=2 order by SXH")
        for sjlx in stlxs:
            self.comboBox_stlx.addItem(sjlx)

        self.pushButton_addItem.clicked.connect(self.AddPaperItem)
        self.pushButton_EditPictureTitle.clicked.connect(self.AddTitlePticture)
        self.pushButton_titilepicture_zooout.clicked.connect(self.TitlePictureZoomout)
        self.pushButton_titelpicture_zoomin.clicked.connect(self.TitlePictureZoomin)
        self.pushButton_AddTitleSubPicture.clicked.connect(self.AddTitleSubPicture)
        self.pushButton_titilesubpicture_zooout.clicked.connect(self.TitleSubPictureZoomout)
        self.pushButton_titelsubpicture_zoomin.clicked.connect(self.TitleSubPictureZoomin)

        self.toolButton_da1.clicked.connect(self.AddPictureAnswer1)
        self.toolButton_da2.clicked.connect(self.AddPictureAnswer2)
        self.toolButton_da3.clicked.connect(self.AddPictureAnswer3)
        self.toolButton_da4.clicked.connect(self.AddPictureAnswer4)
        self.toolButton_da5.clicked.connect(self.AddPictureAnswer5)
        self.toolButton_da6.clicked.connect(self.AddPictureAnswer6)

        self.pushButton_answer_zoomout_1.clicked.connect(self.PictureAnswerZoomout1)
        self.pushButton_answer_zoomout_2.clicked.connect(self.PictureAnswerZoomout2)
        self.pushButton_answer_zoomout_3.clicked.connect(self.PictureAnswerZoomout3)
        self.pushButton_answer_zoomout_4.clicked.connect(self.PictureAnswerZoomout4)
        self.pushButton_answer_zoomout_5.clicked.connect(self.PictureAnswerZoomout5)
        self.pushButton_answer_zoomout_6.clicked.connect(self.PictureAnswerZoomout6)

        self.pushButton_answer_zoomin_1.clicked.connect(self.PictureAnswerZoomin1)
        self.pushButton_answer_zoomin_2.clicked.connect(self.PictureAnswerZoomin2)
        self.pushButton_answer_zoomin_3.clicked.connect(self.PictureAnswerZoomin3)
        self.pushButton_answer_zoomin_4.clicked.connect(self.PictureAnswerZoomin4)
        self.pushButton_answer_zoomin_5.clicked.connect(self.PictureAnswerZoomin5)
        self.pushButton_answer_zoomin_6.clicked.connect(self.PictureAnswerZoomin6)
        self.pushButton_saveanswer.clicked.connect(self.SaveAnswer)
        self.pushButton_saveTitle.clicked.connect(self.SaveTitle)
        self.pushButton_saveRightAnswer.clicked.connect(self.SaveRightAnswer)
        self.pushButton_EditRightPictureAnswer.clicked.connect(self.EditPictureAnswer)

        self.editPictureAnswerForm=EditPictureAnswerForm()
        self.parentclicked.connect(self.SendEditPictureAnswerID)
        self.pushButton_testitem.clicked.connect(self.TestItem)

    def AddPaperItem(self):
        try:
            km=self.comboBox_km.currentText()
            stlx=self.comboBox_stlx.currentText()
            bh=self.m_db.GetFieldValueToSingleStrFromDb("max(BH)","XXFZK.TKB","")
            if bh==None:
                bh=0
            fieldnames=['BH','KM','STLX']
            fieldvalues=[]
            fieldvalues.append(str(bh+1))
            fieldvalues.append(km)
            fieldvalues.append(stlx)
            id=self.m_db.InsertToTable_NotFullField("XXFZK.TKB",fieldnames,fieldvalues)
            self.lineEdit_tmbs.setText(id)
        except:
            print("添加题目时发生错误")


    def AddTitlePticture(self):
        try:
            id=self.lineEdit_tmbs.text()
            if id=="":
                reply = QMessageBox.information(self, "标题","消息",QMessageBox.Yes | QMessageBox.No)
                return
            else:
                fileName, filetype = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()","","图片文件(*.jpg);")
                #将选中的文件入库
                self.m_db.WriteFileToBlob("TMTP","XXFZK.TKB","where ID='"+id+"'",fileName)
                #修改题目类型为“图片”
                self.m_db.UpdateTable("update XXFZK.TKB set TMLX='图片' where ID='"+id+"'")
                #显示图片
                image = QPixmap()
                image.load(fileName)
                scene=QGraphicsScene()
                self.title_picture_item=QGraphicsPixmapItem(image)
                scene.addItem(self.title_picture_item)
                self.graphicsView_titlepicture.setScene(scene)
                self.title_picture_zoomscale=1
        except:
            print("添加题目图片时发生错误")

    def TitlePictureZoomout(self):
        self.title_picture_zoomscale=self.title_picture_zoomscale+0.05
        if self.title_picture_zoomscale>=1.2:
            self.title_picture_zoomscale=1.2
        self.title_picture_item.setScale(self.title_picture_zoomscale)
    def TitlePictureZoomin(self):
        self.title_picture_zoomscale = self.title_picture_zoomscale - 0.05
        if self.title_picture_zoomscale <= 0:
            self.title_picture_zoomscale = 0.2
        self.title_picture_item.setScale(self.title_picture_zoomscale)
    def AddTitleSubPicture(self):
        try:
            id=self.lineEdit_tmbs.text()
            if id=="":
                reply = QMessageBox.information(self, "标题","试题标识不能为空，请先添加试题！",QMessageBox.Yes)
                return
            else:
                fileName, filetype = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()","","图片文件(*.jpg);")
                #将选中的文件入库
                self.m_db.WriteFileToBlob("TMPT","XXFZK.TKB","where ID='"+id+"'",fileName)
                #修改题目类型为“图片”
                self.m_db.UpdateTable("update XXFZK.TKB set YWPT='1' where ID='"+id+"'")
                #显示图片
                image = QPixmap()
                image.load(fileName)
                scene=QGraphicsScene()
                self.title_sub_picture_item=QGraphicsPixmapItem(image)
                scene.addItem(self.title_sub_picture_item)
                self.graphicsView_titlesubpicture.setScene(scene)
                self.title_sub_picture_zoomscale=1
        except:
            print("添加题目配图时发错误！")

    def TitleSubPictureZoomout(self):
        self.title_sub_picture_zoomscale=self.title_sub_picture_zoomscale+0.05
        if self.title_sub_picture_zoomscale>=1.2:
            self.title_sub_picture_zoomscale=1.2
        self.title_sub_picture_item.setScale(self.title_sub_picture_zoomscale)
    def TitleSubPictureZoomin(self):
        self.title_sub_picture_zoomscale = self.title_sub_picture_zoomscale - 0.05
        if self.title_sub_picture_zoomscale <= 0:
            self.title_sub_picture_zoomscale = 0.2
        self.title_sub_picture_item.setScale(self.title_sub_picture_zoomscale)
    def SaveAnswer(self):
        try:
            id = self.lineEdit_tmbs.text()
            if id == "":
                reply = QMessageBox.information(self, "标题", "试题标识不能为空，请先添加试题！", QMessageBox.Yes)
                return
            else:
                da1=self.lineEdit_da1.text()
                da2 = self.lineEdit_da2.text()
                da3 = self.lineEdit_da3.text()
                da4 = self.lineEdit_da4.text()
                da5 = self.lineEdit_da5.text()
                da6 = self.lineEdit_da6.text()
                if da1=="" and da2=="" and da3=="" and da4=="" and da5=="" and da6=="":
                    MESSAGE = "答案不能为空！"
                    reply = QMessageBox.information(self, "标题",MESSAGE, QMessageBox.Yes)
                    return
                else:
                    if da1=="" or da2=="" or da3=="" or da4=="" or da5=="" or da6=="":
                        MESSAGE = "部分答案为空，继续保存吗！"
                        reply = QMessageBox.question(None, "QMessageBox.question()", MESSAGE,QMessageBox.Yes | QMessageBox.No)
                        if reply == QMessageBox.No:
                            return
                 #保存答案到数据库
                sql="update XXFZK.TKB set WZDA1='"+da1+"',WZDA2='"+da2+"',WZDA3='"+da3+"',WZDA4='"+da4+"',WZDA5='"+da5+"',WZDA6='"+da6+"' where ID='"+id+"'"
                if(self.m_db.UpdateTable(sql)==None):
                    reply = QErrorMessage(self).showMessage("保存答案失败！")
                else:
                    reply = QMessageBox.information(self, "标题", "保存答案成功！", QMessageBox.Yes)
        except:
            print("保存文本答案时发生错误")
    def AddPictureAnswer1(self):
        try:
            id=self.lineEdit_tmbs.text()
            if id=="":
                reply = QMessageBox.information(self, "标题","试题标识不能为空，请先添加试题！",QMessageBox.Yes)
                return
            else:
                fileName, filetype = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()","","图片文件(*.jpg);")
                #将选中的文件入库
                self.m_db.WriteFileToBlob("TPDA1","XXFZK.TKB","where ID='"+id+"'",fileName)

                #显示图片
                image = QPixmap()
                image.load(fileName)
                scene=QGraphicsScene()
                self.picture_answer_item1=QGraphicsPixmapItem(image)
                scene.addItem(self.picture_answer_item1)
                self.graphicsView_da1.setScene(scene)
                self.picture_answer_zoomscale1=1
        except:
            print("添加图片答案1时发错误！")

    def AddPictureAnswer2(self):
        try:
            id = self.lineEdit_tmbs.text()
            if id == "":
                reply = QMessageBox.information(self, "标题", "试题标识不能为空，请先添加试题！", QMessageBox.Yes)
                return
            else:
                fileName, filetype = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "",
                                                                 "图片文件(*.jpg);")
                # 将选中的文件入库
                self.m_db.WriteFileToBlob("TPDA2", "XXFZK.TKB", "where ID='" + id + "'", fileName)

                # 显示图片
                image = QPixmap()
                image.load(fileName)
                scene = QGraphicsScene()
                self.picture_answer_item2 = QGraphicsPixmapItem(image)
                scene.addItem(self.picture_answer_item2)
                self.graphicsView_da2.setScene(scene)
                self.picture_answer_zoomscale2 = 1
        except:
            print("添加图片答案2时发错误！")
    def AddPictureAnswer3(self):
        try:
            id = self.lineEdit_tmbs.text()
            if id == "":
                reply = QMessageBox.information(self, "标题", "试题标识不能为空，请先添加试题！", QMessageBox.Yes)
                return
            else:
                fileName, filetype = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "",
                                                                 "图片文件(*.jpg);")
                # 将选中的文件入库
                self.m_db.WriteFileToBlob("TPDA3", "XXFZK.TKB", "where ID='" + id + "'", fileName)

                # 显示图片
                image = QPixmap()
                image.load(fileName)
                scene = QGraphicsScene()
                self.picture_answer_item3 = QGraphicsPixmapItem(image)
                scene.addItem(self.picture_answer_item3)
                self.graphicsView_da3.setScene(scene)
                self.picture_answer_zoomscale3 = 1
        except:
            print("添加图片答案3时发错误！")
    def AddPictureAnswer4(self):
        try:
            id = self.lineEdit_tmbs.text()
            if id == "":
                reply = QMessageBox.information(self, "标题", "试题标识不能为空，请先添加试题！", QMessageBox.Yes)
                return
            else:
                fileName, filetype = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "",
                                                                 "图片文件(*.jpg);")
                # 将选中的文件入库
                self.m_db.WriteFileToBlob("TPDA4", "XXFZK.TKB", "where ID='" + id + "'", fileName)

                # 显示图片
                image = QPixmap()
                image.load(fileName)
                scene = QGraphicsScene()
                self.picture_answer_item4 = QGraphicsPixmapItem(image)
                scene.addItem(self.picture_answer_item4)
                self.graphicsView_da4.setScene(scene)
                self.picture_answer_zoomscale4 = 1
        except:
            print("添加图片答案4时发错误！")
    def AddPictureAnswer5(self):
        try:
            id = self.lineEdit_tmbs.text()
            if id == "":
                reply = QMessageBox.information(self, "标题", "试题标识不能为空，请先添加试题！", QMessageBox.Yes)
                return
            else:
                fileName, filetype = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "",
                                                                 "图片文件(*.jpg);")
                # 将选中的文件入库
                self.m_db.WriteFileToBlob("TPDA5", "XXFZK.TKB", "where ID='" + id + "'", fileName)

                # 显示图片
                image = QPixmap()
                image.load(fileName)
                scene = QGraphicsScene()
                self.picture_answer_item5 = QGraphicsPixmapItem(image)
                scene.addItem(self.picture_answer_item5)
                self.graphicsView_da5.setScene(scene)
                self.picture_answer_zoomscale5 = 1
        except:
            print("添加图片答案5时发错误！")
    def AddPictureAnswer6(self):
        try:
            id = self.lineEdit_tmbs.text()
            if id == "":
                reply = QMessageBox.information(self, "标题", "试题标识不能为空，请先添加试题！", QMessageBox.Yes)
                return
            else:
                fileName, filetype = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "",
                                                                 "图片文件(*.jpg);")
                # 将选中的文件入库
                self.m_db.WriteFileToBlob("TPDA6", "XXFZK.TKB", "where ID='" + id + "'", fileName)

                # 显示图片
                image = QPixmap()
                image.load(fileName)
                scene = QGraphicsScene()
                self.picture_answer_item6 = QGraphicsPixmapItem(image)
                scene.addItem(self.picture_answer_item6)
                self.graphicsView_da6.setScene(scene)
                self.picture_answer_zoomscale6 = 1
        except:
            print("添加图片答案6时发错误！")

    def PictureAnswerZoomout1(self):
        self.picture_answer_zoomscale1 = self.picture_answer_zoomscale1 + 0.05
        if self.picture_answer_zoomscale1 >= 1.2:
            self.picture_answer_zoomscale1 = 1.2
        self.picture_answer_item1.setScale(self.picture_answer_zoomscale1)

    def PictureAnswerZoomin1(self):
        try:
            self.picture_answer_zoomscale1 = self.picture_answer_zoomscale1 - 0.05
            if self.picture_answer_zoomscale1 <= 0:
                self.picture_answer_zoomscale1 = 0.2
            self.picture_answer_item1.setScale(self.picture_answer_zoomscale1)
        except:
            print("缩小图片答案1时发生错误")

    def PictureAnswerZoomout2(self):
        self.picture_answer_zoomscale2 = self.picture_answer_zoomscale2 + 0.05
        if self.picture_answer_zoomscale2 >= 1.2:
            self.picture_answer_zoomscale2 = 1.2
        self.picture_answer_item2.setScale(self.picture_answer_zoomscale2)

    def PictureAnswerZoomin2(self):
        self.picture_answer_zoomscale2 = self.picture_answer_zoomscale2 - 0.05
        if self.picture_answer_zoomscale2 <= 0:
            self.picture_answer_zoomscale2 = 0.2
        self.picture_answer_item2.setScale(self.picture_answer_zoomscale2)

    def PictureAnswerZoomout3(self):
        self.picture_answer_zoomscale3 = self.picture_answer_zoomscale3 + 0.05
        if self.picture_answer_zoomscale3 >= 1.2:
            self.picture_answer_zoomscale3 = 1.2
        self.picture_answer_item3.setScale(self.picture_answer_zoomscale3)

    def PictureAnswerZoomin3(self):
        self.picture_answer_zoomscale3 = self.picture_answer_zoomscale3 - 0.05
        if self.picture_answer_zoomscale3 <= 0:
            self.picture_answer_zoomscale3 = 0.2
        self.picture_answer_item3.setScale(self.picture_answer_zoomscale3)
    def PictureAnswerZoomout4(self):
        self.picture_answer_zoomscale4 = self.picture_answer_zoomscale4 + 0.05
        if self.picture_answer_zoomscale4 >= 1.2:
            self.picture_answer_zoomscale4 = 1.2
        self.picture_answer_item4.setScale(self.picture_answer_zoomscale4)

    def PictureAnswerZoomin4(self):
        self.picture_answer_zoomscale4 = self.picture_answer_zoomscale4 - 0.05
        if self.picture_answer_zoomscale4 <= 0:
            self.picture_answer_zoomscale4 = 0.2
        self.picture_answer_item4.setScale(self.picture_answer_zoomscale4)
    def PictureAnswerZoomout5(self):
        self.picture_answer_zoomscale5 = self.picture_answer_zoomscale5 + 0.05
        if self.picture_answer_zoomscale5 >= 1.2:
            self.picture_answer_zoomscale5 = 1.2
        self.picture_answer_item5.setScale(self.picture_answer_zoomscale5)

    def PictureAnswerZoomin5(self):
        self.picture_answer_zoomscale5 = self.picture_answer_zoomscale5 - 0.05
        if self.picture_answer_zoomscale5 <= 0:
            self.picture_answer_zoomscale5 = 0.2
        self.picture_answer_item5.setScale(self.picture_answer_zoomscale5)
    def PictureAnswerZoomout6(self):
        self.picture_answer_zoomscale6 = self.picture_answer_zoomscale6 + 0.05
        if self.picture_answer_zoomscale6 >= 1.2:
            self.picture_answer_zoomscale6 = 1.2
        self.picture_answer_item6.setScale(self.picture_answer_zoomscale6)

    def PictureAnswerZoomin6(self):
        self.picture_answer_zoomscale6 = self.picture_answer_zoomscale6 - 0.05
        if self.picture_answer_zoomscale6 <= 0:
            self.picture_answer_zoomscale6 = 0.2
        self.picture_answer_item6.setScale(self.picture_answer_zoomscale6)
    def SaveTitle(self):
        try:
            title=self.lineEdit_tmnr.text()
            if title=="":
                reply = QMessageBox.information(self, "标题", "试题标题不能为空！", QMessageBox.Yes)
                return
            self.m_db.UpdateTable("update XXFZK.TKB set TMNR='"+title+"' where ID='"+id+"'")
        except:
            print("保存题目内容时发生错误")
    def SaveRightAnswer(self):
        try:
            righttitle = self.lineEdit_zqda.text()

            if righttitle == "":
                reply = QMessageBox.information(self, "标题", "试题标题不能为空！", QMessageBox.Yes)
                return
            self.m_db.UpdateTable("update XXFZK.TKB set WZDA='" + righttitle + "',ZQDALX='文字'  where ID='" + id + "'")
        except:
            print("保存试题正确答案时发生错误")
    def EditPictureAnswer(self):
        try:
            id = self.lineEdit_tmbs.text()
            if id == "":
                reply = QMessageBox.information(self, "标题", "试题标识不能为空，请先添加试题！", QMessageBox.Yes)
                return
            self.editPictureAnswerForm.show()
            self.parentclicked.emit(id)
        except:
            print("调用图片正确答案时发生错误！")
    def SendEditPictureAnswerID(self,s):
        try:
            self.editPictureAnswerForm.id=s
        except:
            print("发送试题ID发生错误")
    def TestItem(self):
        try:
            id = self.lineEdit_tmbs.text()
            if id == "":
                reply = QMessageBox.information(self, "标题", "试题标识不能为空，请先添加试题！", QMessageBox.Yes)
                return
            #试题类型、科目不能为空
            stlx=self.m_db.GetFieldValueToSingleStrFromDb("STLX","XXFZK.TKB","where ID='"+id+"'")
            km = self.m_db.GetFieldValueToSingleStrFromDb("KM", "XXFZK.TKB", "where ID='" + id + "'")
            if stlx=="":
                reply = QMessageBox.information(self, "错误", "试题类型不能为空！", QMessageBox.Yes)
                return
            if km=="":
                reply = QMessageBox.information(self, "错误", "科目不能为空！", QMessageBox.Yes)
                return
            #如果题目类型是文字，题目内容不能为空，如果是图片，检查图片是否存在
            tmlx=self.m_db.GetFieldValueToSingleStrFromDb("TMLX", "XXFZK.TKB", "where ID='" + id + "'")
            if tmlx=="文字":
                tmnr = self.m_db.GetFieldValueToSingleStrFromDb("TMNR", "XXFZK.TKB", "where ID='" + id + "'")
                if tmnr=="":
                    reply = QMessageBox.information(self, "错误", "题目内容不能为空！", QMessageBox.Yes)
                    return
            elif tmlx=="图片":
                pass
            #检查答案

        except Exception as e:
            print("检查试题信息时发生错误"+e.Message)


