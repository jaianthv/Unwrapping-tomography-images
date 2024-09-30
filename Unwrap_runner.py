import os
import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
from Utils import *
from skimage.morphology import skeletonize, thin
from Kernal_operation_new import *
import multiprocessing as mp
#from Kernal_operation_new_fast import *


def get_first_layer_contour(image):
    
    
    original = image.copy()
    # get center
    cx,cy = get_center(image,None)

    # get list of contours
    
    contours,_ = cv.findContours(image, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_TC89_L1)

    # clean small contours
    contours = clean_extra_contours(contours)
    
    #x = cv.drawContours(image,contours,-1, (255,255,0), 1)
    binary_image = image*0
    for i in range(len(contours)):
        x = cv.drawContours(binary_image, contours, i, (255,255,0), lineType=cv.LINE_8)
    retval, x = cv.threshold(binary_image,20,1,cv.THRESH_BINARY+cv.THRESH_OTSU)
    
   
    # check single contour
    updated_contour, dilate_thick = check_single_contour_new(x)
    

    # check closure
    
    outer_layer, new_contours = correct_check_single_contour(x, updated_contour, dilate_thick)
     
    
    return outer_layer
    

def get_first_layer_convex(image):
    
    # get center
    cx,cy = get_center(image,None)

    # get list of contours
    
    contours,_ = cv.findContours(image, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_TC89_L1)

    # clean small contours

    contours = clean_extra_contours(contours)

    
    # check single contour

    image_new = image *0
    for i in range(len(contours)):
        x = cv.drawContours(image_new, contours, i, (120,0,0), lineType=cv.LINE_8)
    retval, x = cv.threshold(image_new,20,1,cv.THRESH_BINARY+cv.THRESH_OTSU)
    updated_contour, dilate_thick = check_single_contour_new(x)
    
    # Check closure

   
    outer_layer, new_contours = correct_check_single_contour(x, updated_contour, dilate_thick)
  
    hull = []
    for i in range(len(new_contours)):
        hull.append(cv.convexHull(new_contours[i], False))  
    color = (120, 0, 0) #color for convex hull


    binary_image = image*0
    for i in range(len(contours)):
        cv.drawContours(binary_image, hull, i, color, lineType=cv.LINE_8)
    retval, x = cv.threshold(binary_image,20,1,cv.THRESH_BINARY+cv.THRESH_OTSU)

    outer_layer = x
   
    
    return outer_layer




def get_image_raw_first(folder, file, extraction_type=None):

    
    os.chdir(folder)
    image = cv.imread(file,-1)
    raw_image = image.copy()

    #image = np.where(image>17000,image,0)
    image = np.where(image==0,image,1)

    #plt.matshow(image)
    #plt.show()
    
    image = np.array(image,dtype=np.uint8)
    first = image
    
    if extraction_type == "c" or extraction_type == "C" :
        first = get_first_layer_contour(image)
    else:
        first = get_first_layer_convex(image)


    
    fpconnectivity = check_eight_point_convol_op(first)

    if fpconnectivity == True:
        first = correct_by_thin(first)
        
        
    open_ends_present = check_open_ends_convol_op(first)


    if open_ends_present == True:
        first = remove_protruding_open_ends(first)

        
    first = np.array(first, dtype=np.uint8)
    return raw_image, first





def get_image_value_fast(raw_image,coor):
    Intensities = []
    #image = cv.imread(File,-1)
    
    
    for i in range(len(coor)):
        Intensities.append(raw_image[coor[i][0]][coor[i][1]])
        
        #print (raw_image[x[i]][y[i]])
    return Intensities




def get_image_value(raw_image,x,y):
    Intensities = []
    #image = cv.imread(File,-1)
    
    
    for i in range(len(x)):
        Intensities.append(raw_image[x[i]][y[i]])
        
        #print (raw_image[x[i]][y[i]])
    return Intensities



def order_layers(length_layer_one, new_layer_array):
    
    Length_new_layer_array = len(new_layer_array)
    difference = abs(length_layer_one - Length_new_layer_array)
    #print (difference)
    
    if difference%2 == 0:
    
       new = np.pad(new_layer_array,int(difference/2), mode = 'constant')
    
       
    if difference%2 != 0:
       pad_no = (difference-1)/2
       new = np.pad(new_layer_array,[int(pad_no)+1,int(pad_no)], mode = 'constant')
       
    #print ("finished order")
    return new

