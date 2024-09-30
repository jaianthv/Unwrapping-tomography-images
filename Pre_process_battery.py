import numpy as np
import matplotlib.pyplot as plt
import cv2 as cv
import os
from skimage.morphology import skeletonize, thin
from PIL import Image, ImageFilter
#from Kernel_operation import *
import multiprocessing as mp
from Utils import *





def get_shape(im):
    image = im.copy()
    retval, image = cv.threshold(image,0,1,cv.THRESH_BINARY)
    kernel = np.ones((25,25),np.uint8)
    image_1 = cv.dilate(image,kernel,iterations = 1)

    tt =thin(image_1)
     
    tt = np.array(tt, dtype=np.float32)

    img = remove_protruding_open_ends(tt)
    
       
    end_position = np.where(img==1) 

    retval, img = cv.threshold(img,0,1,cv.THRESH_BINARY)
    return img, end_position
