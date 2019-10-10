from PyQt5 import QtCore, QtGui, QtWidgets,QDir,QPalette
from PyQt5.QtWidgets import QMessageBox,QFileDialog,QInputDialog,QLineEdit,QColorDialog,QFontDialog
class DialogUtil:
    # 输入对话框 取整数
    @staticmethod
    def setInteger():
        intNum, ok = QInputDialog.getInt(None, "QInputDialog.getInteger()", "Percentage:", 25, 0, 100, 1)
        if ok:
            return intNum

    # 输入对话框 取实数
    @staticmethod
    def setDouble():
        doubleNum, ok = QInputDialog.getDouble(None, "QInputDialog.getDouble()", "Amount:", 37.56, -10000, 10000, 2)
        if ok:
            return doubleNum

    # 输入对话框 取列表项
    @staticmethod
    def setItem():
        items = ["Spring", "Summer", "Fall", "Winter"]
        item, ok = QInputDialog.getItem(None, "QInputDialog.getItem()", "Season:", items, 0, False)
        if ok and item:
            return item

    # 输入对话框 取文本
    @staticmethod
    def setText():
        text, ok = QInputDialog.getText(None, "QInputDialog.getText()", "User name:", QLineEdit.Normal,QDir.home().dirName())
        if ok and text:
            return text

    # 输入对话框 取多行文本
    @staticmethod
    def setMultiLineText():
        text, ok = QInputDialog.getMultiLineText(None, "QInputDialog.getMultiLineText()", "Address:","John Doe\nFreedom Street")
        if ok and text:
            return text

    # 颜色对话框 取颜色
    @staticmethod
    def setColor():
        # options = QColorDialog.ColorDialogOptions(QFlag.QFlag(colorDialogOptionsWidget.value()))
        color = QColorDialog.getColor(Qt.green, self, "Select Color")
        if color.isValid():
            return color

    # 字体对话框 取字体
    @staticmethod
    def setFont():
        # options = QFontDialog.FontDialogOptions(QFlag(fontDialogOptionsWidget.value()))
        # font, ok = QFontDialog.getFont(ok, QFont(self.label_font.text()), self, "Select Font",options)
        font, ok = QFontDialog.getFont()
        if ok:
            return font

    # 目录对话框 取目录
    @staticmethod
    def setExistingDirectory():
        # options = QFileDialog.Options(QFlag(fileDialogOptionsWidget->value()))
        # options |= QFileDialog.DontResolveSymlinks | QFileDialog.ShowDirsOnly
        directory = QFileDialog.getExistingDirectory(None,"QFileDialog.getExistingDirectory()",self.label_directory.text())
        if directory:
            return directory

    # 打开文件对话框 取文件名
    @staticmethod
    def setOpenFileName():
        # options = QFileDialog.Options(QFlag(fileDialogOptionsWidget.value()))
        # selectedFilter
        fileName, filetype = QFileDialog.getOpenFileName(None,"QFileDialog.getOpenFileName()","","All Files (*);;Text Files (*.txt)")
        if fileName:
            return fileName

    # 打开文件对话框 取一组文件名
    @staticmethod
    def setOpenFileNames():
        # options = QFileDialog.Options(QFlag(fileDialogOptionsWidget.value()))
        # selectedFilter
        openFilesPath = "D:/documents/pyMarksix/draw/"
        files, ok = QFileDialog.getOpenFileNames(None, "QFileDialog.getOpenFileNames()",openFilesPath,"All Files (*);;Text Files (*.txt)")
        if len(files):
            return ",".join(files)

    # 保存文件对话框 取文件名
    @staticmethod
    def setSaveFileName():
        # options = QFileDialog.Options(QFlag(fileDialogOptionsWidget.value()))
        # selectedFilter
        fileName, ok = QFileDialog.getSaveFileName(None, "QFileDialog.getSaveFileName()","","All Files (*);;Text Files (*.txt)")
        if fileName:
            return fileName

    @staticmethod
    def criticalMessage(self):
        # reply = QMessageBox.StandardButton()
        MESSAGE = "批评！"
        reply = QMessageBox.critical(self,
                                     "QMessageBox.critical()",
                                     MESSAGE,
                                     QMessageBox.Abort | QMessageBox.Retry | QMessageBox.Ignore)
        if reply == QMessageBox.Abort:
            self.label_critical.setText("Abort")
        elif reply == QMessageBox.Retry:
            self.label_critical.setText("Retry")
        else:
            self.label_critical.setText("Ignore")

    @staticmethod
    def informationMessage(self):
        MESSAGE = "信息"
        reply = QMessageBox.information(self, "QMessageBox.information()", MESSAGE)
        if reply == QMessageBox.Ok:
            self.label_information.setText("OK")
        else:
            self.label_information.setText("Escape")

    @staticmethod
    def questionMessage():
        MESSAGE = "疑问"
        reply = QMessageBox.question(None, "QMessageBox.question()",MESSAGE,QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel)
        if reply == QMessageBox.Yes:
            return "Yes"
        elif reply == QMessageBox.No:
            return "No"
        else:
            return "Cancel"

    @staticmethod
    def warningMessage():
        MESSAGE = "警告文本"
        msgBox = QMessageBox(QMessageBox.Warning, "QMessageBox.warning()",MESSAGE,QMessageBox.Retry | QMessageBox.Discard | QMessageBox.Cancel,None)
        msgBox.setDetailedText("详细信息。。。")
        # msgBox.addButton("Save &Again", QMessageBox.AcceptRole)
        # msgBox.addButton("&Continue", QMessageBox.RejectRole)
        if msgBox.exec() == QMessageBox.AcceptRole:
            return "Retry"
        else:
            return "Abort"

