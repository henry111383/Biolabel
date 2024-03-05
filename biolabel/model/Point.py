import math

class Point(object):
    def __init__(self, x, y):
        self.__X = x
        self.__Y = y

    def SetX(self, x):
        self.__X = x
        return
    
    def SetY(self, y):
        self.__Y = y
        return

    def GetX(self)->float:
        return self.__X 
    
    def GetY(self)->float:
        return self.__Y
    
    def Distance(self, pt)->float:
        dis = math.sqrt( math.pow(self.GetX()-pt.GetY(), 2) + math.pow(self.GetY()-pt.GetY(), 2) )
        return dis