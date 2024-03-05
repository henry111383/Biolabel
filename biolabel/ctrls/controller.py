from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QFileDialog, QGraphicsScene, QGraphicsPixmapItem,QDialog,QMessageBox,QWidget
from PyQt5.QtGui import QImage, QPixmap, QCursor

from views.Ui_MainWindow import Ui_MainWindow
from views.canvas import *
import os
import numpy as np
import cv2
import pandas as pd
from views.Ui_label import *
from model.LabelService import LabelService
from model.ImageProcessService import ImageProcessService
from model.FileService import FileService
from model.LabelList import LabelList
from model.Image import Image

import matplotlib.pyplot as plt

CURSOR_DEFAULT = QtCore.Qt.ArrowCursor
CURSOR_POINT = QtCore.Qt.PointingHandCursor
CURSOR_DRAW = QtCore.Qt.CrossCursor
CURSOR_MOVE = QtCore.Qt.ClosedHandCursor
CURSOR_GRAB = QtCore.Qt.OpenHandCursor

class MainWindow_controller(QtWidgets.QMainWindow):
     
    current_file = []
    original_img = None
    current_img = None
    current_channel = 'RGB'
    imgItem = None
    LabelNameList = []

    def __init__(self):
        super().__init__() 
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        

        self.setup_control()
        self.labelService = LabelService()
        self.imageProcessService = ImageProcessService()
        self.fileService = FileService()
        self.templabelName = ""
        self.Color = "#ffffff"
        self.EditLabel = None
        self.EditUIlabel = None
        

    def setup_control(self):
        # menubar
        self.ui.actionOpen.triggered.connect(self.open_file)
        self.ui.actionOpenFolder.triggered.connect(self.open_folder)
        self.ui.actionExit.triggered.connect(lambda: exit())
        self.ui.actionSave.triggered.connect(self.saveMyLabel)
        self.ui.actionSave_as.triggered.connect(self.saveAs)
        self.ui.actionExportImage.triggered.connect(self.exportImage)
        self.ui.actionExportLabel.triggered.connect(self.exportLabel)

        # toolBotton
        self.ui.actionCreateLabel.triggered.connect(self.Click_CreateLabel)
        self.ui.actionEditLabel.triggered.connect(self.Click_EditLabel)
        self.ui.actionDIP.triggered.connect(self.Click_DIP)
       

        # issueCreateLabelCommand
        self.ui.canvas.scene.issueLabelCommand.connect(self.issueCreateLabelCommand)
        # issueUpdateLabelCommand
        self.ui.canvas.scene.issueUpdateLabelCommand.connect(self.issueMoveLabelCommand)
        # issueLabelNameDialogShow
        self.ui.canvas.scene.issueLabelNameDialogShow.connect(self.LabelNameDialogShow)
        # issueDeleteLabelCommand
        self.ui.canvas.scene.issueDeleteLabelCommand.connect(self.issueDeleteLabelCommand)

        #LabelNameDialogButton
        self.ui.canvas.scene.LabelNameDialog.AddLabelName.connect(self.LabelNameAccept)

        # === CreateLabel選單 ===
        self.CreateLabelmenu = QtWidgets.QMenu()
        # Add menu options
        create_polygons_option = self.CreateLabelmenu.addAction('Create Polygons')
        create_rect_option = self.CreateLabelmenu.addAction('Create Rectangle')
        create_line_option = self.CreateLabelmenu.addAction('Create Line')
        create_linestrip_option = self.CreateLabelmenu.addAction('Create LineStrip')
        create_point_option = self.CreateLabelmenu.addAction('Create Point')
        
        # Menu option events
        create_polygons_option.triggered.connect(lambda: self.ui.canvas.scene.ChangeShape("poly"))
        create_rect_option.triggered.connect(lambda: self.ui.canvas.scene.ChangeShape("rect"))
        create_point_option.triggered.connect(lambda: self.ui.canvas.scene.ChangeShape("point"))
        create_line_option.triggered.connect(lambda: self.ui.canvas.scene.ChangeShape("line"))
        create_linestrip_option.triggered.connect(lambda: self.ui.canvas.scene.ChangeShape("linestrip"))
        # =================================


        # === DIP 選單 ===
        self.DIPmenu = QtWidgets.QMenu()
        # Add menu options
        DIP_RGB2Gray = self.DIPmenu.addAction('GRAY')
        DIP_OTSUbinary = self.DIPmenu.addAction('BINARY')
        DIP_RGB2Hematoxylin = self.DIPmenu.addAction('Hematoxylin')
        DIP_RGB2Eosin = self.DIPmenu.addAction('Eosin')
        DIP_RGB2Dab = self.DIPmenu.addAction('Dab')
        self.DIPmenu.addSeparator()
        DIP_Back2Original = self.DIPmenu.addAction('Original Image')
        
        # Menu option events
        DIP_RGB2Gray.triggered.connect(lambda: self.issueImageProcessCommand('RGB2Gray'))
        DIP_OTSUbinary.triggered.connect(lambda: self.issueImageProcessCommand('OTSUbinary'))
        DIP_RGB2Hematoxylin.triggered.connect(lambda: self.issueImageProcessCommand('RGB2Hematoxylin'))
        DIP_RGB2Eosin.triggered.connect(lambda: self.issueImageProcessCommand('RGB2Eosin'))
        DIP_RGB2Dab.triggered.connect(lambda: self.issueImageProcessCommand('RGB2Dab'))
        DIP_Back2Original.triggered.connect(lambda: self.issueImageProcessCommand('Back2Original'))
        # =================================
        
        # self.ui.LabelListWidget.itemClicked.connect(self.item_clicked)
        self.ui.LabelListWidget.itemClicked.connect(self.handle_item_click)
        self.ui.FileListWidget.itemClicked.connect(self.FileListItemClick)
        
    def changeshape(self,shape):
        self.ui.canvas.shape=shape

    # === toolBotton action : Create Label ===
    def Click_CreateLabel(self):
        if self.ui.canvas.scene.ImgLoad :
            self.ui.canvas.scene.CreateMode = True
            self.ui.toolButton_CreateLabel.setStyleSheet\
                ("background-color: {}".format(QColor(Qt.darkGray).name()))
            self.ui.canvas.scene.EditMode   = False
            self.ui.toolButton_EditLabel.setStyleSheet("background-color: auto")
            self.StatusBarText('Mode : CreateLabel')
            self.ChangeLabelSelectable()
            self.CheckCursorStyle()
            self.CreateLabelmenu.exec_(QCursor.pos())
            self.ui.canvas.scene.resetDrawing()
        
    # === toolBotton action : Edit Label ===    
    def Click_EditLabel(self):
        if self.ui.canvas.scene.ImgLoad :
            self.ui.canvas.scene.CreateMode = False
            self.ui.toolButton_CreateLabel.setStyleSheet("background-color: auto")
            self.ui.canvas.scene.EditMode   = True
            self.ui.toolButton_EditLabel.setStyleSheet\
                ("background-color: {}".format(QColor(Qt.darkGray).name()))
            self.StatusBarText('Mode : EditLabel')
            self.ChangeLabelSelectable()
            self.CheckCursorStyle()

    # === toolBotton action : DIP ===
    def Click_DIP(self):
        if self.ui.canvas.scene.ImgLoad :
            self.DIPmenu.exec_(QCursor.pos())
        

    # === MenuBar action : OpenFile ===
    def open_file(self):
        filename, filetype = QFileDialog.getOpenFileName(self, "Open file", "./")
        self.open_file_subfunction(filename)

    def open_file_subfunction(self, file_name):
        self.current_file = file_name
        MyJsonName = os.path.dirname(file_name) \
                    + '/' \
                    + os.path.splitext(os.path.basename(file_name))[0] \
                    + '.json'

        print(self.current_file)
        print(MyJsonName)

        if file_name :
            self.read_img_to_view(file_name)
            if self.original_img :
                self.resetMode()
                self.ui.canvas.scene.ImgLoad = True
            else:
                self.errorDialog('Not Supported Format')
            self.read_labels_to_view(MyJsonName)
            self.ui.canvas.scene.resetDrawing()


    # === MenuBar action :OpenDir ===
    def open_folder(self):
        supported_format = ['.bmp', '.pbm', '.pgm', '.ppm', '.sr', '.ras', '.jpeg', '.jpg', '.jpe', '.jp2', '.tiff', '.tif', '.png']
        folder_path = QFileDialog.getExistingDirectory(self, "Open folder", "./")
        if folder_path:
            
            UIFileList = self.ui.FileListWidget
            self.ui.FileListWidget.clear()
            for fileItem in os.listdir(folder_path):
                supportedFlag = False
                for fmt in supported_format:
                    if fmt in fileItem:
                        supportedFlag = True
                        break
                if supportedFlag :
                    item = QtWidgets.QListWidgetItem()
                    item.setText(fileItem)
                    item.setData( 4, folder_path)  
                    UIFileList.addItem(item)
            self.resetMode()
            self.ui.canvas.scene.clear()
        else: 
            return
    
        

    # reset Mode after OpenFile
    def resetMode(self):
        self.ui.canvas.scene.CreateMode = False
        self.ui.toolButton_CreateLabel.setStyleSheet("background-color: auto")
        self.ui.canvas.scene.EditMode   = False
        self.ui.toolButton_EditLabel.setStyleSheet("background-color: auto")
        self.StatusBarText("")
        self.resetComponent()
        self.CheckCursorStyle()
    
    def resetComponent(self):
        self.LabelNameList.clear()  
        # ViewWidgets
        self.ui.LabelNameList.clear()
        self.ui.LabelListWidget.clear()
        self.ui.canvas.scene.LabelNameDialog.LabelNameList.clear()
        self.labelService.labelList.ClearAllLabel()
        self.ui.canvas.scene.UILabelList.clear()
        self.ui.LabelListWidget.clear()

    # def clearView(self):
    #     self.ui.canvas.scene
    # ============= Read Data to View =============
    # read image to view
    def read_img_to_view(self, imgFileLocation):
        self.original_img = self.fileService.LoadImage(imgFileLocation)
        self.current_img  = self.original_img
        if self.original_img :
            # reset the view
            self.ui.canvas.scene.clear()
            # get size of image
            img = self.original_img.GetImg()
            h, w, _ = img.shape
            img[0, : , :] = 0
            img[h-1, : ,:] = 0
            img[:, w-1, :] = 0
            img[:, 0, :] = 0
            # set QImage
            qImg = QImage(img, w, h, 3 * w, QImage.Format_RGB888)
            # set QPixmanp
            pix = QPixmap.fromImage(qImg)
            self.imgItem = QGraphicsPixmapItem(pix)
            self.ui.canvas.scene.setSceneRect(QRectF(0, 0, w, h))
            self.ui.canvas.scene.addItem(self.imgItem)
            self.ui.canvas.setAlignment(Qt.AlignTop | Qt.AlignCenter)
        return
    
    # read labels to view
    def read_labels_to_view(self, JsonFileName):
        self.resetComponent()
        labelUI_dict = self.fileService.LoadUILabel(JsonFileName)
        if len(labelUI_dict) == 0:
            self.labelService.labelList = LabelList()
        else: 
            for key in labelUI_dict.keys():
                UIlabel = labelUI_dict[key]
                self.templabelName = UIlabel['Name']
                color = UIlabel['Color']
                ptList = []
                for pt in UIlabel['Points']:
                    ptList.append(Point(pt[0], pt[1]))
                labelType = UIlabel['Type']
                # print(UIlabel)
                if labelType == 'rect':
                    # create UIlabel (Rectengle)
                    self.ui.canvas.scene.tempLabel = MyRectItem(ptList[0].GetX(), ptList[0].GetY(), ptList[1].GetX(), ptList[1].GetY())
                    self.issueCreateLabelCommand('CreateLabel', color ,labelType, ptList)
                    self.ui.canvas.scene.tempLabel.label.SetLabelColor(color)
                    self.ui.canvas.scene.UILabelList.append(self.ui.canvas.scene.tempLabel)
                    self.ui.canvas.scene.addItem(self.ui.canvas.scene.tempLabel)
                    self.ui.canvas.scene.tempLabel.setLineColor(color)
                    self.AddLabelNameList(self.templabelName)
                    
                elif labelType == 'point':
                    # create UIlabel (Point)
                    self.ui.canvas.scene.tempLabel = MyPointItem(ptList[0].GetX(), ptList[0].GetY())
                    self.issueCreateLabelCommand('CreateLabel', color ,labelType, ptList)
                    self.ui.canvas.scene.tempLabel.label.SetLabelColor(color)
                    self.ui.canvas.scene.UILabelList.append(self.ui.canvas.scene.tempLabel)
                    self.ui.canvas.scene.addItem(self.ui.canvas.scene.tempLabel)
                    self.ui.canvas.scene.tempLabel.setLineColor(color)
                    self.AddLabelNameList(self.templabelName)

                elif labelType == 'line':
                    # create UIlabel (Line)
                    self.ui.canvas.scene.tempLabel = MyLineItem(ptList[0].GetX(), ptList[0].GetY(), ptList[1].GetX(), ptList[1].GetY())
                    self.issueCreateLabelCommand('CreateLabel', color ,labelType, ptList)
                    self.ui.canvas.scene.tempLabel.label.SetLabelColor(color)
                    self.ui.canvas.scene.UILabelList.append(self.ui.canvas.scene.tempLabel)
                    self.ui.canvas.scene.addItem(self.ui.canvas.scene.tempLabel)
                    self.ui.canvas.scene.tempLabel.setLineColor(color)
                    self.AddLabelNameList(self.templabelName)

                elif labelType == 'linestrip':
                    # create UIlabel (Line)
                    self.ui.canvas.scene.tempLabel = MyLineStrip([(ptList[0].GetX(), ptList[0].GetY()), \
                                                                  (ptList[1].GetX(), ptList[1].GetY())])
                    if len(ptList) >= 3:
                        for pt in ptList[2:]:
                            self.ui.canvas.scene.tempLabel.addPoint((pt.GetX(), pt.GetY()))
                    self.ui.canvas.scene.tempLabel.updatePath()
                    self.issueCreateLabelCommand('CreateLabel', color ,labelType, ptList)
                    self.ui.canvas.scene.tempLabel.label.SetLabelColor(color)
                    self.ui.canvas.scene.UILabelList.append(self.ui.canvas.scene.tempLabel)
                    self.ui.canvas.scene.addItem(self.ui.canvas.scene.tempLabel)
                    self.ui.canvas.scene.tempLabel.setLineColor(color)
                    self.AddLabelNameList(self.templabelName)
                
                elif labelType == 'poly':
                    # create UIlabel (Polygon)
                    self.ui.canvas.scene.tempLabel = MyLineStrip([(ptList[0].GetX(), ptList[0].GetY()), \
                                                                  (ptList[1].GetX(), ptList[1].GetY())], \
                                                                    shape='poly')
                    if len(ptList) >= 3:
                        for pt in ptList[2:]:
                            self.ui.canvas.scene.tempLabel.addPoint((pt.GetX(), pt.GetY()))
                    self.ui.canvas.scene.tempLabel.updatePath()
                    self.issueCreateLabelCommand('CreateLabel', color ,labelType, ptList)
                    self.ui.canvas.scene.tempLabel.label.SetLabelColor(color)
                    self.ui.canvas.scene.UILabelList.append(self.ui.canvas.scene.tempLabel)
                    self.ui.canvas.scene.addItem(self.ui.canvas.scene.tempLabel)
                    self.ui.canvas.scene.tempLabel.setLineColor(color)
                    self.AddLabelNameList(self.templabelName)
            self.Click_EditLabel()
        pass

    # ============= For Main View =============
    # set text in StatusBar
    def StatusBarText(self, str):
        self.ui.statusBar.showMessage(str)
        return
    
    # change QGraphicsItem selectable
    def ChangeLabelSelectable(self):
        scene = self.ui.canvas.scene
        if scene.EditMode :
            for item in scene.UILabelList:
                item.setFlag(QGraphicsItem.ItemIsSelectable, False)
                item.setFlag(QGraphicsItem.ItemSendsGeometryChanges, True)
                item.setFlag(QGraphicsItem.ItemIsFocusable, True)
                item.setFlag(QGraphicsItem.ItemIsMovable, True) 
                item.EditMode = True
                
        else:
            for item in scene.UILabelList:
                item.setFlag(QGraphicsItem.ItemIsSelectable, False)
                item.setFlag(QGraphicsItem.ItemSendsGeometryChanges, False)
                item.setFlag(QGraphicsItem.ItemIsFocusable, False)
                item.setFlag(QGraphicsItem.ItemIsMovable, False) 
                item.EditMode = False

    # 讓鼠標可以變化
    def CheckCursorStyle(self):
        if self.ui.canvas.scene.CreateMode :
            self.ui.canvas.setCursor(CURSOR_DRAW)
        elif self.ui.canvas.scene.EditMode : 
            self.ui.canvas.setCursor(CURSOR_GRAB)
        else:
            self.ui.canvas.setCursor(CURSOR_DEFAULT)
    
    # ============= Create Labels =============
    # set LabelName
    def SetLabelNameList(self):
        for item in self.LabelNameList:
            self.ui.LabelNameList.addItem(item)
            self.ui.canvas.scene.LabelNameDialog.LabelNameList.addItem(item)
            
    def LabelNameDialogShow(self, color): # for Create
        self.templabelName = ""
        self.ui.canvas.scene.LabelNameDialog.toolButton.setStyleSheet(f"background-color: {color}")
        self.ui.canvas.scene.LabelNameDialog.color = color
        self.ui.canvas.scene.LabelNameDialog.exec_()
        self.ui.canvas.scene.setFocus()
        QApplication.processEvents()

    def LabelNameDialogShowForEdit(self, label, UIlabel, item): # for Edit
        self.EditLabel = label
        self.UIlabel = UIlabel
        self.EditItem = item
        self.ui.canvas.scene.LabelNameDialog.textEdit.setText(label.GetName())
        color = QColor(label.GetLabelColor())
        self.ui.canvas.scene.LabelNameDialog.toolButton.setStyleSheet(f"background-color: {color.name()}")
        self.ui.canvas.scene.LabelNameDialog.color = label.GetLabelColor()
        self.ui.canvas.scene.LabelNameDialog.exec_()
        self.UpdateLabelNameList()
        
    def LabelNameAccept(self, str, color):
        if self.checkLabelNameSuccess(str):
            if self.ui.canvas.scene.CreateMode == True:
                self.templabelName = str    
                self.AddLabelNameList(str)
            elif self.ui.canvas.scene.EditMode == True:
                label = self.EditLabel
                if label.GetName() != str:
                    self.issueEditLabelNameCommand(str ,label)
                    self.EditItem.setText(str)
                if label.GetLabelColor() != color:
                    self.issueEditLabelColorCommand(color ,label)
                    self.UIlabel.setLineColor(color)
                    self.Color = color 

    def AddLabelNameList(self, str):
        if self.LabelNameList.count(str) == 0:
            self.LabelNameList.append(str)
            self.ui.LabelNameList.addItem(str)
            self.ui.canvas.scene.LabelNameDialog.LabelNameList.addItem(str)

    def UpdateLabelNameList(self):
        UILabelList = self.ui.LabelListWidget
        self.LabelNameList.clear()
        for index in range(UILabelList.count()):
            item = UILabelList.item(index)
            data = item.data(4).GetName()
            self.LabelNameList.append(data)
        self.LabelNameList = list(set(self.LabelNameList))
        # reset the list
        self.ui.canvas.scene.LabelNameDialog.LabelNameList.clear()
        self.ui.LabelNameList.clear()
        for Name in self.LabelNameList:
            self.ui.canvas.scene.LabelNameDialog.LabelNameList.addItem(Name)
            self.ui.LabelNameList.addItem(Name)

    def checkLabelNameSuccess(self, str):
        print(str)
        if len(str) != 0: # sucess 
            self.ui.canvas.scene.inputLabelNameSuccess = True
            return True
        else : # fails
            self.ui.canvas.scene.inputLabelNameSuccess = False
            return False

    # Call LabelService
    def issueCreateLabelCommand(self, cmd, color ,type, ptList):
        if cmd == 'CreateLabel' and len(self.templabelName) !=0:
            new_label = self.labelService.CreateLabel(self.templabelName, type, color, ptList) # 創建一個Label
            item = QtWidgets.QListWidgetItem()
            item.setText(self.templabelName)
            item.setData(4, new_label)  
            item.setData(5, self.ui.canvas.scene.tempLabel)  
            self.ui.LabelListWidget.addItem(item)
            self.ui.canvas.scene.tempLabel.label = new_label # 每個UILabel對應一個Label
            self.ui.canvas.scene.tempLabel.setLineColor(self.ui.canvas.scene.LabelNameDialog.color)
            self.issueEditLabelColorCommand(self.ui.canvas.scene.LabelNameDialog.color ,new_label)
            self.labelService.labelList.AddLabel(new_label) # 加入labelList
            print(f"成功！目前有這些：{[x.GetName() for x in self.labelService.labelList.GetLabelList()]}")
        else:
            # LabelName為空則不創建Label
            self.ui.canvas.scene.drawing = True

    
    # ============= Control Labels =============
    def handle_item_click(self, item):
        if(self.ui.canvas.scene.EditMode):
            self.LabelNameDialogShowForEdit(item.data(4), item.data(5), item)

    def FileListItemClick(self,item):  
        self.open_file_subfunction(os.path.join(item.data(4), item.text()))

    # Call LabelService
    def issueMoveLabelCommand(self, ptlist  , Label):
        self.labelService.moveLabel( ptlist , Label) 

    def issueEditLabelNameCommand(self, labelname, Label):
        self.labelService.EditLabelName( labelname, Label) 

    def issueEditLabelColorCommand(self, color , Label):
        self.labelService.EditLabelColor(color , Label) 

    def issueDeleteLabelCommand(self,  Label):
        UILabelList = self.ui.LabelListWidget
        for index in range(UILabelList.count()):
            item = UILabelList.item(index)
            data = item.data(4)  
            if data == Label:
                UILabelList.takeItem(index) 
                break
        self.labelService.DeleteLabel(Label)
        self.UpdateLabelNameList()
    
    # ============= DIP =============
    # Call DIPService
    def issueImageProcessCommand(self, str):
        # revision channel name
        if 'RGB' in str:
            self.current_img.SetChannel(str.replace('RGB2',''))
        elif 'OTSUbinary' in str:
            self.current_img.SetChannel('binary')
        # DIP
        if str == 'Back2Original':
            self.current_img.SetChannel('RGB')
            self.current_img = self.original_img
            # get size of image
            h, w, _ = self.original_img.GetImg().shape
            # set QImage
            qImg = QImage(self.original_img.GetImg(), w, h, 3 * w, QImage.Format_RGB888)
            # set QPixmanp
            pix = QPixmap.fromImage(qImg)
            self.imgItem.setPixmap(pix)
        else:
            self.current_img = eval(f'self.imageProcessService.{str}(self.original_img)')
            img = self.current_img.GetImg()
            # get size of image
            h, w, _ = img.shape
            # set QImage
            qImg = QImage(img, w, h, 3 * w, QImage.Format_RGB888)
            # set QPixmanp
            pix = QPixmap.fromImage(qImg)
            self.imgItem.setPixmap(pix)

    # ============= Save =============
    # Save My label to Json
    def saveMyLabel(self):
        if self.original_img :
            current_labellist = self.labelService.labelList
            # into File
            MyLabelFile = self.fileService.ConvertLabel2File(label=current_labellist)
            # save LabelFile
            FileName = os.path.splitext(self.current_file)[0] + '.json'
            MyLabelFile.SetFileLocation(FileName)
            self.fileService.StoreLabel(LF=MyLabelFile, format='My')
        else :
            self.errorDialog('No any existing image!')
            
    # Save label by other name 
    def saveAs(self):
        if self.current_img:
            file_name, _ = QFileDialog.getSaveFileName(self, "Save File", "", 'JSON (*.json)')
            print(file_name)
            if file_name:
                current_labellist = self.labelService.labelList
                # into File
                MyLabelFile = self.fileService.ConvertLabel2File(label=current_labellist)
                # save LabelFile
                MyLabelFile.SetFileLocation(file_name)
                self.fileService.StoreLabel(LF=MyLabelFile, format='My')
        else :
            self.errorDialog('No any existing image!')

    # ============= Export =============
    # Export DIP image 
    def exportImage(self):
        filter_str = "PNG Files (*.png);;TIF Files (*.tif);;All Files (*)"
        if self.current_img :
            file_name, _ = QFileDialog.getSaveFileName(self, "Save File", "", filter_str)
            print(file_name)
            if file_name:
                MyImagefile = self.fileService.ConvertImage2File(img=self.current_img)
                if self.fileService.StoreImage(IF=MyImagefile, fileLocation=file_name):
                    return
                else:
                    self.errorDialog('Something Wrong!')
        else :
            self.errorDialog('No image can be exported!')

    # Export Label to csv
    def exportLabel(self):
        if self.current_img :
            file_name, _ = QFileDialog.getSaveFileName(self, "Save File", "", "CSV Files (*.csv)")
            if file_name:
                df = {'Name':[], 'Color':[], 'Type':[], 'Points(XY)':[]}
                for label_ in self.labelService.labelList.GetLabelList():
                    df['Name'].append(label_.GetName())
                    df['Color'].append(label_.GetLabelColor())
                    df['Type'].append(label_.GetLabelType())
                    # points to xy
                    ptlist = label_.GetPoint()
                    templist = []
                    for pt in ptlist:
                        tempX = pt.GetX()
                        tempY = pt.GetY()
                        templist.append([tempX, tempY])
                    df['Points(XY)'].append(templist)
                df = pd.DataFrame.from_dict(df)
                df.to_csv(file_name)
                print('exportLabel')
            else:
                self.errorDialog('Something Wrong!')
        else :
            self.errorDialog('No image can be exported!')

    # ============= message =============
    def errorDialog(self, msg):
        dlg = QMessageBox()
        dlg.setText(msg)
        button = dlg.exec()


