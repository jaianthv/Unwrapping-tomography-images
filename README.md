# Unwrapping-tomography-images
The unwrapping codes developed can digitally unroll 2D slices of a 3D object measured by a tomography technique. Few associated functions can be used identify only external surface and characterize surface roughness.





<IMG SRC="Media1.gif" height="500" width="900"><br>

## List of python modules needed
1. Numpy
2. OpenCV
3. Pillow (PIL)
4. matplotlib
5. skimage
6. multiprocessing
7. os
8. sys

## List of python scripts
1. Utils.py - contains functions required for preprocessing the image.
   
2. Kernel_operation.py - contains funtions required to perform kernel operation and analyze the result. Contains list of if statements. Please refer the manuscript.
   
3. Unwrap_runner.py - Contains functions which by using Kernel_operation.py unwraps the given image.<br>
   
4. Unwrap_image_New.py - Contains example codes which uses the functions in Unwrap_runner.py to unwrap single image or list of images in the folder. One can simply use this code to run the unwrapping procedure.<br>


## List of functions available
### *Utils.py*
1.	`get_center(image, str)` <br>
image = np.array <br>
str = “Show” to display image or None <br>
returns *cx,cy* - coordinates of center of mass <br>

2.	`Clean_small_contours(list(contours))`<br>
list(contours) - obtained from cv.findContours <br>
returns  *new list of contours* - after removing the smaller ones <br>

3. `check_single_contour_new(image)`<br>
image = np.array, binary 0 (background) and 1 (object). Hollow objects also works, e.g. segmented coating layer like. <br>
returns *Updated contour points, number of dilation performed* <br>
Note - For the very first reference layer, the matrix kernel for dilation is kept at 5 x 5, this will make sure that the reference layer is little outside the edge of the object. <br>  

4. `correct_check_single_contour(image, contours, k_i)`<br>
image = np.array, binary, just to make an empty image<br>
contours = updated contours from `check_single_contour_new` <br>
k_i = kernel size, default = 5 <br>
returns *corrected outer layer with contour drawn (2D array), new contour compensating for the dilation*

5. `check_eight_point_convol_op(img)`<br>
img = np.array - any line with line width 1, dtype=np.uint8, line value should be 1 and rest should be 0.<br>
Checks if there are any points with 4-point connectivity<br>
returns *True/False*

6. `correct_by_thin(img)`<br>
img = np.array = any line with line with/without width 1, dtype=np.uint8, line value should be 1 and rest should be 0.<br>
returns *thin image with 8-point connectivity*

7. `check_open_ends_convol_op(img)`<br>
img = np.array - line with width 1, dtype=np.uint8, line value should be 1 and rest should be 0.<br>
returns *True - if there are open ends/ false - otherwise*

8. `remove_defects(img, unique, counts, kernel)`<br>
It is a nested function of `remove_protruding ends` - can be modified if new kernel is developed. Mainly used to remove isolated pixels. To some extent removes non-eight point connectivity pixels. <br>
img = np.array - with defective line image with line width as 1, line value should be 1 and rest should be zero <br>
unique = list of unique elements obtained from np.unique.<br>
counts = list of counts from the elements obtained from np.unique.<br>
kernel = default - [[1,1,1],[1,0,1],[1,1,1]] <br>
returns *Image - after removing defective pixels.*

9. `remove_protruding_open_ends(img)`<br>
Other functions required - `check_open_ends_convol_op`, `remove_defects` <br>
Iterates (default - 80 iterations) apply kernel - [[-1,-1,-1],[-1,1,-1],[-1,-1,-1]], multiply with original image, convert to absolute value, remove every pixel value above "1" (protruding pixels). After each iteration check if any protruding ends are present by `check_open_ends_convol_op`. If no open ends are present, returns the corrected image. <br>
returns *corrected image*

10. `get_first_point(img)` <br>
img = image with line after correcting for defects. Requires function `find_point`.
returns *coordinates of a starting point*

11. `findpoint(img, cx,cy)` <br>
img = image <br>
cx, cy = coorinates of the center of mass of the sample, type = int.<br>
From the center of the image, this functions draws a line horizontally to the left. The point where it overlaps with reference line from the object is considered as the starting point. <br>
returns *x_coordinate, y_coordinate*

12. `get_start_end_open_end(img)`<br>
img = spiral structure or line with two open end (start and end) <br>
This function identifies the open ends. Then by using function `determine_points` identifies start and the end points. By default the point closer to the origin [0,0] of the image, top left corner is considered start point. One can change this if needed.
returns *start point coordinates[x1,y1], end point coordinates[x2,y2]*  

