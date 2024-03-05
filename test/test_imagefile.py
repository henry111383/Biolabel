import unittest
import os, sys
import cv2
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from biolabel.model.Image import Image
from biolabel.model.ImageFile import ImageFile

class ImageFileShouldBeCorrect(unittest.TestCase):
    def setUp(self):
        self.temp = cv2.cvtColor(cv2.imread('hook.png'), cv2.COLOR_BGR2RGB)
        self.Image = Image(value=self.temp, channel='RGB', imageName='Test') 
        self.IF = ImageFile(self.Image, fileLocation='C://secret/Test.json', fileFormat='COCO', fileName='Test', directory='C://secret')
    
    def tearDown(self):
        del self.temp
        del self.Image
        del self.IF

    # self func
    def test_ImageFile_GetImgInfo(self):
        expected = self.Image
        result = self.IF.GetImgInfo()
        self.assertAlmostEqual(expected, result)

    def test_ImageFile_SetImgInfo(self):
        temp = cv2.cvtColor(cv2.imread('HE.png'), cv2.COLOR_BGR2RGB)
        Image2 = Image(value=temp, channel='RGB', imageName='Test') 
        expected = Image2
        self.IF.SetImgInfo(Image2)
        result = self.IF.GetImgInfo()
        self.assertAlmostEqual(expected, result)

    # father class func
    def test_ImageFile_GetFileLocation(self):
        expected = 'C://secret/Test.json'
        result = self.IF.GetFileLocation()
        self.assertAlmostEqual(expected, result)

    def test_ImageFile_SetFileLocation(self):
        self.IF.SetFileLocation('D://Happy/Test.json')
        expected = 'D://Happy/Test.json'
        result = self.IF.GetFileLocation()
        self.assertAlmostEqual(expected, result)

    def test_ImageFile_GetFileFormat(self):
        expected = 'COCO'
        result = self.IF.GetFileFormat()
        self.assertAlmostEqual(expected, result)

    def test_ImageFile_SetFileFormat(self):
        self.IF.SetFileFormat('BIO')
        expected = 'BIO'
        result = self.IF.GetFileFormat()
        self.assertAlmostEqual(expected, result)

    def test_ImageFile_GetFileName(self):
        expected = 'Test'
        result = self.IF.GetFileName()
        self.assertAlmostEqual(expected, result)

    def test_ImageFile_SetFileName(self):
        self.IF.SetFileName('Given')
        expected = 'Given'
        result = self.IF.GetFileName()
        self.assertAlmostEqual(expected, result)

    def test_ImageFile_GetDirectory(self):
        expected = 'C://secret'
        result = self.IF.GetDirectory()
        self.assertAlmostEqual(expected, result)

    def test_ImageFile_SetDirectory(self):
        self.IF.SetDirectory('D://Luffy')
        expected = 'D://Luffy'
        result = self.IF.GetDirectory()
        self.assertAlmostEqual(expected, result)
