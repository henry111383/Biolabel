from .File import *

class LabelFile(File):
    def __init__(self, labelList,\
                    fileLocation=None, \
                    fileName=None, \
                    fileFormat=None, \
                    directory=None, \
                    parent=None):
        super(LabelFile, self).__init__(fileLocation, fileName, fileFormat, directory)
        self.__LabelInfo = labelList

    # getter
    def GetLabelInfo(self):
        return self.__LabelInfo
    
    # setter
    def SetLabelInfo(self, labelList):
        self.__LabelInfo = labelList
