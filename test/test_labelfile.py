import unittest
import os, sys
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from biolabel.model.Point import Point
from biolabel.model.Label import Label
from biolabel.model.LabelList import LabelList
from biolabel.model.LabelFile import LabelFile

class LabelFileShouldBeCorrect(unittest.TestCase):
    def setUp(self):
        self.A = Point(10, 10)
        self.B = Point(30, 30)
        self.C = Point(20, 30)
        self.D = Point(40, 50)
        self.Label1 = Label("test1", "rect", [self.A, self.B])
        self.Label2 = Label("test2", "line", [self.C, self.D])
        self.Labellist = LabelList([self.Label1, self.Label2])
        self.LF = LabelFile(self.Labellist, fileLocation='C://secret/Test.json', fileFormat='COCO', fileName='Test', directory='C://secret')
    def tearDown(self):
        del self.A
        del self.B
        del self.C
        del self.D
        del self.Label1
        del self.Label2
        del self.Labellist
        del self.LF

    # self func
    def test_LabelFile_GetLabelInfo(self):
        expected = self.Labellist
        result = self.LF.GetLabelInfo()
        self.assertAlmostEqual(expected, result)

    # father class func
    def test_LabelFile_GetFileLocation(self):
        expected = 'C://secret/Test.json'
        result = self.LF.GetFileLocation()
        self.assertAlmostEqual(expected, result)

    def test_LabelFile_SetFileLocation(self):
        self.LF.SetFileLocation('D://Happy/Test.json')
        expected = 'D://Happy/Test.json'
        result = self.LF.GetFileLocation()
        self.assertAlmostEqual(expected, result)

    def test_LabelFile_GetFileFormat(self):
        expected = 'COCO'
        result = self.LF.GetFileFormat()
        self.assertAlmostEqual(expected, result)

    def test_LabelFile_SetFileFormat(self):
        self.LF.SetFileFormat('BIO')
        expected = 'BIO'
        result = self.LF.GetFileFormat()
        self.assertAlmostEqual(expected, result)

    def test_LabelFile_GetFileName(self):
        expected = 'Test'
        result = self.LF.GetFileName()
        self.assertAlmostEqual(expected, result)

    def test_LabelFile_SetFileName(self):
        self.LF.SetFileName('Given')
        expected = 'Given'
        result = self.LF.GetFileName()
        self.assertAlmostEqual(expected, result)

    def test_LabelFile_GetDirectory(self):
        expected = 'C://secret'
        result = self.LF.GetDirectory()
        self.assertAlmostEqual(expected, result)

    def test_LabelFile_SetDirectory(self):
        self.LF.SetDirectory('D://Luffy')
        expected = 'D://Luffy'
        result = self.LF.GetDirectory()
        self.assertAlmostEqual(expected, result)
