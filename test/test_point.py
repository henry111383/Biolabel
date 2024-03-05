import unittest
import os, sys
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))

from biolabel.model.Point import Point

class Point_PointShouldBeCorrect(unittest.TestCase):
    def setUp(self):
        self.pt1 = Point(3,4)
        self.pt2 = Point(0,0)

    def tearDown(self):
        del self.pt1
        del self.pt2

    def test_pt1_SetX(self):
        expected = 3
        result = self.pt1.GetX()
        self.assertAlmostEqual(expected, result)

    def test_pt1_GetY(self):
        expected = 4
        result = self.pt1.GetY()
        self.assertAlmostEqual(expected, result)

    def test_pt2_GetX(self):
        expected = 0
        result = self.pt2.GetX()
        self.assertAlmostEqual(expected, result)

    def test_pt2_GetY(self):
        expected = 0
        result = self.pt2.GetY()
        self.assertAlmostEqual(expected, result)

    def test_Distance(self):
        expected = 5
        result = self.pt1.Distance(self.pt2)


