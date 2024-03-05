from .Image import Image
import numpy as np
import cv2
import PIL.Image
import skimage 

class ImageProcessService():
    def __init__(self, img=Image()):
        pass
        
    def RGB2Gray(self, img):
        value = cv2.cvtColor(img.GetImg(), cv2.COLOR_RGB2GRAY)
        value = np.stack((value, value, value), axis=-1)
        return Image(value, channel='gray', imageName='RGB2Gray') 
        
    def OTSUbinary(self, img):
        value = cv2.cvtColor(img.GetImg(), cv2.COLOR_RGB2GRAY)
        binary_val = cv2.threshold(value, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)[1]
        binary_val = np.stack((binary_val, binary_val, binary_val), axis=-1)
        return Image(binary_val, channel='binary', imageName='OTSUbinary')

    def RGB2Hematoxylin(self, img):
        value = img.GetImg()
        null = np.zeros_like(value[:, :, 0])
        Hematoxylin = skimage.color.rgb2hed(value)
        Hematoxylin = skimage.color.hed2rgb(np.stack((Hematoxylin[:, :, 0], null, null), axis=-1))
        Hematoxylin = np.round(Hematoxylin*255).astype(np.uint8)
        return Image(Hematoxylin, channel='Hematoxylin', imageName='RGB2Hematoxylin')
            

    def RGB2Eosin(self, img):
        value = img.GetImg()
        null = np.zeros_like(value[:, :, 0])
        Eosin = skimage.color.rgb2hed(value)
        Eosin = skimage.color.hed2rgb(np.stack((null, Eosin[:, :, 1], null), axis=-1))
        Eosin = np.round(Eosin*255).astype(np.uint8)
        return Image(Eosin, channel='Eosin', imageName='RGB2Eosin')


    def RGB2Dab(self, img):
        value = img.GetImg()
        null = np.zeros_like(value[:, :, 0])
        Dab = skimage.color.rgb2hed(value)
        Dab = skimage.color.hed2rgb(np.stack((null, null, Dab[:, :, 2]), axis=-1))
        Dab = np.round(Dab*255).astype(np.uint8)
        return Image(Dab, channel='Dab', imageName='RGB2Dab')