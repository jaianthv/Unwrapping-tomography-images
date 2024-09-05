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



### *Unwrap_single_image.py*

1. `get_first_layer_contour(image)` <br>
image - binary image, np.array, dtype = uint8. <br>
returns *outer layer* - outer reference layer of the image by connecting the contour points with 8-point connectivity. Removes small countours, correct for a full closure of the object if convex hull fails.  
