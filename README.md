# Unwrapping-tomography-images
The unwrapping codes developed can digitally unroll 2D slices of a 3D object measured by a tomography technique. Few associated functions can be used identify only external surface and characterize surface roughness.

## List of python scripts
1. Utils.py
2. Kernel_operation.py
3. Unwrap_single_image.py
4. Unwrap_folder.py

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

5. `correct_check_single_contour(image, contours, k_i)`<br>
image = np.array, binary, just to make an empty image<br>
contours = updated contours from `check_single_contour_new` <br>
k_i = kernel size, default = 5 <br>
returns *corrected outer layer with contour drawn (2D array), new contour compensating for the dilation*

6. `check_eight_point_convol_op(img)`<br>
img = np.array - any line with line width 1, dtype=np.uint8, line value should be 1 and rest should be 0.<br>
Checks if there are any points with 4-point connectivity<br>
returns *True/False*

7. `correct_by_thin(img)`<br>
img = np.array = any line with line with/without width 1, dtype=np.uint8, line value should be 1 and rest should be 0.<br>
returns *thin image with 8-point connectivity*

8. `check_open_ends_convol_op(img)`<br>
img = np.array - line with width 1, dtype=np.uint8, line value should be 1 and rest should be 0.<br>
returns *True - if there are open ends/ false - otherwise*

9. `remove_defects(img, unique, counts, kernel)`<br>
It is a nested function of `remove_protruding ends` - can be modified if new kernel is developed. Mainly used to remove isolated pixels. To some extent removes non-eight point connectivity pixels. <br>
img = np.array - with defective line image with line width as 1, line value should be 1 and rest should be zero <br>
unique = list of unique elements obtained from np.unique.<br>
counts = list of counts from the elements obtained from np.unique.<br>
kernel = default - [[1,1,1],[1,0,1],[1,1,1]] <br>
returns *Image - after removing defective pixels.*<br>

10. `remove_protruding_open_ends(img)`<br>
Other functions required - `check_open_ends_convol_op`, `remove_defects` <br>
Iterates (default - 80 iterations) apply kernel - [[-1,-1,-1],[-1,1,-1],[-1,-1,-1]], multiply with original image, convert to absolute value, remove every pixel value above "1" (protruding pixels). After each iteration check if any protruding ends are present by `check_open_ends_convol_op`. If no open ends are present, returns the corrected image. <br>
returns *corrected image*


### *Unwrap_single_image.py*

1. `get_first_layer_contour(image)` <br>
image - binary image, np.array, dtype = uint8. <br>
returns *outer layer* - outer reference layer of the image by connecting the contour points with 8-point connectivity. Removes small countours, correct for a full closure of the object if convex hull fails.  
