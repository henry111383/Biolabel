import unittest
import os, sys
import PyQt5
from  PyQt5 import QtCore
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))

from biolabel.model.LabelService import *
from biolabel.model.Label import *
class LabelService_LabelServiceShouldBeCorrect(unittest.TestCase):
    def setUp(self):
        self.LabelService = LabelService()
        self.A = Point(10,10)
        self.B = Point(30,30)
        self.C = Point(20,30)
        self.D = Point(40,50)
        self.E = Point(100,100)
        self.PolyLabel1 = Label('poly1', 'poly', '#ffffff' ,[self.A, self.B, self.E])
        self.RectLabel2 = Label('RectLabel2', 'rect' , '#ffffff' ,[self.C, self.D])

    def tearDown(self):
        del self.A
        del self.B
        del self.C
        del self.D 
        del self.E
        del self.PolyLabel1 
        del self.RectLabel2
        
    def test_LabelService_CreateLabel(self):
        ExpectName = 'poly1'
        ExpectType = 'poly'
        ExpectColor = '#ffffff'
        ExpectptList = [self.A, self.B, self.E]
        NewLabel = self.LabelService.CreateLabel(ExpectName, ExpectType,ExpectColor, ExpectptList)
        self.assertEqual(ExpectName ,NewLabel.GetName())
        self.assertEqual(ExpectType ,NewLabel.GetLabelType())
        self.assertEqual(ExpectColor ,NewLabel.GetLabelColor())
        self.assertEqual(ExpectptList ,NewLabel.GetPoint())

    def test_LabelService_MoveLabelAllePoint(self):
        ExceptPoint0 = PyQt5.QtCore.QPointF(20,20)
        ExceptPoint1 = PyQt5.QtCore.QPointF(40,40)
        ExceptPoint2 = PyQt5.QtCore.QPointF(110,110)
        moveptList = [ExceptPoint0,ExceptPoint1,ExceptPoint2]
        MoveLabel = self.LabelService.moveLabel(moveptList,self.PolyLabel1)
        ptList =  MoveLabel.GetPoint()
        self.assertEqual(ExceptPoint0.x() , ptList[0].GetX())
        self.assertEqual(ExceptPoint0.y() , ptList[0].GetY())
        self.assertEqual(ExceptPoint1.x() , ptList[1].GetX())
        self.assertEqual(ExceptPoint1.y() , ptList[1].GetY())
        self.assertEqual(ExceptPoint2.x() , ptList[2].GetX())
        self.assertEqual(ExceptPoint2.y() , ptList[2].GetY())

    def test_LabelService_EditLabelName(self):
        Name = "RectLabel1"
        EditLabel = self.LabelService.EditLabelName(Name,self.RectLabel2)
        self.assertEqual(Name , EditLabel.GetName())

    def test_LabelService_EditLabelColor(self):
        Color = "#00ff00"
        EditLabel = self.LabelService.EditLabelColor(Color,self.RectLabel2)
        self.assertEqual(Color , EditLabel.GetLabelColor())

    def test_LabelService_DeleteLabel(self):
        self.LabelService.labelList.AddLabel(self.PolyLabel1)
        self.LabelService.labelList.AddLabel(self.RectLabel2)
        self.LabelService.DeleteLabel(self.PolyLabel1)
        self.assertEqual(self.RectLabel2 , self.LabelService.labelList.GetLabelList()[0])
        self.assertEqual(1 , len(self.LabelService.labelList.GetLabelList()))

   