13. `determine_points(point_1, end_points)`<br>
This function determines which coordinates in the list of end_points is closer to point_1, by measuring the Eucledian distance. It goes inside `get_start_end_open_end` function.<br>
returns  *start point coordinates[x1,y1], end point coordinates[x2,y2]*

14. `close_2_end(img, first_outer_layer_image)` <br>
To identify how much area of the original image has been transformed. With convex hull less than 0.1% volume can be unwrapped, however with contour we find it is upto 1 %. So default is 1%. Can be changed if needed. <br>
returns *True/False if the condition is met* in the Unwrapping procedure the number of layers to unwrap will break if it had reached this limit

15. `get_ref_fill_image(image)`<br>
With an input border image, it returns the center part of the image filled with 1 and outer 0.
returns *image with center filled*

16. `check_corner_pixels(image)`<br>
The thinning and the remove protruding function sometime missed defective pixels, especially the corner pixels. With this function we multiply the pixels with the directional matrix and find those defective pixels and remove them. Once done, it will again check for the presence of anymore protruding pixels.
returns *image with corrected pixels*




### *Unwrap_runner.py*

Unwrapping functions<br>

1. `unwrap_single_line(img, start_point_est)`<br>
img = image with single line <br>
start_point_est = default is None, this option uses the first point estimated by the unwrapping algorithm for each concentric layer. If it is not used, it uses the function `find_point` in `Utils.py`, and estimate starting point each time a new concentric layer is determined.
returns *x_coordinates, y_coordinates of unwrapped line, Next concentric layer, by default the starting point on the new layer determined by the algorithm*


2. `unwrap_layers(No_of_layers, image, raw_image, use_layer_start_point)` <br>
Unwrap a given image with the given number of layers.<br>
No_of_layers = depends on the image, even if you put a large number, the interation will stop once 99 % volume is transformed when using contour and 99.9 5 when using convex hull approach.<br>
image = Outer line/reference image. <br>
raw_image = image to be unwrapped, with no change in the bitness. <br>
use_layer_start_point = default = None, you can put "Yes", then starting point for the next concentric layer will be taken from the algorithm. see `unwrap_single_line`, `find_point` in `Utils.py`<br>
returns *unwrapped image*


3. `unwrap_layers(No_of_layers, image, raw_image, use_layer_start_point)` <br>
This function unwraps a single image into user defined number of layers.<br>
No_of_layers = depending on the size of the image. Tested upto 200 layers on a large tablet. <br>
image = outer layer image by contour or convex hull. <br>
raw_image = orignal image, with no changes applied <br>
use_layer_start_point = Use start point from the algorithm from the second layer to unwrap. Default determine by drawing a line. To yes this type a string eg. "yes".<br>
return *Unwrapped image* 



4. `unwrap_folder_single_process(folder, no_layers, use_layer_point=None, border_type=None, destination_folder=None)` <br>
Unwrap all the images inside a folder saved as .tiff files.<br>
folder = full path where the files are located. <br>
no_layers = layers to unwrap<br>
user_layer_point = Use start point of the algorithm. Default is None.<br>
border_type = default is convex hull, if countour is needed add "c", as a string.<br>
destination_folder= None and save it as folder "Unwrapped", unless you have a different name leave it as such.
returns *None* Opens a folder "Unwrapped" and saves the unwrapped images with the same name with prefix as "unwrapped".<br>


5. `unwrap_folder_multi_process(No_process, folder, no_layers, use_layer_point=None, border_type=None, destination_folder=None)` <br>
Unwrap all the images, by splitting the number of images into user defined value and unwrapping them in parallel. Faster than `unwrap_folder`.<br>
No_process = number of processes to split. Usually this can be the number of cores available in the computer. Putting higher number wont help unless you have enough cores.<br>
folder = full path where the files are located. <br>
no_layers = layers to unwrap<br>
user_layer_point = Use start point of the algorithm. Default is None.<br>
border_type = default is convex hull, if countour is needed add "c", as a string.<br>
destination_folder= None and save it as folder "Unwrapped", unless you have a different name leave it as such.
returns *None* Opens a folder "Unwrapped" and saves the unwrapped images with the same name with prefix as "unwrapped".<br>



6. `unwrap_folder_single_process_MP(array, List_of_files, folder, no_layers, use_layer_point=None, border_type=None, destination_folder=None)` <br>
The target function to parallelize the process of 'unwrap_folder_multi_process'. <b>
array = list of indices of the images split based on the number of processes given as an input.<br>
List_of_files = list of tiff files determined by `get_files`.<br>
folder = full path where the files are located. <br>
no_layers = layers to unwrap<br>
user_layer_point = Use start point of the algorithm. Default is None.<br>
border_type = default is convex hull, if countour is needed add "c", as a string.<br>
destination_folder= None and save it as folder "Unwrapped", unless you have a different name leave it as such.
returns *None* Opens a folder "Unwrapped" and saves the unwrapped images with the same name with prefix as "unwrapped".<br>


