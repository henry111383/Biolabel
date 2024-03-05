
class Label():
    def __init__(self, name=None, type=None, color="#ff0000", ptList=[]):
        self.__LabelName = name
        self.__LabelType = type
        self.__ptList = ptList
        self.__LabelColor = color

    def GetPoint(self):
        return self.__ptList
    
    def AddPoint(self, pt):
        self.__ptList.append(pt)
        return
    
    def RemovePoint(self, index):
        if index :
            if len(self.__ptList) > index:
                del self.__ptList[index]
        return
    
    def UpdatePoint(self, index, pt):
        if len(self.__ptList) > index:
            del self.__ptList[index]
            self.__ptList.insert(index, pt)
        return
    
    def GetName(self):
        return self.__LabelName
    
    def SetName(self, name):
        self.__LabelName = name
        return
        
    def GetLabelType(self):
        return self.__LabelType
    
    def GetLabelColor(self):
        return self.__LabelColor
    
    def SetLabelColor(self, color):
        self.__LabelColor = color
        return
