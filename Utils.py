import cv2 as cv
import numpy as np
import os
#import porespy as ps
import sys
import matplotlib.pyplot as plt
from Kernal_operation_new import *
from skimage.morphology import skeletonize, thin

def get_center(image, show_image):
    # object should be non-zero, background should be zero
    temp_image = image.copy()
    temp_image = cv.floodFill(temp_image,None, (0,0),1)
    temp_image = cv.bitwise_not(temp_image[1])
   
    temp_image = temp_image - 254
    
    M = cv.moments(temp_image)
    cx = (M["m10"] / M["m00"])
    cy = (M["m01"] / M["m00"])
    center_coordinates = (int(cx), int(cy)) 
    radius = 3
    color = (10, 10, 0) 
    thickness = 1
    

    if show_image == "show" or show_image == "Show":
        temp_image = cv.circle(temp_image, center_coordinates, radius, color, thickness)
        plt.matshow(temp_image)
        plt.show()

    return int(cx), int(cy)



    
def clean_extra_contours(contours):

    # draw contours
    # dilate contours
    # check len of contours
    # if you have to dilate 


    
    No_of_contours = len(contours)
    #print (No_of_contours)
    Individual = []
    
    for i in range(No_of_contours):
        Individual.append(len(contours[i]))
        
   
    #print (Individual)
    
    Max_Con = max(Individual)
    #print (Max_Con)
    idx = Individual.index(Max_Con)
    #print (idx)
       
    del_item = []

    for j in range(len(contours)):
        #if Max_Con - len(contours[j]) > 1506:
        if len(contours[j])/Max_Con < 0.9:
           #print (Max_Con - len(contours[j]))
           del_item.append(len(contours[j]))
    
    #print (del_item)

    for j in range(0,len(del_item)):
        no_of_contour = len(contours)
        
        for k in range(0,no_of_contour):
            if len(contours[k]) == del_item[j] :
                del(contours[k])
                break
    return contours
        




def check_single_contour_new(image):

    temp_image = image.copy()
    
    length = np.shape(image)[0] * np.shape(image)[1]
    #print (length)
    sum_p = 0
    original_image = image.copy()
    
    for i in range(5,50):

              
        kernel = np.ones((i,i),np.uint8)
        binary_image = cv.dilate(temp_image,kernel,iterations=1)

        contours,_ = cv.findContours(binary_image, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_TC89_L1)
        #print (len(contours))
       
        if len(contours) == 1 :
            sum_p = sum_p + 1
            #print ("Checked_single_length")
            
        if sum_p == 1:
          # print (len(contours))
           #print (i)
           return contours, i
           break
        if i == 50:
           plt.matshow(binary_image)
           plt.title("ITs going above 40")
           plt.show()



def correct_check_single_contour(image, contours, k_i):

    temp_image = image.copy()
    empty_image = image*0
    
    for i in range(len(contours)):
        x = cv.drawContours(empty_image, contours, i, (120,0,0), lineType=cv.LINE_8)
    retval, x = cv.threshold(empty_image,20,1,cv.THRESH_BINARY+cv.THRESH_OTSU)

    if k_i >5:  
        kernel = np.ones((k_i-5,k_i-5),np.uint8)
        x = cv.dilate(temp_image,kernel,iterations=1)
        #plt.matshow(x)
        #plt.show()

        mask_image = cv.floodFill(x,None, (0,0),1)
        mask_image = cv.bitwise_not(mask_image[1])
        flood_fill = mask_image - 254

        Edge_image = cv.Canny(flood_fill,1,1)
        #plt.matshow(Edge_image)

        contours,_ = cv.findContours(Edge_image, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_TC89_L1)
        
        empty_image = image*0
        for i in range(len(contours)):
            x = cv.drawContours(empty_image, contours, i, (120,0,0), lineType=cv.LINE_8)
        retval, x = cv.threshold(empty_image,20,1,cv.THRESH_BINARY+cv.THRESH_OTSU)
    

    return x, contours

    