Unwrap fast - not a line by line extraction <br>

1. `unwrap_single_multiline_closed(img, raw_image, layers_2_extract)`<br>
img = 2d -np.array, reference line to be unwrapped <br>
raw_image = 2d-np.array, image to be unwrapped.<br>
layers_2_extract = int, number of layers to be unwrapped <br>
returns *unwrapped raw image* <br>

2. `unwrap_folder_multiline_closed_single_process(folder, layers_2_extract, border_type=None, destination_folder=None)`<br>
folder = str, path where the files are located.<br>
layers_2_extract = int, number of layers to be unwrapped <br>
border_type=None, default convex hull, type string "c" or "C" for contour.<br>
destination_folder=None, default folder name "Unwrapped", specify here if otherwise. <br>


3. `unwrap_folder_multiline_closed_single_MP(array, List_of_files, folder, no_layers, border_type=None, destination_folder=None)` <br>
Subprocess called in a multiprocess unwrapping `unwrap_folder_multiline_closed_multi_process`.<br>
array = list of split indecies to access the list of tiff files in the subprocess.<br>
returns *None*


4. `unwrap_folder_multiline_closed_multi_process(No_process, folder, no_layers, border_type=None, destination_folder=None)`
Unwrap all the images, by splitting the number of images into user defined value and unwrapping them in parallel.<br>
No_process = number of processes to split. Usually this can be the number of cores available in the computer. Putting higher number wont help unless you have enough cores.<br>
folder = full path where the files are located. <br>
no_layers = layers to unwrap<br>
border_type = default is convex hull, if countour is needed add "c", as a string.<br>
destination_folder= None and save it as folder "Unwrapped", unless you have a different name leave it as such.
returns *None* Opens a folder "Unwrapped" and saves the unwrapped images with the same name with prefix as "unwrapped".<br>



Unwrap open ends - not line by line extraction<br>

1. `unwrap_image_multiline_open(shape_image, image, layers_2_extract)` <br>

shape_image = 2d np.array, with a reference line with width one pixel, following the shape of the object to be unwrapped.
image = 2d np.array, raw image to be unwrapped<br>
layers_2_extract = int, number of layers to be extracted. <br>





save functions <br>
    
1. `save_unwrapped_folder(current_folder, destination_folder=None, Layer_image, file)` <br>
This function is used inside unwrapping folder, stores the unwrapped images in a separate folder, default is "Unwrapped".<br>
returns *None*

2. `save_single_image(current_folder, destination_folder=None, Layer_image, file)`<br>
This function is used to save single unwrapped image, unless specified, the unwrapped image will be saved in the same directory as a source image with "unwrapped" as prefix.<br>
returns *None*

Load data functions/preprocess functions <br>

1. `get_files(folder)` <br>
Mention the folder here and it will retrieve all the tiff files from the folder. Default is tiff files. If other format, this function need to be changed.<br>
returns *List of image files ordered*

2. `get_first_layer_contour(image)`<br>
To determine the outer reference layer based on contour points.<br>
image = np.array, binary, background "0", object "1". <br>
returns *image with outer layer value 1 and width 1*

3. `get_first_layer_convex(image)`<br>
To determine the outer reference layer based on convex hull.<br>
image = np.array, binary, background "0", object "1". <br>
returns *image with outer layer value 1 and width 1*

4. `get_image_raw_first(folder, file, extraction_type=None)` <br>
This functions calls `get_first_layer_contour` or `get_first_layer_convex` depending on the user input. Here it is important the image to be unwrapped is already segmented from the background. The image can be of any bitness. But the background must be "0". The object can have any value.<br>
folder = path/location of the folder<br>
file = name of the file as string.<br>
extraction_type = default is convex hull type. IF other wise, enter "c" or "C" here.




Unwrap supporting functions <br>

1. `get_image_value(raw_image,x,y)`<br>
This function will get the image values of the unwrapped layer coordinates.<br>
raw_image = the original image which need to be unwrapped <br>
x,y = x and y coordinates obtained from the unwrapping algorithm (`unwrap_single_line`)<br>
return *list of pixel value of the unwrapped coordinates in a 1D array*




2. `get_image_value_fast(raw_image, coor)`<br>
This function will get the image values of the unwrapped layers coordinates, when multiple layers are extracted using `unwrap_single_multiline_closed`.<br>
raw_image = the original image which need to be unwrapped <br>
coor = list of x and y coordinates obtained from the unwrapping algorithm (`unwrap_single_multiline_closed`)<br>
return *list of pixel value of the unwrapped coordinates in an order in a 2D array*


