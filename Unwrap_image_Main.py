import os
import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
from Utils import *
from skimage.morphology import skeletonize, thin
from Kernal_operation_new import *
from Unwrap_runner import *
from Pre_process_battery import * ## make sure to remove this if a new preprocessing step is made for the battery like objects.


folder  =
file =                     # tif file

## List of argument to change are given next to each line of code. Kindly check https://github.com/jaianthv/Unwrapping-tomography-images/blob/main/README.md for detailed instructions
## Make to to comment other lines which are not going to tbe used.

#### Unwrap single file


raw_image, first = get_image_raw_first(folder, file,None) # replace None with "c" or "C" for contour based extraction
unwrap_image = unwrap_layers(150, first, raw_image, None) ## change no of layers the first argument




#### Unwrap folder as a single process

#unwrap_folder_single_process(folder, 10, use_layer_point=None, border_type=None, destination_folder=None) # Change number of layers second argument, change border_typre = "C" or "c" if you prefer contour based extraction



#### Unwrap folder as a multiple process

#if __name__ == '__main__':
#    unwrap_folder_multi_process(2, folder, 40, use_layer_point=None, border_type=None, destination_folder=None) # first argument - number of processes, third argument - no of layers to unwrap, # border_type




#### fast unwrap a single file

#raw_image, first = get_image_raw_first(folder, file)
#unwrap_single_multiline_closed(first, raw_image, 10) # third argument - number of layers to extract


#### fast unwrap folder as a single process

#unwrap_folder_multiline_closed_single_process(folder, 10, border_type=None, destination_folder=None) # second argument - number of layers to extract,thirdt border type, 


#### fast unwrap folder as a multiprocess

#if __name__ == '__main__':
#    unwrap_folder_multiline_closed_multi_process(2, folder, 10, border_type=None, destination_folder=None)



#### unwrap open ends single image with preprocessing combined

#os.chdir(folder)
#image = cv.imread(file,-1)
#shape_image, open_points = get_shape(image)
#unwrap_image_multiline_open(shape_image, image, 50)

















