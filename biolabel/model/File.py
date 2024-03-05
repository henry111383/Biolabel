
class File():
    def __init__(self, \
                    fileLocation=None, \
                    fileName=None, \
                    fileFormat=None, \
                    directory=None, \
                ):
        self.__FileLocation = fileLocation
        self.__FileName = fileName 
        self.__FileFormat = fileFormat
        self.__Directory = directory

    # getter
    def GetFileLocation(self):
        return self.__FileLocation
    
    def GetFileName(self):
        return self.__FileName
    
    def GetFileFormat(self):
        return self.__FileFormat
    
    def GetDirectory(self):
        return self.__Directory

    # setter
    def SetFileLocation(self, str):
        self.__FileLocation = str
    
    def SetFileName(self, str):
        self.__FileName = str
    
    def SetFileFormat(self, str):
        self.__FileFormat = str
    
    def SetDirectory(self, str):
        self.__Directory = str
    