def convert_2_imageD(array_1D,number,list_data_length, start, end):
    new_layer = []
    maximum = max(list_data_length)
    #print (maximum)
    for i in range(len(list_data_length)):
        if list_data_length[i] != maximum:
           new_layer_temp = order_layers(maximum,array_1D[start[i]:end[i]-1])
           #print (start[i])
           #print (end[i]-1)
           #print ("conversion")
           #print (len(new_layer_temp))
           for j in range(len(new_layer_temp)):
               new_layer.append(new_layer_temp[j])
        if list_data_length[i] == maximum:
            #print ("no conversion")
            for j in range(start[i],end[i]):
                
                new_layer.append(array_1D[j])
    #print ((new_layer))
    #print (np.shape(np.array(new_layer), dtype = np.uint8))
                           
            
        
       
    return np.reshape(np.array(new_layer),(maximum, number), order ='F')
   






def unwrap_single_line(img, start_point_est):
    image = img.copy()
    
    SP, center_x, center_y = get_first_point(image)
    starting_point = [SP[1], SP[0]]
    
    if start_point_est!=None:
        starting_point =start_point_est
    
    #center_x = cor_x
    #center_y = cor_y

    ## coordinates of the unwrapped pixels
    x_coordinate = []
    y_coordinate = []
    temp_array =[]

    image_length = cv.findNonZero(image)

    Next_layer_empty_image = image*0 # empty image


    current_position = starting_point
    previous_position = [0,0]
    unwrap_image = []
    
    Reference_image = get_ref_fill_image(image) # needed to identify the coordinates of the inner concentric layer
    
    for i in range(len(image_length)):
        if i ==0:
            x_coordinate.append(starting_point[0])
            y_coordinate.append(starting_point[1])
            current_position = starting_point
            previous_position = [0,0]
        

        Position_matrix, remove_data = get_image_matrix(image, current_position[0], current_position[1])
        #print (Position_matrix)
        Kernel_matrix = kernel_matrix()
        result = Operate_matrix(Position_matrix, Kernel_matrix)
        #print (result)

             
        
        Next_point, Next_layer_point, remove_coordinate = Next_coordinate(result, current_position[0], current_position[1], previous_position, center_x, center_y, Position_matrix, remove_data, Reference_image)

        if i ==0:
            starting_point_new_layer = Next_layer_point[0]
            

        # create the next layer in an empty image
        for j in range(len(Next_layer_point)):
            Next_layer_empty_image[Next_layer_point[j][0]][Next_layer_point[j][1]] = 1
            temp_array.append(Next_layer_point[j])

        # remove defective pixels if they are still present - only for safety, never needed in the updated version
        if remove_coordinate[0][0] and remove_coordinate[0][1] != 0:
           
           for j in range(len(remove_coordinate)):
               image[remove_coordinate[j][0]][remove_coordinate[j][1]] = 0

        # connect the points to be safe
        if i > 0:
            
            p1 = (temp_array[len(temp_array)-1][1], temp_array[len(temp_array)-1][0])
            #print (p1)
            p2 = (temp_array[len(temp_array)-2][1], temp_array[len(temp_array)-2][0])
            #print (p2)
            cv.line(Next_layer_empty_image, p1, p2, 1, thickness=1, lineType=cv.LINE_8, shift=0)



        x_coordinate.append(Next_point[0])
        y_coordinate.append(Next_point[1])
        if len(Next_point) == 0:
            print ("Error - cannot find the next position")
            break

         
    
        previous_position = current_position
        current_position = Next_point
        
        #unwrap_image.append(get_image_value(img, Extend_coordinate))

    
    return x_coordinate, y_coordinate, Next_layer_empty_image, starting_point_new_layer





def unwrap_layers(No_of_layers, image, raw_image, use_layer_start_point): # image - outerlayer image, raw_image - straight from the file no threshold
    
    x = image
    Layer_image = []
    start = []
    end = []
    original_image = image
    retval, original_image = cv.threshold(original_image,100,1,cv.THRESH_BINARY+cv.THRESH_OTSU)
    
    xx= []
    
    List_data_length = []
    start_point_Est = None
    for i in range(No_of_layers):
        
        
        
        cor_x, cor_y = get_center(image, None)
        x_coor, y_coor, Next_image, starting_point_next_layer = unwrap_single_line(x,start_point_Est)
        if use_layer_start_point!=None:
           start_point_Est = starting_point_next_layer

        
        #newim = unwarp(file,x_coor,y_coor)
        # unwrapped layer
        newim = get_image_value(raw_image, x_coor, y_coor)
        #print (newim)
        
        
        x = Next_image
        x = check_image(x)
        
        #print (i)    
        x = check_corner_pixels(x)
            #plt.matshow(x)
            #plt.show()

        In_the_end = close_2_end(x,image)
        
        if In_the_end == True:
            break


        
        
        original_image = (original_image + (x * (i+2)))
       
        List_data_length.append(len(newim))
        
        #print (List_data_length)
        for j in range(len(newim)):
            Layer_image.append(newim[j])
            
        if i == 0:
           start.append(0)
           end.append(len(newim))
        if i !=0:
           start.append(end[i-1])
           end.append(len(Layer_image)-1)
        #print (start)
        #print (end)
        
       
        
    

    
    Layer_image = convert_2_imageD(Layer_image,len(start),List_data_length,start,end) # i+1 = number of layers
    #plt.matshow(Layer_image)
    #plt.show()


    #plt.matshow(Layer_image)
    #plt.matshow(original_image)
    #plt.show()

    #path_name = "Upto_center_layers_contour.tiff"
    #cv.imwrite(path_name,original_image)
    
    
    #path_name = "Unwrap_inner_%s.tiff"%file.replace(".tiff","")
    #cv.imwrite(path_name,Layer_image.transpose())

    #os.chdir(folder)
    
    return Layer_image


