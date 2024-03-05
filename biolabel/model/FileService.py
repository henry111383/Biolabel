from .File import File
from .ImageFile import ImageFile
from .LabelFile import LabelFile
from .LabelList import LabelList
from .Image import Image
import os
import cv2
import json
class FileService():
    def __init__(self):
        pass

    def StoreImage(self, IF:ImageFile, fileLocation:str)-> bool:
        img = IF.GetImgInfo().GetImg()
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        try:
            cv2.imwrite(fileLocation, img)
            return True
        except:
            return False


    def LoadImage(self, fileLocation:str)-> Image:
        # read image
        try:
            img = cv2.cvtColor(cv2.imread(fileLocation), cv2.COLOR_BGR2RGB)
            # create Image instance
            return Image(img, channel='RGB', imageName='Original')
        except:
            print('Error! Wrong format!')
            return None
        

    def StoreLabel(self, LF:LabelFile, format:str)-> bool:
        MyJson = {}
        labellist = LF.GetLabelInfo().GetLabelList()
        for index, label in enumerate(labellist):
            Name = label.GetName()
            Color = label.GetLabelColor()
            Type = label.GetLabelType()
            PointList =  label.GetPoint()
            Points = []
            for pt in PointList:
                Points.append([pt.GetX(), pt.GetY()])
            LabelDict={'Name': Name, 'Color': Color, 'Type': Type, 'Points': Points}

            MyJson[index] = LabelDict
        json_data = json.dumps(MyJson, indent=4)
        with open(LF.GetFileLocation(), "w") as file:
            file.write(json_data)
        return
        

    
    def LoadUILabel(self, fileLocation:str)-> dict:
        if os.path.exists(fileLocation):
            # print('Json Exists!')
            with open(fileLocation) as f:
                data = json.load(f)
                try :
                    if ["Name", "Color", "Type", "Points"] == list(data['0'].keys()):
                        # print('is Our JSON')
                        return data
                    else :
                        # print('not our JSON')
                        return dict()
                except :
                    return dict()
        else: # file doesnt exists 
            print('Json doesnt Exists!')
            return dict()
        

    def ConvertLabel2File(self, label:LabelList )-> LabelFile: 
        return LabelFile(labelList=label)
        
    def ConvertImage2File(self, img:Image) -> ImageFile:
        return ImageFile(image=img)
