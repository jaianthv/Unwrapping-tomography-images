# Unwrapping-tomography-images
The unwrapping codes developed can digitally unroll 2D slices of a 3D object measured by a tomography technique. Few associated functions can be used identify only external surface and characterize surface roughness.

## List of python scripts
1. Utils.py
2. Kernel_operation.py
3. Unwrap_single_image.py
4. Unwrap_folder.py

## List of functions available

1.	`get_center(image, str)`
image = np.array
str = “Show” to display image or None
returns *cx,cy* - coordinates of center of mass

2.	`Clean_small_contours(list(contours))`
list(contours) - obtained from cv.findContours
returns  *new list of contours* - after removing the smaller ones