def get_files(folder):
    os.chdir(folder)
    List_of_files = os.listdir();
    List_of_files.sort()

    List_of_tiff = []

    for i in range(0,len(List_of_files)):  #check344 360 1292
        Is_it_tif=".tif" in List_of_files[i]
        if Is_it_tif==True:
            List_of_tiff.append(List_of_files[i])
    return List_of_tiff



def save_single_image(current_folder, destination_folder, Layer_image, file):
    if destination_folder!=None:
        check = os.path.isdir(destination_folder)
        if check == False:
            os.mkdir(destination_folder)
            os.chdir(destination_folder)
    path_name = "Unwrapped_"+file
    cv.imwrite(path_name,Layer_image.transpose())
    os.chdir(current_folder)
    

def save_unwrapped_folder(current_folder, destination_folder, Layer_image, file):
 
    '''
    if destination_folder==None:
        destination_folder = "Unwrapped"
    
    check = os.path.isdir(destination_folder)
    if check == False:
       os.mkdir(destination_folder)
    '''
    os.chdir("Unwrapped")
    path_name = "Unwrapped_"+file
    cv.imwrite(path_name,Layer_image.transpose())
    os.chdir(current_folder)




def unwrap_folder_single_process(folder, no_layers, use_layer_point=None, border_type=None, destination_folder=None):

    os.chdir(folder)
    List_of_files = get_files(folder)
    os.mkdir("Unwrapped")
    #print (List_of_files)

    for i in range(len(List_of_files)):  #check344 360 1292 0 1388
        os.chdir(folder)
        file = List_of_files[i]
        raw_image, first = get_image_raw_first(folder, file, border_type)
        unwrap_image = unwrap_layers(no_layers, first, raw_image, use_layer_point)

        save_unwrapped_folder(folder, destination_folder, unwrap_image, file)

        
        


def unwrap_folder_single_process_MP(array, List_of_files, folder, no_layers, use_layer_point=None, border_type=None, destination_folder=None):
    
    for i in range(len(array)):
        os.chdir(folder)
        file = List_of_files[array[i]]
        print (List_of_files[array[i]])
        raw_image, first = get_image_raw_first(folder, file, border_type)
        unwrap_image = unwrap_layers(no_layers, first, raw_image, use_layer_point)
        save_unwrapped_folder(folder, destination_folder, unwrap_image, file)



def unwrap_folder_multi_process(No_process, folder, no_layers, use_layer_point=None, border_type=None, destination_folder=None):
    os.chdir(folder)
    List_of_tiff = get_files(folder)
    #os.mkdir("Unwrapped")
    check = os.path.isdir("Unwrapped")
    if check == False:
       os.mkdir("Unwrapped")
    
    temp_num = np.arange(len(List_of_tiff))
    split_temp_num = np.array_split(temp_num,No_process)

    thread_list = []
    for kk in range(len(split_temp_num)):
        p = mp.Process(target=unwrap_folder_single_process_MP, args=(split_temp_num[kk], List_of_tiff, folder, no_layers, use_layer_point, border_type, destination_folder))
        thread_list.append(p)

    for thread in thread_list:
        thread.start()
    for thread in thread_list:
        thread.join()









########################################################################################################################################################################
########################### Unwarp_fast #########################################################################################