def check_corner_pixels(image):
    #plt.matshow(image)
    #plt.show()
    img = image.copy()
    previous_image = img.copy()
    img =np.array(img,dtype=np.float32)
    kernel = np.array([[-5,4,15],[-4,-1,-16],[10,8,-20]])
    img = cv.filter2D(img, ddepth=-1, kernel=kernel)
    img = img*previous_image
    

    unique, counts = np.unique(img, return_counts=True)
    unique = np.delete(unique,0)
    counts = np.delete(counts,0)
    #print (unique, counts)
        
    #print (index)
    corner_list = [-9,3,-1,-13]
    corner_points = np.isin(unique, corner_list)

    if corner_points.any() ==True:
        to_remove = unique[corner_points]
        #print (to_remove)
        for ii in range(len(to_remove)):
            img = np.where(img!=to_remove[ii], img, 0)
            
        img = np.absolute(img)
        img = np.where(img==0,img,1)
        
        #plt.matshow(img)
        #plt.show()
        img = remove_protruding_open_ends(img)
        #plt.matshow(img)
        #plt.show()
        img = np.array(img,dtype=np.uint8)
        return img
    else:
        return image



def check_eight_point_convol_op(img):
    previous_image = img
    kernel = np.array([[-5,4,15],[-4,-1,-16],[10,8,-20]])
    img = cv.filter2D(img, ddepth=-1, kernel=kernel)
    img = img*previous_image

    unique, counts = np.unique(img, return_counts=True)
    unique = np.delete(unique,0)
    counts = np.delete(counts,0)
    #print (unique, counts)
        
    #print (index)
    fp_list = [-30, 6, 1, 14, 9, -33, -18, -17]
    fp_points = np.isin(unique, fp_list)
    #print (unique[fp_points])
    if unique[fp_points].any() == True: 
       return True
    else:
       return False




    


def check_open_ends_convol_op(img):
    #plt.matshow(img)
    #plt.show()
    img = np.array(img,dtype=np.float32)
    previous_image = img
    kernel = np.array([[1,1,1],[1,0,1],[1,1,1]])
    img = cv.filter2D(img, ddepth=-1, kernel=kernel)
    
    img = np.absolute(img*previous_image)
    #plt.matshow(img)
    #plt.show()
    #retval, img = cv.threshold(img,0,1,cv.THRESH_BINARY)
    unique, counts = np.unique(img, return_counts=True)
    unique = np.delete(unique,0)
    counts = np.delete(counts,0)
    
    # there are no defects unique will be 0 and 2, if there are defects it will more than 0 and 2.
    if len(unique)>1:
        return True
    else:
        return False





def remove_defects(img, unique, counts, kernel2):
    index = np.where(counts==np.amax(counts))
    img_mask = np.where(img>(unique[index]),img,0)
    #plt.matshow(img_mask)
    #plt.title("remove_defects")
    #plt.show()
    #cv.imwrite("d3.tiff", img_mask)


    #plt.matshow(img)
    #plt.show()
    

    img1 = np.where(img<np.amax(unique), img,0)
    #plt.matshow(img1)
    #plt.show()
    #cv.imwrite("d4.tiff", img1)
    previous_image = img1
    img = cv.filter2D(img1, ddepth=-1, kernel=kernel2)
    #cv.imwrite("d4b.tiff", img)
    #plt.matshow(img)
    #plt.show()
    
    #plt.matshow(img*previous_image+img_mask)
    #plt.show()
    #cv.imwrite("d6.tiff", img*previous_image+img_mask)
    Final_image = img*previous_image+img_mask
    retval, Final_image = cv.threshold(Final_image,0,1,cv.THRESH_BINARY)
    #cv.imwrite("d7.tiff", Final_image)
    #plt.matshow(Final_image)
    #plt.show()
    return Final_image







