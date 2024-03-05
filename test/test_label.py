import unittest
import os, sys
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))

from biolabel.model.Point import *
from biolabel.model.Label import *

class Label_RectLabelShouldBeCorrect(unittest.TestCase):
    def setUp(self):
        self.A = Point(10,10)
        self.B = Point(30,30)
        self.C = Point(20,30)
        self.D = Point(40,50)
        self.E = Point(100,100)
        self.RectLabel1 = Label('RectLabel1', 'rect' , "#ffffff" ,[self.A, self.B])
        self.RectLabel2 = Label('RectLabel2', 'rect', "#ffffff" ,[self.C, self.D])
        # self.RectLabel3 = Label('RectLabel2', 'point',[self.C])
        # self.RectLabel4 = Label('RectLabel2', 'point',[self.C])
        

    def tearDown(self):
        del self.A
        del self.B
        del self.C
        del self.D
        del self.E
        del self.RectLabel1
        del self.RectLabel2
        

    def test_RectLabel1_getPointList(self):
        expected = [self.A, self.B]
        result = self.RectLabel1.GetPoint()
        self.assertEqual(expected, result)

    def test_RectLabel2_getPointList(self):
        expected = [self.C, self.D]
        result = self.RectLabel2.GetPoint()
        self.assertEqual(expected, result)

    def test_Polygon_AddPoint(self):
        expected = [self.A, self.B, self.E]
        self.RectLabel1.AddPoint(self.E)
        result = self.RectLabel1.GetPoint()
        self.assertEqual(expected, result)

    def test_Polygon_Remove(self):
        expected = [self.A]
        self.RectLabel1.RemovePoint(1)
        result = self.RectLabel1.GetPoint()
        self.assertEqual(expected, result)

    def test_Polygon_UpdatePoint(self):
        expected = [self.A, self.C, self.E]
        self.RectLabel1.AddPoint(self.E)
        self.RectLabel1.UpdatePoint(1, self.C)
        result = self.RectLabel1.GetPoint()
        self.assertEqual(expected, result)
    
    def test_Label_GetName(self):
        expected = "RectLabel1"
        result = self.RectLabel1.GetName()
        self.assertEqual(expected, result)

    def test_Label_SetName(self):
        expected = "Test"
        self.RectLabel1.SetName("Test")
        result = self.RectLabel1.GetName()
        self.assertEqual(expected, result)

    def test_Label_GetLabelType(self):
        expected = 'rect'
        result = self.RectLabel1.GetLabelType()
        self.assertEqual(expected, result)