def unwrap_single_multiline_closed(img, raw_image, layers_2_extract):
    image = img.copy()
    
    SP, center_x, center_y = get_first_point(image)
    starting_point = [SP[1], SP[0]]
    
    
    ## coordinates of the unwrapped pixels
    x_y_coordinate = []
    
    temp_array =[]

    image_length = cv.findNonZero(image)

    
    current_position = starting_point
    previous_position = [0,0]
    unwrap_image = []
    
    Reference_image = get_ref_fill_image(image) # needed to identify the coordinates of the inner concentric layer
    
    for i in range(len(image_length)):
        if i ==0:
            #x_coordinate.append(starting_point[0])
            #y_coordinate.append(starting_point[1])
            current_position = starting_point
            previous_position = [0,0]
        

        Position_matrix, remove_data = get_image_matrix(image, current_position[0], current_position[1])
        #print (Position_matrix)
        Kernel_matrix = kernel_matrix()
        result = Operate_matrix(Position_matrix, Kernel_matrix)
        #print (result)

             
        
        Next_point, Extend_coordinate = Next_coordinate_fast(result, current_position[0], current_position[1], previous_position, center_x, center_y, Position_matrix, Reference_image, layers_2_extract)
        unwrap_image.append(get_image_value_fast(raw_image, Extend_coordinate))
        x_y_coordinate.append(Extend_coordinate)

       
       
        if len(Next_point) == 0:
            print ("Error - cannot find the next position")
            break

         
    
        previous_position = current_position
        current_position = Next_point
        
        #unwrap_image.append(get_image_value(img, Extend_coordinate))

    #plt.matshow(unwrap_image)
    #plt.show()
    unwrap_image = np.array(unwrap_image)
    return unwrap_image





    
def unwrap_folder_multiline_closed_single_process(folder, layers_2_extract, border_type=None, destination_folder=None):
    os.chdir(folder)
    List_of_files = get_files(folder)
    os.mkdir("Unwrapped")
    #print (List_of_files)

    for i in range(len(List_of_files)):  #check344 360 1292 0 1388
        os.chdir(folder)
        file = List_of_files[i]
        raw_image, first = get_image_raw_first(folder, file, border_type)
        unwrap_image = unwrap_single_multiline_closed(first, raw_image, layers_2_extract)

        save_unwrapped_folder(folder, destination_folder, unwrap_image, file)



    






def unwrap_folder_multiline_closed_single_MP(array, List_of_files, folder, no_layers, border_type=None, destination_folder=None):
    for i in range(len(array)):
        os.chdir(folder)
        file = List_of_files[array[i]]
        print (List_of_files[array[i]])
        raw_image, first = get_image_raw_first(folder, file, border_type)
        unwrap_image = unwrap_single_multiline_closed(first, raw_image, no_layers)
        save_unwrapped_folder(folder, destination_folder, unwrap_image, file)











def unwrap_folder_multiline_closed_multi_process(No_process, folder, no_layers, border_type=None, destination_folder=None):
    os.chdir(folder)
    List_of_tiff = get_files(folder)
    #os.mkdir("Unwrapped")
    check = os.path.isdir("Unwrapped")
    if check == False:
       os.mkdir("Unwrapped")
    
    temp_num = np.arange(len(List_of_tiff))
    split_temp_num = np.array_split(temp_num,No_process)

    thread_list = []
    for kk in range(len(split_temp_num)):
        p = mp.Process(target=unwrap_folder_multiline_closed_single_MP, args=(split_temp_num[kk], List_of_tiff, folder, no_layers, border_type, destination_folder))
        thread_list.append(p)

    for thread in thread_list:
        thread.start()
    for thread in thread_list:
        thread.join()




###################################################################################################################################################################################
################################### unwrap_open


def unwrap_image_multiline_open(shape_image, image, layers_2_extract):
    
    
    start_point, end_point = get_start_end_open_end(shape_image)
   
    #shape_image[end_point[0]][end_point[1]]=10
    #plt.matshow(shape_image)
    #plt.show()

    first_position, remove_data = get_image_matrix(shape_image,start_point[0],start_point[1])
    #print (first_position)

    Real_start_point = determine_second(shape_image, first_position, start_point[0], start_point[1] )
    #shape_image[Real_start_point[0]][Real_start_point[1]]=10
    #plt.matshow(shape_image)
    #plt.show()

    image_length = cv.findNonZero(shape_image)

    current_position = Real_start_point
    previous_position = start_point
    unwrap_image = []
    print ("start unwrap")
    for i in range(len(image_length)-2):
        

        Position_matrix, remove_data = get_image_matrix(shape_image, current_position[0], current_position[1])
        Kernel_matrix = kernel_matrix()
        result = Operate_matrix(Position_matrix, Kernel_matrix)
        #print (result)

        #Next_point, Extend_coordinate = Next_coordinate(result,current_position[0],current_position[1],previous_position, end_point[0], end_point[1], Position_matrix)
        Next_point, Extend_coordinate = Next_coordinate_open_ends(result, current_position[0], current_position[1], previous_position, end_point[0], end_point[1], Position_matrix, None, layers_2_extract)
        #print (Extend_coordinate)
        previous_position = current_position
        current_position = Next_point
        unwrap_image.append(get_image_value_fast(image, Extend_coordinate))

        #if current_position == end_point:
        #   break
        #   break
    #plt.matshow(unwrap_image)
    #plt.show()
    return unwrap_image



    