def remove_protruding_open_ends(img):
    # to remove protruding pixels connected to a 8-point connectivity line. Other pixels protruding from
    # a non-8 point connectivity will not be removed
    
    kernel1 = np.array([[-1,-1,-1],[-1,1,-1],[-1,-1,-1]])

    # to remove non-8point connectivity pixels
    kernel2 = np.array([[1,1,1],[1,0,1],[1,1,1]])

    previous_image = img
    
    previous_image = np.array(previous_image, dtype=np.float32)
    
    for i in range(0,80):

        img = cv.filter2D(previous_image, ddepth=-1, kernel=kernel1)
        
        img = np.absolute(img*previous_image)
        
        
        retval, img = cv.threshold(img,0,1,cv.THRESH_BINARY)
        previous_image = img
        val = check_open_ends_convol_op(previous_image)
        #print (val)
        
        if val == False:
            break



        
    remove_protude = img
    #cv.imwrite("d1.tiff", img)
   
    img = cv.filter2D(previous_image, ddepth=-1, kernel=kernel2)

    img = np.absolute(img)
    img = img*previous_image
    unique, counts = np.unique(img, return_counts=True)
    unique = np.delete(unique,0)
    counts = np.delete(counts,0)
    #print (unique, counts)
    
    #print (index)
    three = np.isin(unique,3)
    
    one = np.isin(unique,1)
    if three.any() == True or one.any() == True:
        img = remove_defects(img, unique, counts, kernel2)
        previous_image = img
        img = cv.filter2D(img, ddepth=-1, kernel=kernel2)

        img = np.absolute(img)
        img = img*previous_image

        #plt.matshow(img)
        #plt.show()
        unique, counts = np.unique(img, return_counts=True)
        unique = np.delete(unique,0)
        counts = np.delete(counts,0)
    
    #plt.matshow(img)
    #plt.show()
    #cv.imwrite("d2.tiff", img)
    #kernel = np.ones((10,10),np.uint8)
    #temp_im = cv.dilate(img,kernel,iterations = 1)
    #temp_im = np.array(temp_im, dtype=np.uint8)
    #cv.imwrite("xx.tiff", temp_im)




    
    #end_position = np.where(img==1) 

    retval, img = cv.threshold(img,0,1,cv.THRESH_BINARY)
    
    return img
    
    


def correct_by_thin(img):
    original = img.copy()
    #fp_list = [-2, 6, 1, -18, 14, 9, -33]   # [-2,-33], [6,9], [1,14], [-18,-17]


    fp_list = [-2,6,1,-18]
    fp_list_1 = [-33, 9, 14, -17]
    tp_list_eight = [11,10,-21,-25,24,-22,-26,-7,2,9,22,-11,13,4,-17,-6]
    tp_list_non_eight = [-9,3,-1]#,-13]
    tt =thin(img)
    return tt
               
   



def get_ref_fill_image(image):
    temp_image = image.copy()
    temp_image = cv.floodFill(temp_image,None, (0,0),1)
    temp_image = cv.bitwise_not(temp_image[1])
   
    temp_image = temp_image - 254
    return temp_image









def check_image(first):
    fpconnectivity = check_eight_point_convol_op(first)
   
    
    #if fpconnectivity == True:
        
    first = correct_by_thin(first)
    
    
    open_ends_present = check_open_ends_convol_op(first)
    

    if open_ends_present == True:
        first = remove_protruding_open_ends(first)
    
    first = np.array(first, dtype=np.uint8)

   
    return first






def close_2_end(img, first_outer_layer_image):

    temp_image = img.copy()
    temp_outer = first_outer_layer_image.copy()

    img_c = cv.floodFill(temp_image,None, (0,0),1)
    img_c = cv.bitwise_not(img_c[1])
    img_c = img_c - 254


    length_img_c = len(cv.findNonZero(img_c))
    

    first_layer_c = cv.floodFill(temp_outer,None, (0,0),1)
    first_layer_c = cv.bitwise_not(first_layer_c[1])
    first_layer_c = first_layer_c-254

    length_first_layer_c = len(cv.findNonZero(first_layer_c))

    #print (100 * length_img_c/length_first_layer_c)

    if length_img_c/length_first_layer_c < 0.001: # for hull 0.001 for contour 0.01
        return True
    
    else:
        return False





















































































###############################


def get_COM_line(image,show_image):
    cx,cy = get_center(image,show_image)
    cy = get_y_axis(image)
    
    shape=np.shape(image)
    img = np.zeros(shape, np.uint8)
    cv.line(img,(0,cy),(shape[1],cy),(1,0,0),1)
    if show_image == "show" or show_image == "Show":
    
        plt.matshow(img)
        plt.show()
    img = np.array(img,dtype=np.uint8)
    return img
    

def get_y_axis(image):
    x = (cv.findNonZero(image))
    #print (len(x))
    
    x = np.array(x)
    #print (x)
    temp =[]
      
    for i in range(0,len(x)):
        coordinate = x[i]
        coordinate_x = int(coordinate[0][1])  #change in coordinate
        #coordinate_y = int(coordinate[0][0])  #change in coordinate
        
        temp.append(coordinate_x)
    return max(temp,key=temp.count)
    #return round(np.average(temp))
    