4. `convert_2_imageD(array_1D,number,list_data_length, start, end)` <br>
The Unwrapped coordinates are stored as a single array, they are resized in this function. <br>
array_1D = pixel vaules of the unwrapped image<br>
number = number of layers actually unwrapped by the algorithm, may change with the user input if the volume limit defined `close_2_end` in `Utils.py` is reached.<br>
list_data_length = length of each layer unwrapped.<br>
start, end, list of indices of each layers in list_data_length<br>
returns *output of order_layer()*

5. `order_layers(length_layer_one, new_layer_array)`<br>
The lenth of the unwrapped layers decreases radially inwards, this function will assess the length of each layers and resize the layers by padding the edges with zeros. Each layers unwrapped will have the same length after this.<br>
returns *Unwrapped image with padding*

### *Kernel_operation.py*
 In addtion to the list of functions here this code also imports few functions from 'Kernel_calculator.py'. It is not required in the new version however, will be eventually removed. <br>



1. `get_image_matrix(Inner_layer_segmented,x,y)`<br>
Inner_layer_segmented = 2d, np.array, with reference line of the image to be unwrapped.
x,y = coordinates.
returns *2d, 3x3 array with x,y in the center -   [[x-1,y+1],[x,y+1],[x+1,y+1]],[[x-1,y],[x,y],[x+1,y]],[[x-1,y-1],[x,y-1],[x+1,y-1]]*

2. `kernel_matrix()`<br>
returns *directional matrix [[-5, 4, 15], [-4, -1, -16], [10, 8, -20]]*

3. `Operate_matrix(Position_matrix, Kernel)`
carries out elemet wise multiplication and get the get the sum of the resulting 3x3 array.<br>
returns *int*


4. The following functions are same but split into three for layer-by-layer extraction, multiple layer extraction(_fast) and objects with open ends (_open_ends). This function analyses the result from the `Operate_matrix` function and returns the next pixel the directional matrix need to go, and the concentric pixel or pixels to be extracted.<br>

    4.1. `Next_coordinate(result,x,y,previous_point, center_x, center_y, Position_matrix, remove_data, reference)` <br>
      returns *return next_coordinate (position of the next pixel to go in the current line), Next_coordinate_layer (position of the concentric pixel towards the center of the object relative to the current pixel), remove_coordinate (if a defective pixel is present, from the old version, will be removed in the future.)*<br>

    4.2. `Next_coordinate_fast(result,x,y,previous_point, center_x, center_y, Position_matrix, reference, pts)`<br>
      returns *return next_coordinate (position of the next pixel to go in the current line), Extend_coordinate (list of coordinates of the concentric layers)*<br>

    4.3. `Next_coordinate_open_ends(result,x,y,previous_point, center_x, center_y, Position_matrix, reference, pts)`<br>
      same as `Next_coordinate_fast` with few different supporting functions. Hence it is been separated. <br>

5. Supporting functions of all `Next_coodinate` functions described before.<br>

    5.1. For `Next_coordinate`<br>
                5.1.1. `find_correct_point(center_x, center_y, [x-1,y], [x+1,y], result, reference)`<br>
                Checks if the next concentric pixel in the direction towards the center of the object.<br>
                returns *new x and y coordinate*<br>
                5.1.2 `find_right_order(previous_point, Next_coordinate_layer_1, Next_coordinate_layer_2)`<br>
               Same as 5.1.1, however applied when operating on diagonal matrix<br>
               returns *new x and y coordinates*<br>



    5.2. For `Next_coordinate_fast`<br>
               5.2.1. `Extend_point_horizontal`<br>
               returns *list of array corresponding to the concentric layers in horizontal direction*<br>
               5.2.2. `Extend_point_vertical`<br>
               returns *list of array corresponding to the concentric layers in vertical direction*<br>
               5.2.3. `guess_orienHOV`<br>
               returns *Guess weather with the pixel orientation horizontal or vertical layers are better based on which axis points towards the center of the object - list of array corresponding to the concentric layers in horizontal direction*<br>



    5.3 For `Next_coordinate_open_ends`<br>
    Same as 5.2, except minor changes in the input paramters.<br>
    Description same as above with different names and input variables.
               5.2.1. `Extend_point_horizontal_OE`<br>
               5.2.2. `Extend_point_vertical_OE`<br>
               5.2.3. `guess_orienHOV_OE`<br>

6. `determine_second(shape_image,first_position, x, y)` <br>
It is used to get the second point from the open end.
returns *coodinates of the second point connected from the given coordinate*


