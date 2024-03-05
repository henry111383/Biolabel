import unittest
import os
import sys
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))

from biolabel.model.LabelList import *
from biolabel.model.Label import *
from biolabel.model.Point import *


class LabelListTest(unittest.TestCase):
    def setUp(self):
        self.A = Point(10, 10)
        self.B = Point(30, 30)
        self.C = Point(20, 30)
        self.D = Point(40, 50)
        self.Label1 = Label("test1", "rect", [self.A, self.B])
        self.Label2 = Label("test2", "line", [self.C, self.D])
        self.Labellist = LabelList([self.Label1, self.Label2])

    def tearDown(self):
        del self.A
        del self.B
        del self.C
        del self.D
        del self.Label1
        del self.Label2

    def test_GetLabelList(self):
        result = self.Labellist.GetLabelList()
        self.assertEqual(self.Label1, result[0])
        self.assertEqual(self.Label2, result[1])

    def test_ReviseLabel(self):
        new_Label = Label("test3", "poly", [self.A, self.C])
        self.Labellist.ReviseLabel(0,new_Label)
        result = self.Labellist.GetLabelList()
        self.assertEqual(new_Label, result[0])
        self.assertEqual(self.Label2, result[1])
    def test_AddLabel(self):
        new_Label = Label("test3", "poly", [self.A, self.C])
        self.Labellist.AddLabel(new_Label)
        result = self.Labellist.GetLabelList()
        self.assertEqual(self.Label1, result[0])
        self.assertEqual(self.Label2, result[1])
        self.assertEqual(new_Label, result[2])
    
    def test_ClearAllLabel(self):
        self.Labellist.ClearAllLabel()
        result = self.Labellist.GetLabelList()
        self.assertEqual(0,len(result))
