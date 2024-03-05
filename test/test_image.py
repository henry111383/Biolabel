import unittest
import os, sys
import cv2
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))

from biolabel.model.Image import *

class Image_ImageShouldBeCorrect(unittest.TestCase):
    def setUp(self):
        self.temp = cv2.cvtColor(cv2.imread('hook.png'), cv2.COLOR_BGR2RGB)
        self.img1 = Image(value=self.temp, channel='RGB', imageName='Test') 

    def tearDown(self):
        del self.img1
        
    def test_Image_GetImg(self):
        expected = self.temp
        result = self.img1.GetImg()
        self.assertEqual(expected.all(), result.all())

    def test_Image_SetImg(self):
        expected = np.ndarray([])
        self.img1.SetImg(expected)
        result = self.img1.GetImg()
        self.assertEqual(expected.all(), result.all())

    def test_Image_SetName(self):
        expected = 'OK'
        self.img1.SetName('OK')
        result = self.img1.GetName()
        self.assertEqual(expected, result)
    
    def test_Image_GetName(self):
        expected = 'Test'
        result = self.img1.GetName()
        self.assertEqual(expected, result)

    def test_Image_GetSize(self):
        expected = (640, 586, 3)
        result = self.img1.GetSize()
        self.assertEqual(expected, result)
    
    def test_Image_SetChannel(self):
        expected = 'HED'
        self.img1.SetChannel('HED')
        result = self.img1.GetChannel()
        self.assertEqual(expected, result)

    def test_Image_GetChannel(self):
        expected = 'RGB'
        result = self.img1.GetChannel()
        self.assertEqual(expected, result)

    
    


  