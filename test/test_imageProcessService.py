import unittest
import os, sys
import cv2
import numpy as np
import skimage 

import matplotlib.pyplot as plt
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))

from biolabel.model.ImageProcessService import *
from biolabel.model.Image import *

class ImageProcessService_ImageProcessServiceShouldBeCorrect(unittest.TestCase):
    def setUp(self):
        self.temp = cv2.cvtColor(cv2.imread('IHC.png'), cv2.COLOR_BGR2RGB)
        self.imageProcessService = ImageProcessService()
        self.img1 = Image(value=self.temp, channel='RGB', imageName='Test') 
        value = cv2.cvtColor(cv2.imread('IHC.png'), cv2.COLOR_BGR2GRAY)
        self.tempGray = np.stack((value, value, value), axis=-1)
        self.img2 = Image(value=self.tempGray, channel='gray', imageName='Test') 
        Bin_value = cv2.threshold(value, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)[1]
        self.tempBin = np.stack((Bin_value, Bin_value, Bin_value), axis=-1)
        null = np.zeros_like(self.temp[:, :, 0])
        self.HED = skimage.color.rgb2hed(self.temp)
        self.tempH = skimage.color.hed2rgb(np.stack((self.HED[:, :, 0], null, null), axis=-1))
        self.tempE = skimage.color.hed2rgb(np.stack((null, self.HED[:, :, 1], null), axis=-1))
        self.tempD = skimage.color.hed2rgb(np.stack((null, null, self.HED[:, :, 2]), axis=-1))

    def tearDown(self):
        del self.imageProcessService
        del self.img1
        del self.img2
        
    def test_ImageProcessService_RGB2Gray(self):
        expected = self.tempGray
        processed_img = self.imageProcessService.RGB2Gray(self.img1)
        result = processed_img.GetImg()
        self.assertEqual(expected.all(), result.all())
        self.assertEqual(processed_img.GetChannel(), 'gray')
        self.assertEqual(processed_img.GetName(), 'RGB2Gray')
        del processed_img


    def test_ImageProcessService_OTSUbinary(self):
        expected = self.tempBin
        processed_img = self.imageProcessService.OTSUbinary(self.img2)
        result = processed_img.GetImg()
        self.assertEqual(expected.all(), result.all())
        self.assertEqual(processed_img.GetChannel(), 'binary')
        self.assertEqual(processed_img.GetName(), 'OTSUbinary')
        del processed_img


    def test_ImageProcessService_RGB2Hematoxylin(self):
        expected = self.tempH
        processed_img = self.imageProcessService.RGB2Hematoxylin(self.img1)
        result = processed_img.GetImg()
        self.assertEqual(expected.all(), result.all())
        self.assertEqual(processed_img.GetChannel(), 'Hematoxylin')
        self.assertEqual(processed_img.GetName(), 'RGB2Hematoxylin')
        del processed_img


    def test_ImageProcessService_RGB2Eosin(self):
        expected = self.tempE
        processed_img = self.imageProcessService.RGB2Eosin(self.img1)
        result = processed_img.GetImg()
        self.assertEqual(expected.all(), result.all())
        self.assertEqual(processed_img.GetChannel(), 'Eosin')
        self.assertEqual(processed_img.GetName(), 'RGB2Eosin')
        del processed_img


    def test_ImageProcessService_RGB2Dab(self):
        expected = self.tempD
        processed_img = self.imageProcessService.RGB2Dab(self.img1)
        result = processed_img.GetImg()
        self.assertEqual(expected.all(), result.all())
        self.assertEqual(processed_img.GetChannel(), 'Dab')
        self.assertEqual(processed_img.GetName(), 'RGB2Dab')
        del processed_img


  