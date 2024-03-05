import numpy as np

class Image():
    def __init__(self, value=np.ndarray([]), channel=None, imageName=None):
        self.__Value = value
        self.__Size = np.shape(self.__Value)
        self.__Channel = channel
        self.__ImageName = imageName

    def SetName(self, ImageName):
        self.__ImageName = ImageName
        return
    
    def GetName(self):
        return self.__ImageName
    
    def SetImg(self, img, channelName='RGB'):
        self.__Value = img
        self.__Channel = channelName

    def GetImg(self):
        return self.__Value

    def GetSize(self):
        return self.__Size
    
    def SetChannel(self, str):
        self.__Channel = str

    def GetChannel(self):
        return self.__Channel
    
    