def Is_it_enclosed(image,cx,cy): # image should be an np array
    length = np.shape(image)[0] * np.shape(image)[1]
    print (length)
    for i in range(3,500):
        
        
        kernel = np.ones((i,i),np.uint8)
        binary_image = cv.dilate(image,kernel,iterations=1)
        flood_fill = cv.floodFill(binary_image,None,(cx,cy),1)
        #plt.matshow(binary_image)
        #plt.show()
        #print (len(cv.findNonZero(flood_fill[1])))
        if len(cv.findNonZero(flood_fill[1])) < length*0.95:
            print (len(cv.findNonZero(flood_fill[1])))
            return i
            break








def get_start_end_open_end(img):

    
    # to remove non-8point connectivity pixels
    kernel2 = np.array([[1,1,1],[1,0,1],[1,1,1]])

    previous_image = img
    img = cv.filter2D(img, ddepth=-1, kernel=kernel2)

    img = np.absolute(img)
    img = img*previous_image
    unique, counts = np.unique(img, return_counts=True)
    unique = np.delete(unique,0)
    counts = np.delete(counts,0)
    
    end_position = np.where(img==1)
    #print (end_position)
    point = [0,0]
    start, end = determine_points(point, end_position)
    return start, end





def determine_points(point_1, end_points):
    if len(end_points[0]) !=2:
        print ("Danger more than 1 end points")
    R = []
    point_1_val = np.sqrt( point_1[0]**2 + point_1[1]**2)
    for i in range(len(end_points[0])):
        temp_r = np.sqrt( end_points[i][0]**2 + end_points[i][1]**2)
        R.append(temp_r)
    R = np.array(R)
    min_val = np.subtract(R,point_1_val)
    index = np.where(min_val==np.amin(min_val))
    index = index[0][0]
    if index ==1:
        other_index = 0;
    if index ==0:
        other_index = 1
    #print (end_points)
    ## points might be inverted check
    return [end_points[0][index],end_points[1][index]], [end_points[0][other_index],end_points[1][other_index]]





























  

def check_closure(binary_image, Inner_layer_segmented, cx, cy):



    x,y,w,h = cv.boundingRect(binary_image)
    
    #d=cv.rectangle(binary_image,(x,y),(x+w,y+h),(2,2,2),2)
    area_rect = w*h
    peri_rect = 2*(w+h)

    #plt.matshow(d)
    #plt.show()

    peri_hull = len(cv.findNonZero(Inner_layer_segmented))
    flood_fill = cv.floodFill(Inner_layer_segmented,None,(cx,cy),1)
    area_hull = len(cv.findNonZero(flood_fill[1]))
    length = np.shape(binary_image)[0] * np.shape(binary_image)[1]
    
    contours,_ = cv.findContours(Inner_layer_segmented, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_TC89_L1)
    no_of_cnt = len(contours)

    if no_of_cnt == 1 and area_hull < area_rect and area_hull> 0.9*area_rect:
        return True
    else:
        return False
    
    if no_of_cnt > 1:
        
        return False
    #if no_of_cnt == 1 and area_hull > 0.7*area_rect:
        
    #    return False

def checked(binary_image, cx, cy):
    retval, binary_image = cv.threshold(binary_image,0,1,cv.THRESH_BINARY)
    
    for j in range(2,500):
        
        
        kernel = np.ones((j,j),np.uint8)
        binary_image = cv.dilate(binary_image,kernel,iterations=1)
        
        
    
        contours,_ = cv.findContours(binary_image, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_TC89_L1)
        
        if len(contours) > 1:
           contours = clean_extra_contours(contours)

        

    
        hull = []
        for i in range(len(contours)):

            hull.append(cv.convexHull(contours[i], False))  

            x = cv.drawContours(binary_image,contours,-1, (255,255,0), 1)
            #plt.matshow(x)
            #plt.show()
    
            color = (120, 0, 0) #color for convex hull
            
            binary_image = binary_image*0
        for k in range(len(contours)):
            cv.drawContours(binary_image, hull, k, color, lineType=cv.LINE_8)

        retval, Inner_layer_segmented_1 = cv.threshold(binary_image,20,1,cv.THRESH_BINARY+cv.THRESH_OTSU)

        #plt.matshow(Inner_layer_segmented_1,"XXX")
        #plt.show()
        Final_image = Inner_layer_segmented_1.copy()  
        if check_closure(binary_image,Inner_layer_segmented_1, cx, cy) == True:
            
            return Final_image, j
            break
    
    








    '''
    for j in range(0,len(contours)-1):
        if len(contours[j]) in del_item:
            index_to_del.append(j)
    print (index_to_del)

    for k in range(0,len(index_to_del)-1):
        contours[index_to_del[k]] == 0
    print (contours)
    '''
        

    

                   
                            
                            

    '''

    
    for j in range(0,1000):
        no_of_contour = len(contours)
        print (len(contours))
        for k in range(0,len(contours)-1):
            print (k)
            if len(contours[k]) != Max_Con:
            #if Max_Con-len(contours[k]) < 20:
               
               print ("Deleting")
            
               del(contours[k])
               break
    
    '''
            
    print ("After delete")
    print (len(contours))
    print (contours)
        
        

    return contours



