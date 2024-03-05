# -*- coding: utf-8 -*-issueLabelNameDialogShow
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QColor
class LabelName_Dialog(QtWidgets.QDialog):
    AddLabelName = QtCore.pyqtSignal(str,str)
    def __init__(self,parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.color = "#ff0000"
        self.colorSelector = QtWidgets.QColorDialog()
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(358, 370)
        self.gridLayoutWidget = QtWidgets.QWidget(Dialog)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(0, 0, 351, 368))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(10, 20, 10, 20)
        self.gridLayout.setSpacing(20)
        self.gridLayout.setObjectName("gridLayout")
        self.LabelNameList = QtWidgets.QListWidget(self.gridLayoutWidget)
        self.LabelNameList.setObjectName("LabelNameList")
        self.gridLayout.addWidget(self.LabelNameList, 3, 0, 1, 1)
        self.buttonBox = QtWidgets.QDialogButtonBox(self.gridLayoutWidget)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout.addWidget(self.buttonBox, 2, 0, 1, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.textEdit = QtWidgets.QLineEdit(self.gridLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.textEdit.sizePolicy().hasHeightForWidth())
        self.textEdit.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setKerning(False)
        self.textEdit.setFont(font)
        self.textEdit.setObjectName("textEdit")
        self.horizontalLayout.addWidget(self.textEdit)
        self.toolButton = QtWidgets.QToolButton(self.gridLayoutWidget)
        self.toolButton.setObjectName("toolButton")
        
        self.horizontalLayout.addWidget(self.toolButton)
        self.gridLayout.addLayout(self.horizontalLayout, 1, 0, 1, 1)
        self.gridLayout.setRowStretch(1, 1)
        self.gridLayout.setRowStretch(2, 1)
        self.gridLayout.setRowStretch(3, 10)

        # 添加取消事件
        self.buttonBox.rejected.connect(self.reject)
        # 為 "OK" 按鈕添加 "clicked" 事件
        self.buttonBox.accepted.connect(self.accept)
        self.toolButton.clicked.connect(self.OpenColorPick)
        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Input the Label Name", "Input the Label Name"))
        self.LabelNameList.itemClicked.connect(self.SetLabelName)

    def accept(self):
        new_LabelName =self.textEdit.text()
        # 若輸入的LabelName為空且不重複則加入LabelNameList
        self.AddLabelName.emit(new_LabelName, self.color)
        super().accept()

    def reject(self):
        self.textEdit.clear()
        self.AddLabelName.emit('',self.color )
        super().reject()
        
    # 根據點擊的Item將相對應內容設置到textEdit
    def SetLabelName(self,item):
        self.textEdit.setText(item.text())

    def OpenColorPick(self):
        color = self.colorSelector.getColor()
        if color.isValid():
            hex_code = color.name()
            self.color = hex_code
            self.toolButton.setStyleSheet(f"background-color: {hex_code}")
        else:
            print("Invalid color selected.")





    




