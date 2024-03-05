import unittest
import os, sys
import numpy as np
import cv2

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))

from biolabel.model.File import File
from biolabel.model.Image import Image
from biolabel.model.LabelFile import LabelFile
from biolabel.model.ImageFile import ImageFile
from biolabel.model.Label import Label
from biolabel.model.LabelList import LabelList
from biolabel.model.Point import Point
from biolabel.model.FileService import FileService


class File_FileServiceShouldBeCorrect(unittest.TestCase):
    def setUp(self):
        self.pointA = Point(3, 4)
        self.pointB = Point(10, 10)
        self.pointC = Point(12, 14)
        self.img = cv2.cvtColor(cv2.imread('HE.png'), cv2.COLOR_BGR2RGB)
        self.img = Image(self.img)
        self.labelA = Label(name='labelA', type='rect', color="#ff0000", ptList=[self.pointA, self.pointB])
        self.labelB = Label(name='labelB', type='rect', color="#00ff00", ptList=[self.pointC, self.pointA, self.pointB])
        self.ll = LabelList()
        self.ll.AddLabel(self.labelA)
        self.ll.AddLabel(self.labelB)
        self.FS = FileService()
        
    def tearDown(self):
        del self.pointA
        del self.pointB
        del self.pointC
        del self.labelA
        del self.labelB
        self.ll.ClearAllLabel()
        del self.ll
    
    def test_ConvertLabel2FileShouldbeCorrect(self):
        testLabelFile = self.FS.ConvertLabel2File(label=self.ll)
        self.assertTrue(isinstance(testLabelFile, LabelFile))
        
    def test_ConvertLabel2FileAndInfoShouldbeCorrect(self):
        testLabelFile = self.FS.ConvertLabel2File(label=self.ll)
        expected = self.ll
        result = testLabelFile.GetLabelInfo()
        self.assertEqual(expected, result)

    def test_ConvertImage2FileShouldbeCorrect(self):
        testImgFile = self.FS.ConvertImage2File(img=self.img)
        self.assertTrue(isinstance(testImgFile, ImageFile))

    def test_ConvertImage2FileAndInfoShouldbeCorrect(self):
        testImgFile = self.FS.ConvertImage2File(img=self.img)
        expected = self.img
        result = testImgFile.GetImgInfo()
        self.assertEqual(expected, result)

    def test_StoreImageShouldbeCorrect(self):
        Location = 'for_FStest.png'
        IF = self.FS.ConvertImage2File(img=self.img)
        self.FS.StoreImage(IF=IF, fileLocation=Location)
        self.assertTrue(os.path.isfile(Location))
        os.remove(Location)

    def test_LoadImageShouldbeCorrect(self):
        Location = 'HE.png'
        tempImg = self.FS.LoadImage(Location)
        self.assertTrue(isinstance(tempImg, Image))

    def test_StoreLabelShouldbeCorrect(self):
        Location = 'test/for_FStest.json'
        format = 'My'
        testLabelFile = self.FS.ConvertLabel2File(label=self.ll)
        testLabelFile.SetFileLocation(Location)
        self.FS.StoreLabel(LF=testLabelFile, format=format)
        self.assertTrue(os.path.isfile(Location))

    def test_LoadUILabelShouldbeCorrect(self):
        Location = 'test/for_FStest.json'
        myDict = self.FS.LoadUILabel(fileLocation=Location)
        self.assertTrue(isinstance(myDict, dict))

    def test_LoadUILabelAndFormatShouldbeCorrect(self):
        Location = 'test/for_FStest.json'
        myDict = self.FS.LoadUILabel(fileLocation=Location)
        expected = ["Name", "Color", "Type", "Points"]
        result = list(myDict['0'].keys())
        self.assertEqual(expected, result)

    def test_LoadUILabelAndLengthInfoShouldbeCorrect(self):
        Location = 'test/for_FStest.json'
        myDict = self.FS.LoadUILabel(fileLocation=Location)
        expected = 2
        result = len(myDict)
        self.assertEqual(expected, result)

    def test_LoadUILabelAndLabelNameInfoShouldbeCorrect(self):
        Location = 'test/for_FStest.json'
        myDict = self.FS.LoadUILabel(fileLocation=Location)
        expected = ['labelA', 'labelB']
        result = []
        for i in range(len(myDict)):
            result.append(myDict[str(i)]['Name'])
        self.assertEqual(expected, result)

    def test_LoadUILabelAndLabelTypeInfoShouldbeCorrect(self):
        Location = 'test/for_FStest.json'
        myDict = self.FS.LoadUILabel(fileLocation=Location)
        expected = ['rect', 'rect']
        result = []
        for i in range(len(myDict)):
            result.append(myDict[str(i)]['Type'])
        self.assertEqual(expected, result)

    def test_LoadUILabelAndLabelColorInfoShouldbeCorrect(self):
        Location = 'test/for_FStest.json'
        myDict = self.FS.LoadUILabel(fileLocation=Location)
        expected = ['#ff0000', '#00ff00']
        result = []
        for i in range(len(myDict)):
            result.append(myDict[str(i)]['Color'])
        self.assertEqual(expected, result)

    def test_LoadUILabelAndLabelPointInfoShouldbeCorrect(self):
        Location = 'test/for_FStest.json'
        myDict = self.FS.LoadUILabel(fileLocation=Location)
        expected = [[[3, 4], [10, 10]], [[12, 14], [3, 4], [10, 10]]]
        result = []
        for i in range(len(myDict)):
            result.append(myDict[str(i)]['Points'])
        self.assertEqual(expected, result)