def clean_image(image):
    
    return 0 



############################


def get_first_point(Inner_layer_segmented):
    
    r = cv.boundingRect(Inner_layer_segmented)
       
    r_xmax = r[2];
    r_ymax = r[3]
    p1 = (int(r[0]),int(r[1]))
    p2 = (int((r[0])+(r[2])), int(r[1]+r[3]))
    cx = (p1[0]+p2[0])/2
    cy = (p1[1]+p2[1])/2
    M = cv.moments(Inner_layer_segmented)
    cx = int(M["m10"] / M["m00"])
    cy = int(M["m01"] / M["m00"])
    '''
    center_coordinates = (int(cx), int(cy)) 
    radius = 3
    color = (1, 0, 0) 
    thickness = 2
    image = cv.circle(Inner_layer_segmented, center_coordinates, radius, color, thickness)
    plt.matshow(image)
    plt.show()
    '''
    first_point = find_point(Inner_layer_segmented,cx,cy)
    return first_point, cx, cy
    


def find_point(Inner_layer_segmented,cx,cy):
    Line_image = Inner_layer_segmented
    Im_mult = Line_image.copy()
    temp= Line_image.copy()
    
    Im_mult = Im_mult*0;
    cv.line(Im_mult, (int(cx),int(cy)), (int(len(Inner_layer_segmented)/2),0), (1,0,0), thickness=1, lineType=cv.LINE_4, shift=0) # else 4 or 8 at lintype
    #plt.matshow(Im_mult)
    #plt.show()
    Im_mult = (Im_mult*temp)
    #Im_mult = np.array(Im_mult,dtype=np.uint8)
    #print(type(Im_mult))
    #plt.matshow(Im_mult+Line_image)
    #plt.show()
    x = []
    #cv.imshow('jj',Im)
    x = (cv.findNonZero(Im_mult))
    #plt.matshow(Im_mult)
    #print("startingpoint_is")
    #print (x[0][0])
    return x[0][0]




##############################directional matrix


def create_empty_image(image):
    for_save = image.copy()
    for_save = for_save * 0
    return for_save








############# arrange

def change_image(image):
    Input_image = image
    x = (cv.findNonZero(Input_image))
    #print (len(x))
    
    x = np.array(x)
    
    for i in range(0,len(x)):
        coordinate = x[i]
        coordinate_x = int(coordinate[0][1])  #change in coordinate
        coordinate_y = int(coordinate[0][0])  #change in coordinate
        if Input_image[coordinate_x][coordinate_y] !=1:
           Input_image[coordinate_x][coordinate_y] = 1

    return Input_image
    





######################## some old stuff

def check_single_contour(image, cx, cy):
    length = np.shape(image)[0] * np.shape(image)[1]
    #print (length)
    sum_p = 0
    
    for i in range(2,50):
        
        kernel = np.ones((i,i),np.uint8)
        binary_image = cv.dilate(image,kernel,iterations=1)
        
        flood_fill = cv.floodFill(binary_image,None,(cx,cy),1)
        #binary_image = cv.Canny(flood_fill[1],1,1)
        
        #flood_fill = cv.floodFill(binary_image,None,(cx,cy),1)
        binary_image = flood_fill[1]
        #plt.matshow(flood_fill[1])
        #plt.show()
        
        contours,_ = cv.findContours(flood_fill[1], cv.RETR_EXTERNAL, cv.CHAIN_APPROX_TC89_L1)
        #print (len(contours))
       
        if len(contours) == 1 :
            sum_p = sum_p + 1
            #print ("Checked_single_length")
            
        if sum_p == 5:
           #print (len(contours))
           return contours
           break
        if i == 50:
           plt.matshow(binary_image)
           plt.title("ITs going above 40")
           plt.show()
