from .Label import Label
from .Point import Point
from .LabelList import LabelList
class LabelService():
    def __init__(self):
        self.NameList = set()
        self.labelList = LabelList([])

    def CreateLabel(self, name, type, Color, ptList)->Label:
        self.NameList.add(name)
        return Label(name=name, type=type, color=Color, ptList=ptList)
    
    def moveLabel(self, ptlist , Label)->Label:
        for index , pt in enumerate(ptlist):
            Label.UpdatePoint(index,Point(pt.x(),pt.y()))
        return Label
    
    def EditLabelName(self, Name, Label)->Label:
        Label.SetName(Name)
        return Label
    
    def EditLabelColor(self, color, Label)->Label:
        Label.SetLabelColor(color)
        return Label
    
    def DeleteLabel(self , label ) :
        try:
            self.labelList.RemoveLabel(label)
            return True
        except:
            print('Error! Not Found This Label')
            return False
    