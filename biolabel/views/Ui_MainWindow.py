# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QRectF, Qt, QPointF ,QLineF ,QSize
from PyQt5.QtGui import QPainterPath, QPainter, QPen, QBrush,QFont, QColor ,QIcon, QPixmap
from PyQt5.QtWidgets import QLabel, QGraphicsRectItem, QApplication, QGraphicsView, QGraphicsScene,QWidget ,QGraphicsItem , QGraphicsPathItem,QDialog,QGraphicsTextItem, QVBoxLayout, QHBoxLayout
from PyQt5 import QtWidgets
from .canvas import *
import sys

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1440, 900)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_1 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_1.setSpacing(0)
        self.horizontalLayout_1.setObjectName("horizontalLayout_1")
        self.verticalLayout_1 = QtWidgets.QVBoxLayout()
        self.verticalLayout_1.setSpacing(0)
        self.verticalLayout_1.setObjectName("verticalLayout_1")

        # === font of toolButton ===
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(14)
        # ==========================

        # === toolButton: CreateLabel ===
        self.toolButton_CreateLabel = QtWidgets.QToolButton(self.centralwidget)
        self.actionCreateLabel = QtWidgets.QAction(MainWindow)
        self.toolButton_CreateLabel.setDefaultAction(self.actionCreateLabel)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.toolButton_CreateLabel.sizePolicy().hasHeightForWidth())
        self.toolButton_CreateLabel.setSizePolicy(sizePolicy)
        self.toolButton_CreateLabel.setFont(font)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("biolabel/icons/pen.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.toolButton_CreateLabel.setIcon(icon)
        self.toolButton_CreateLabel.setIconSize(QtCore.QSize(50, 50))
        self.toolButton_CreateLabel.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.toolButton_CreateLabel.setObjectName("toolButton_CreateLabel")
        self.verticalLayout_1.addWidget(self.toolButton_CreateLabel)

        

        # === toolButton: EditLabel ===
        self.toolButton_EditLabel = QtWidgets.QToolButton(self.centralwidget)
        self.actionEditLabel = QtWidgets.QAction(MainWindow)
        self.toolButton_EditLabel.setDefaultAction(self.actionEditLabel)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.toolButton_EditLabel.sizePolicy().hasHeightForWidth())
        self.toolButton_EditLabel.setSizePolicy(sizePolicy)
        self.toolButton_EditLabel.setFont(font)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("biolabel/icons/select.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.toolButton_EditLabel.setIcon(icon1)
        self.toolButton_EditLabel.setIconSize(QtCore.QSize(50, 50))
        self.toolButton_EditLabel.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.toolButton_EditLabel.setObjectName("toolButton_EditLabel")
        self.verticalLayout_1.addWidget(self.toolButton_EditLabel)

        # === toolButton: DIP ===
        self.toolButton_DIP = QtWidgets.QToolButton(self.centralwidget)
        self.actionDIP = QtWidgets.QAction(MainWindow)
        self.toolButton_DIP.setDefaultAction(self.actionDIP)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.toolButton_DIP.sizePolicy().hasHeightForWidth())
        self.toolButton_DIP.setSizePolicy(sizePolicy)
        self.toolButton_DIP.setFont(font)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("biolabel/icons/edit-image.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.toolButton_DIP.setIcon(icon2)
        self.toolButton_DIP.setIconSize(QtCore.QSize(50, 50))
        self.toolButton_DIP.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.toolButton_DIP.setObjectName("toolButton_3")
        self.verticalLayout_1.addWidget(self.toolButton_DIP)


        # === label font === 
        labelfont = QtGui.QFont()
        labelfont.setFamily("Times New Roman")
        labelfont.setPointSize(12)
        # ==================
        
        # === label: LabelName ===
        self.label_LabelName = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(12)
        self.label_LabelName.setFont(labelfont)
        self.label_LabelName.setAlignment(QtCore.Qt.AlignCenter)
        self.label_LabelName.setObjectName("label_LabelName")
        self.verticalLayout_1.addWidget(self.label_LabelName)
        self.LabelNameList = QtWidgets.QListWidget(self.centralwidget)
        self.LabelNameList.setObjectName("listWidget_LabelName")
        self.verticalLayout_1.addWidget(self.LabelNameList)
        self.horizontalLayout_1.addLayout(self.verticalLayout_1)
        self.verticalLayout_canvas = QtWidgets.QVBoxLayout()
        self.verticalLayout_canvas.setObjectName("verticalLayout_canvas")

        # === canvas ===
        self.canvas = GraphicView(self.centralwidget)
        self.canvas.setObjectName("canvas")
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.canvas.sizePolicy().hasHeightForWidth())
        self.canvas.setSizePolicy(sizePolicy)
        self.canvas.setObjectName("graphicsView_2")
        self.verticalLayout_canvas.addWidget(self.canvas)
        self.horizontalLayout_1.addLayout(self.verticalLayout_canvas)
        self.verticalLayout_9 = QtWidgets.QVBoxLayout()
        self.verticalLayout_9.setSpacing(0)
        self.verticalLayout_9.setObjectName("verticalLayout_9")

        # === label: LabelList ===
        self.label_LabelList = QtWidgets.QLabel(self.centralwidget)
        self.label_LabelList.setFont(labelfont)
        self.label_LabelList.setAlignment(QtCore.Qt.AlignCenter)
        self.label_LabelList.setObjectName("label_LabelList")
        self.verticalLayout_9.addWidget(self.label_LabelList)
        self.LabelListWidget = QtWidgets.QListWidget(self.centralwidget)
        self.LabelListWidget.setObjectName("LabelListWidget")
        self.verticalLayout_9.addWidget(self.LabelListWidget)

        # === label: FileList ===
        self.label_FileList = QtWidgets.QLabel(self.centralwidget)
        self.label_FileList.setFont(labelfont)
        self.label_FileList.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_FileList.setAlignment(QtCore.Qt.AlignCenter)
        self.label_FileList.setObjectName("label_FileList")
        self.verticalLayout_9.addWidget(self.label_FileList)
        self.FileListWidget = QtWidgets.QListWidget(self.centralwidget)
        self.FileListWidget.setObjectName("FileListWidget")
        self.verticalLayout_9.addWidget(self.FileListWidget)
        self.horizontalLayout_1.addLayout(self.verticalLayout_9)
        self.horizontalLayout_1.setStretch(0, 1)
        self.horizontalLayout_1.setStretch(1, 7)
        self.horizontalLayout_1.setStretch(2, 3)
        self.verticalLayout.addLayout(self.horizontalLayout_1)
        MainWindow.setCentralWidget(self.centralwidget)

        # === ManuBar ===
        self.menuBar = QtWidgets.QMenuBar(MainWindow)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 1440, 22))
        self.menuBar.setObjectName("menuBar")
        self.menuFile = QtWidgets.QMenu(self.menuBar)
        self.menuFile.setObjectName("menuFile")
        MainWindow.setMenuBar(self.menuBar)
        self.statusBar = QtWidgets.QStatusBar(MainWindow)
        self.statusBar.setObjectName("statusBar")
        MainWindow.setStatusBar(self.statusBar)
        self.actionOpen = QtWidgets.QAction(MainWindow)
        self.actionOpen.setObjectName("actionOpen")
        self.actionOpenFolder = QtWidgets.QAction(MainWindow)
        self.actionOpenFolder.setObjectName("actionOpenDir")
        self.actionSave = QtWidgets.QAction(MainWindow)
        self.actionSave.setObjectName("actionSave")
        self.actionSave_as = QtWidgets.QAction(MainWindow)
        self.actionSave_as.setObjectName("actionSave_as")
        self.actionExportImage = QtWidgets.QAction(MainWindow)
        self.actionExportImage.setObjectName("actionExportImage")
        self.actionExit = QtWidgets.QAction(MainWindow)
        self.actionExit.setObjectName("actionExit")
        self.actionExportLabel = QtWidgets.QAction(MainWindow)
        self.actionExportLabel.setObjectName("actionExportLabel")
        self.menuFile.addAction(self.actionOpen)
        self.menuFile.addAction(self.actionOpenFolder)
        self.menuFile.addAction(self.actionSave)
        self.menuFile.addAction(self.actionSave_as)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionExportImage)
        self.menuFile.addAction(self.actionExportLabel)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionExit)
        self.menuBar.addAction(self.menuFile.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.toolButton_CreateLabel.setText(_translate("MainWindow", "Create Label"))
        self.toolButton_EditLabel.setText(_translate("MainWindow", "Edit Label"))
        self.toolButton_DIP.setText(_translate("MainWindow", "DIP"))
        self.label_LabelName.setText(_translate("MainWindow", "Label Name"))
        self.label_LabelList.setText(_translate("MainWindow", "Label List"))
        self.label_FileList.setText(_translate("MainWindow", " File List"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.actionOpen.setText(_translate("MainWindow", "OpenFile"))
        self.actionOpenFolder.setText(_translate("MainWindow", "OpenFolder"))
        self.actionSave.setText(_translate("MainWindow", "Save"))
        self.actionSave_as.setText(_translate("MainWindow", "Save as"))
        self.actionExportImage.setText(_translate("MainWindow", "Export Image"))
        self.actionExit.setText(_translate("MainWindow", "Exit"))
        self.actionExportLabel.setText(_translate("MainWindow", "Export Labels"))


