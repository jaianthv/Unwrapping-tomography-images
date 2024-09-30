
import cv2 as cv
import numpy as np
import os
#import porespy as ps
import sys
import matplotlib.pyplot as plt
from Kernel_calculator import *


def extract_point(Inner_layer_segmented,x_coordinate, y_coordinate):
    intensity = []
    for i in range(len(x_coordinate)):
        intensity.append(Inner_layer_segmented[x_coordinate][y_coordinate])
    return intensity
    
       

def get_image_matrix(Inner_layer_segmented,x,y): # x and y interchanged
    remove_data = [[0,0]]
    I = Inner_layer_segmented
    x_axis = np.shape(Inner_layer_segmented)[0]-1
    y_axis = np.shape(Inner_layer_segmented)[1]-1
    

    R1 = [x-1,y+1]
    if y+1 > y_axis:
       R1 = I[x-1,y]
       R1=0
    else:
       R1 = I[x-1,y+1]

    R2 = [x,y+1]
    if y+1 > y_axis:
       R2 = I[x,y]
       R2=0
    else:
       R2 = I[x,y+1]
       
    R3 = [x+1,y+1]
    
    if x+1 > x_axis:
       #R3 = I[x,y+1]
       R3 = 0
    elif y+1 > y_axis:
       #R3 =I[x+1,y]
       R3=0
    

    else:
       R3 = I[x+1,y+1]
       
    R4 = I[x-1,y]
    
       
    R5 = I[x,y]
    
    R6 = [x+1,y]
    if x+1 > x_axis:
       R6 = I[x,y]
       R6 =0
    else:
       R6 = I[x+1,y]
       
    R7 = I[x-1,y-1]
    
       
    R8 = I[x,y-1]
    

       
    R9 = [x+1,y-1]
    if x+1 > x_axis:
       R9 = I[x,y-1]
       R9=0
    else:
       R9 = I[x+1,y-1]
    

    Position_matrix = [[R1, R2, R3],
                       [R4, R5, R6],
                       [R7, R8, R9]]



    
    '''
    Position_matrix = [[I[x-1][y+1], I[x][y+1], I[x+1][y+1]],
                       [I[x-1][y],   I[x][y],   I[x+1][y]],
                       [I[x-1][y-1], I[x][y-1], I[x+1][y-1]]]

    '''
    #print (Position_matrix)
    Kernel_matrix = np.array(kernel_matrix())
    
    if np.sum(Position_matrix) == 4:
        print ("Replacing 4 points")
        Position_matrix, remove_data = check_corners(Position_matrix,x,y)
        #print (Position_matrix)
        if Position_matrix == None:

            Position_matrix = [[R1, R2, R3],
                               [R4, R5, R6],
                               [R7, R8, R9]]
            '''
            Position_matrix = [[I[x-1][y+1], I[x][y+1], I[x+1][y+1]],
                               [I[x-1][y],   I[x][y],   I[x+1][y]],
                               [I[x-1][y-1], I[x][y-1], I[x+1][y-1]]]
            '''


    if np.sum(Position_matrix) == 5:
        print ("yes yes")
        #print (Position_matrix)
        #temp = [[1,0,0],[0,1,0],[0,0,1]]  # if [100,010,111]

        #temp = [[0,0,1],                [0,1,0],                [1,0,0]]# if [001,010,111]

        #temp = [ [0,1,0], [0,1,0], [0,1,0] ] # if [111,010,010]

        #temp = [ [1,0,0], [0,1,1], [0,0,0]] #if [100,111,100]

        temp = [ [0,1,0], [0,1,0], [1,0,0]]   #if [010,010,111]

        if Position_matrix == [[1, 1, 1], [0, 1, 0], [0, 1, 0]]:
            temp = [ [0,0,1], [0,1,0], [0,1,0]]
            


        Position_matrix = np.multiply(temp,Position_matrix)
        







    '''
    if np.sum(Position_matrix) == 4 and Operate_matrix(Position_matrix, Kernel_matrix) == -14:
        print ("yes yes")
        #plt.matshow(Inner_layer_segmented)
        #plt.show()
        print (Operate_matrix(Position_matrix, Kernel_matrix))
        Position_matrix = [[I[x-1][y+1], I[x][y+1], I[x+1][y+1]],
                           [I[x-1][y],   I[x][y],   0],
                           [I[x-1][y-1], I[x][y-1], I[x+1][y-1]]]
     '''   


            
            
    #print (Position_matrix)
    
    return Position_matrix, remove_data



def two_options(Position_matrix, Previous_point, x, y):
    if np.sum(Position_matrix) == 4 and Operate_matrix(Position_matrix, kernel_matrix()) == 14:
       next_point_1 = [x+1,y]
       next_point_2 = [x,y-1]





       
       #make previous point = 0
       #center point = 0
       # find indices of tow non-zero
       # choose 1st check if the next three points can be found if yes use this as next point
       # if not try second point if the next three poinyts can be found use this as next point
       # provide output with previous point, center point and next point as positional matrix







def kernel_matrix():
    '''
    Kernel = [[-5, 1, 15],
              [2, -1, 4],
              [10, 3, -20]]
    '''
    Kernel = [[-5, 4, 15],
              [-4, -1, -16],
              [10, 8, -20]]
    #print (Kernel)
    return Kernel


def Operate_matrix(Position_matrix, Kernel):
    Position_matrix = np.array(Position_matrix)
    
    Kernel_matrix = np.array(Kernel)
  
    mult = np.multiply(Position_matrix,Kernel_matrix)
  
    result = np.sum(mult)
    #print (result)
    
    return result

def Next_coordinate(result,x,y,previous_point, center_x, center_y, Position_matrix, remove_data, reference): # remove outer - after center_y outer,
    
    remove_coordinate = remove_data
    # vertical 
    if result == 11: #3
       next_coordinate = [x,y+1]
       #extend point from the current position
       
       Next_coordinate_layer = find_correct_point(center_x, center_y, [x-1,y], [x+1,y], result, reference)
       
            
        
        
       if next_coordinate[0] == previous_point[0] and next_coordinate[1] == previous_point[1]:
           
          next_coordinate = [x,y-1]
          
          Next_coordinate_layer = find_correct_point(center_x, center_y, [x-1,y], [x+1,y], result, reference)
         
                                                                              
        
    
             
    # horizontal
    if result == -21: #5
        next_coordinate = [x+1,y]
        
        Next_coordinate_layer = find_correct_point(center_x, center_y, [x,y-1], [x,y+1], result, reference)
        

        
        if next_coordinate[0] == previous_point[0] and next_coordinate[1] == previous_point[1]:
            next_coordinate = [x-1,y]
            #Extend_coordinate = Extend_point_vertical(center_x, center_y, x, y)
            Next_coordinate_layer = find_correct_point(center_x, center_y, [x,y-1], [x,y+1], result, reference)
            
        
        

    # diagonal left
    if result == 24: #unchanged
        next_coordinate = [x+1,y+1]
      
        Next_coordinate_layer_1 = find_correct_point(center_x, center_y, [x,y+1], [x+1,y], result, reference)
        Next_coordinate_layer_2 = find_correct_point(center_x, center_y, [x-1,y], [x,y-1], result, reference)
        
        Next_coordinate_layer = find_right_order(previous_point, Next_coordinate_layer_1, Next_coordinate_layer_2)
       
           
        
        if next_coordinate[0] == previous_point[0] and next_coordinate[1] == previous_point[1]:
            next_coordinate = [x-1,y-1]
            
            Next_coordinate_layer_1 = find_correct_point(center_x, center_y, [x,y+1], [x+1,y], result, reference)
            Next_coordinate_layer_2 = find_correct_point(center_x, center_y, [x-1,y], [x,y-1], result, reference)
            Next_coordinate_layer = find_right_order(previous_point, Next_coordinate_layer_1, Next_coordinate_layer_2)
            
            
    #diagonal right
    if result == -26: #unchanged
        next_coordinate = [x-1,y+1]
        
        Next_coordinate_layer_1 = find_correct_point(center_x, center_y, [x,y+1], [x-1,y], result, reference)
        Next_coordinate_layer_2 = find_correct_point(center_x, center_y, [x+1,y], [x,y-1], result, reference)
        Next_coordinate_layer = find_right_order(previous_point, Next_coordinate_layer_1, Next_coordinate_layer_2)
        

        
        if next_coordinate[0] == previous_point[0] and next_coordinate[1] == previous_point[1]:
            next_coordinate = [x+1,y-1]
          
            #Next_coordinate_layer = find_correct_point(center_x, center_y, [x+1,y+1], [x-1,y-1], result)
            Next_coordinate_layer_1 = find_correct_point(center_x, center_y, [x,y+1], [x-1,y], result, reference)
            Next_coordinate_layer_2 = find_correct_point(center_x, center_y, [x+1,y], [x,y-1], result, reference)
            Next_coordinate_layer = find_right_order(previous_point, Next_coordinate_layer_1, Next_coordinate_layer_2)
           
    
    # straight left top
    if result == 2: #-3
        next_coordinate = [x-1,y+1]
       
        Next_coordinate_layer = find_correct_point(center_x, center_y, [x+1,y], [x-1,y], result, reference)
      
            
        
        if next_coordinate[0] == previous_point[0] and next_coordinate[1] == previous_point[1]:
            next_coordinate = [x,y-1]
            
            Next_coordinate_layer = find_correct_point(center_x, center_y, [x+1,y], [x-1,y], result, reference)
            
        



    # straight right top
    if result == 22:#17
        next_coordinate = [x+1,y+1]
       
        Next_coordinate_layer = find_correct_point(center_x, center_y, [x+1,y], [x-1,y], result, reference)
    
        
        if next_coordinate[0] == previous_point[0] and next_coordinate[1] == previous_point[1]:
            next_coordinate = [x,y-1]
            
            Next_coordinate_layer = find_correct_point(center_x, center_y, [x+1,y], [x-1,y], result, reference)
           

    # straight bottom right
    if result == -17:#-20
        next_coordinate = [x,y+1]
        
        Next_coordinate_layer = find_correct_point(center_x, center_y, [x+1,y], [x-1,y], result, reference)
        
        
        if next_coordinate[0] == previous_point[0] and next_coordinate[1] == previous_point[1]:
            next_coordinate = [x+1,y-1]
            
            Next_coordinate_layer = find_correct_point(center_x, center_y, [x+1,y], [x-1,y], result, reference)
           
        

    # straight bottom left
    if result == 13: #10
        next_coordinate = [x,y+1]
        
        Next_coordinate_layer = find_correct_point(center_x, center_y, [x+1,y], [x-1,y], result, reference)
       
        if next_coordinate[0] == previous_point[0] and next_coordinate[1] == previous_point[1]:
            next_coordinate = [x-1,y-1]
           
            Next_coordinate_layer = find_correct_point(center_x, center_y, [x+1,y], [x-1,y], result, reference)
            
        
           
            

    # horizontal top right
    if result == 10: #16
        next_coordinate = [x+1,y+1]
        
        Next_coordinate_layer = find_correct_point(center_x, center_y, [x,y+1], [x,y-1], result, reference)
       
            
        if next_coordinate[0] == previous_point[0] and next_coordinate[1] == previous_point[1]:
            next_coordinate = [x-1,y]
            
            Next_coordinate_layer = find_correct_point(center_x, center_y, [x,y+1], [x,y-1], result, reference)
            


    # horizontal bottom right
    if result == -25 and np.sum(Position_matrix) == 3: #-19
        next_coordinate = [x+1,y-1]
        
        Next_coordinate_layer = find_correct_point(center_x, center_y, [x,y+1], [x,y-1], result, reference)
        #remove_coordinate = [[x+1,y]]
     
        if next_coordinate[0] == previous_point[0] and next_coordinate[1] == previous_point[1]:
            next_coordinate = [x-1,y]
          
            Next_coordinate_layer = find_correct_point(center_x, center_y, [x,y+1], [x,y-1], result, reference)
            #remove_coordinate = [[x+1,y]]
           
        


    # horizontal top left
    if result == -22 and np.sum(Position_matrix) == 3: #-2
        next_coordinate = [x+1,y]
        
        Next_coordinate_layer = find_correct_point(center_x, center_y, [x,y+1], [x,y-1], result, reference)
       
        if next_coordinate[0] == previous_point[0] and next_coordinate[1] == previous_point[1]:
            next_coordinate = [x-1,y+1]
            
            Next_coordinate_layer = find_correct_point(center_x, center_y, [x,y+1], [x,y-1], result, reference)
          
        

    # horizontal bottom left
    if result == -7:#13
        next_coordinate = [x+1,y]
        
        Next_coordinate_layer = find_correct_point(center_x, center_y, [x,y+1], [x,y-1], result, reference)
       
        if next_coordinate[0] == previous_point[0] and next_coordinate[1] == previous_point[1]:
            next_coordinate = [x-1,y-1]
           
            Next_coordinate_layer = find_correct_point(center_x, center_y, [x,y+1], [x,y-1], result, reference)
           
        

    # arrow shape right
    if result == 4 and np.sum(Position_matrix) == 3:
        next_coordinate = [x-1,y+1]
        
        Next_coordinate_layer = find_correct_point(center_x, center_y, [x-1,y], [x+1,y], result, reference)
     
        if next_coordinate[0] == previous_point[0] and next_coordinate[1] == previous_point[1]:
            next_coordinate = [x-1,y-1]
            
            Next_coordinate_layer = find_correct_point(center_x, center_y, [x-1,y], [x+1,y], result, reference)
            
    # arrow shape left
    if result == -6:
        next_coordinate = [x+1,y+1]
        
        Next_coordinate_layer = find_correct_point(center_x, center_y, [x-1,y], [x+1,y], result, reference)
        
        if next_coordinate[0] == previous_point[0] and next_coordinate[1] == previous_point[1]:
            next_coordinate = [x+1,y-1]
            
            Next_coordinate_layer = find_correct_point(center_x, center_y, [x-1,y], [x+1,y], result, reference)
            


    # arrow shape down
    if result == 9:
        next_coordinate = [x+1,y+1]
        
        Next_coordinate_layer = find_correct_point(center_x, center_y, [x,y-1], [x,y+1], result, reference)
        
            
        if next_coordinate[0] == previous_point[0] and next_coordinate[1] == previous_point[1]:
            next_coordinate = [x-1,y+1]
            
            Next_coordinate_layer = find_correct_point(center_x, center_y, [x,y-1], [x,y+1], result, reference)
          
            
        

    # arrow shape up
    if result == -11:
        next_coordinate = [x+1,y-1]
        
        Next_coordinate_layer = find_correct_point(center_x, center_y, [x,y-1], [x,y+1], result, reference)
       
            
        if next_coordinate[0] == previous_point[0] and next_coordinate[1] == previous_point[1]:
            next_coordinate = [x-1,y-1]
            
            Next_coordinate_layer = find_correct_point(center_x, center_y, [x,y-1], [x,y+1], result, reference)
           



    # 4 point
    
    if result == 32 and np.sum(Position_matrix) == 4:
        next_coordinate = [x+1,y+1]
        
       
        Next_coordinate_layer_1 = find_correct_point(center_x, center_y, [x,y+1], [x+1,y], result, reference)
        Next_coordinate_layer_2 = find_correct_point(center_x, center_y, [x-1,y], [x,y-1], result, reference)
        Next_coordinate_layer = find_right_order(previous_point, Next_coordinate_layer_1, Next_coordinate_layer_2)
       
        
        if next_coordinate[0] == previous_point[0] and next_coordinate[1] == previous_point[1]:
            next_coordinate = [x-1,y-1]
           
            Next_coordinate_layer_1 = find_correct_point(center_x, center_y, [x,y+1], [x+1,y], result, reference)
            Next_coordinate_layer_2 = find_correct_point(center_x, center_y, [x-1,y], [x,y-1], result, reference)
            Next_coordinate_layer = find_right_order(previous_point, Next_coordinate_layer_1, Next_coordinate_layer_2)
            
            
    
    if result == 8 and np.sum(Position_matrix) == 4:
        next_coordinate = [x+1,y+1]
        
        Next_coordinate_layer_1 = find_correct_point(center_x, center_y, [x,y+1], [x+1,y], result, reference)
        Next_coordinate_layer_2 = find_correct_point(center_x, center_y, [x-1,y], [x,y-1], result, reference)
        Next_coordinate_layer = find_right_order(previous_point, Next_coordinate_layer_1, Next_coordinate_layer_2)
 
           
        
        if next_coordinate[0] == previous_point[0] and next_coordinate[1] == previous_point[1]:
            next_coordinate = [x-1,y-1]
            
            Next_coordinate_layer_1 = find_correct_point(center_x, center_y, [x,y+1], [x+1,y], result, reference)
            Next_coordinate_layer_2 = find_correct_point(center_x, center_y, [x-1,y], [x,y-1], result, reference)
            Next_coordinate_layer = find_right_order(previous_point, Next_coordinate_layer_1, Next_coordinate_layer_2)
          
            
      
    if result == 28 and np.sum(Position_matrix) == 4: #unchanged
        next_coordinate = [x+1,y+1]
        
        Next_coordinate_layer_1 = find_correct_point(center_x, center_y, [x,y+1], [x+1,y], result, reference)
        Next_coordinate_layer_2 = find_correct_point(center_x, center_y, [x-1,y], [x,y-1], result, reference)
        Next_coordinate_layer = find_right_order(previous_point, Next_coordinate_layer_1, Next_coordinate_layer_2)
        
           
        
        if next_coordinate[0] == previous_point[0] and next_coordinate[1] == previous_point[1]:
            next_coordinate = [x-1,y-1]
            
            Next_coordinate_layer_1 = find_correct_point(center_x, center_y, [x,y+1], [x+1,y], result, reference)
            Next_coordinate_layer_2 = find_correct_point(center_x, center_y, [x-1,y], [x,y-1], result, reference)
            Next_coordinate_layer = find_right_order(previous_point, Next_coordinate_layer_1, Next_coordinate_layer_2)
            
            
    
    if result == 20 and np.sum(Position_matrix) == 4: #unchanged
        next_coordinate = [x+1,y+1]
        
        Next_coordinate_layer_1 = find_correct_point(center_x, center_y, [x,y+1], [x+1,y], result, reference)
        Next_coordinate_layer_2 = find_correct_point(center_x, center_y, [x-1,y], [x,y-1], result, reference)
        Next_coordinate_layer = find_right_order(previous_point, Next_coordinate_layer_1, Next_coordinate_layer_2)
      
           
        
        if next_coordinate[0] == previous_point[0] and next_coordinate[1] == previous_point[1]:
            next_coordinate = [x-1,y-1]
            
            Next_coordinate_layer_1 = find_correct_point(center_x, center_y, [x,y+1], [x+1,y], result, reference)
            Next_coordinate_layer_2 = find_correct_point(center_x, center_y, [x-1,y], [x,y-1], result, reference)
            Next_coordinate_layer = find_right_order(previous_point, Next_coordinate_layer_1, Next_coordinate_layer_2)
            
           
    if result == -30 and np.sum(Position_matrix) == 4: #unchanged
        next_coordinate = [x-1,y+1]
        
        Next_coordinate_layer_1 = find_correct_point(center_x, center_y, [x,y+1], [x-1,y], result, reference)
        Next_coordinate_layer_2 = find_correct_point(center_x, center_y, [x+1,y], [x,y-1], result, reference)
        Next_coordinate_layer = find_right_order(previous_point, Next_coordinate_layer_1, Next_coordinate_layer_2)


        
        if next_coordinate[0] == previous_point[0] and next_coordinate[1] == previous_point[1]:
            next_coordinate = [x+1,y-1]
           
            #Next_coordinate_layer = find_correct_point(center_x, center_y, [x+1,y+1], [x-1,y-1], result)
            Next_coordinate_layer_1 = find_correct_point(center_x, center_y, [x,y+1], [x-1,y], result, reference)
            Next_coordinate_layer_2 = find_correct_point(center_x, center_y, [x+1,y], [x,y-1], result, reference)
            Next_coordinate_layer = find_right_order(previous_point, Next_coordinate_layer_1, Next_coordinate_layer_2)
 
    
    

    if result == -18 and np.sum(Position_matrix) ==4 : #unchanged
        next_coordinate = [x-1,y+1]
        
        Next_coordinate_layer_1 = find_correct_point(center_x, center_y, [x,y+1], [x-1,y], result, reference)
        Next_coordinate_layer_2 = find_correct_point(center_x, center_y, [x+1,y], [x,y-1], result, reference)
        Next_coordinate_layer = find_right_order(previous_point, Next_coordinate_layer_1, Next_coordinate_layer_2)
 

        
        if next_coordinate[0] == previous_point[0] and next_coordinate[1] == previous_point[1]:
            next_coordinate = [x+1,y-1]
            
            #Next_coordinate_layer = find_correct_point(center_x, center_y, [x+1,y+1], [x-1,y-1], result)
            Next_coordinate_layer_1 = find_correct_point(center_x, center_y, [x,y+1], [x-1,y], result, reference)
            Next_coordinate_layer_2 = find_correct_point(center_x, center_y, [x+1,y], [x,y-1], result, reference)
            Next_coordinate_layer = find_right_order(previous_point, Next_coordinate_layer_1, Next_coordinate_layer_2)

            
    if result == -42 and np.sum(Position_matrix) == 4: #unchanged
        next_coordinate = [x-1,y+1]
       
        Next_coordinate_layer_1 = find_correct_point(center_x, center_y, [x,y+1], [x-1,y], result, reference)
        Next_coordinate_layer_2 = find_correct_point(center_x, center_y, [x+1,y], [x,y-1], result, reference)
        Next_coordinate_layer = find_right_order(previous_point, Next_coordinate_layer_1, Next_coordinate_layer_2)


        
        if next_coordinate[0] == previous_point[0] and next_coordinate[1] == previous_point[1]:
            next_coordinate = [x+1,y-1]
            
            #Next_coordinate_layer = find_correct_point(center_x, center_y, [x+1,y+1], [x-1,y-1], result)
            Next_coordinate_layer_1 = find_correct_point(center_x, center_y, [x,y+1], [x-1,y], result, reference)
            Next_coordinate_layer_2 = find_correct_point(center_x, center_y, [x+1,y], [x,y-1], result, reference)
            Next_coordinate_layer = find_right_order(previous_point, Next_coordinate_layer_1, Next_coordinate_layer_2)

    
    if result == -22 and np.sum(Position_matrix) == 4: #unchanged
        next_coordinate = [x-1,y+1]
        
        Next_coordinate_layer_1 = find_correct_point(center_x, center_y, [x,y+1], [x-1,y], result, reference)
        Next_coordinate_layer_2 = find_correct_point(center_x, center_y, [x+1,y], [x,y-1], result, reference)
        Next_coordinate_layer = find_right_order(previous_point, Next_coordinate_layer_1, Next_coordinate_layer_2)


        
        if next_coordinate[0] == previous_point[0] and next_coordinate[1] == previous_point[1]:
            next_coordinate = [x+1,y-1]
            
            Next_coordinate_layer_1 = find_correct_point(center_x, center_y, [x,y+1], [x-1,y], result, reference)
            Next_coordinate_layer_2 = find_correct_point(center_x, center_y, [x+1,y], [x,y-1], result, reference)
            Next_coordinate_layer = find_right_order(previous_point, Next_coordinate_layer_1, Next_coordinate_layer_2)


    
    if result == 26 and np.sum(Position_matrix) ==4:#17
        next_coordinate = [x+1,y+1]
        remove_coordinate = [[x,y+1]]
        
        Next_coordinate_layer = find_correct_point(center_x, center_y, [x+1,y], [x-1,y], result, reference)

        
        if next_coordinate[0] == previous_point[0] and next_coordinate[1] == previous_point[1]:
            next_coordinate = [x,y-1]
            remove_coordinate = [[x,y+1]]
            
            Next_coordinate_layer = find_correct_point(center_x, center_y, [x+1,y], [x-1,y], result, reference)
      
        
    if result == 6 and np.sum(Position_matrix) ==4: #-3
       next_coordinate = [x-1,y+1]
       remove_coordinate = [[x,y+1]]
       
       Next_coordinate_layer = find_correct_point(center_x, center_y, [x+1,y], [x-1,y], result, reference)
   
            
        
       if next_coordinate[0] == previous_point[0] and next_coordinate[1] == previous_point[1]:
           next_coordinate = [x,y-1]
           remove_coordinate = [[x,y+1]]
           
           Next_coordinate_layer = find_correct_point(center_x, center_y, [x+1,y], [x-1,y], result, reference)
    
        
    if result == 21 and np.sum(Position_matrix) == 4: #10
        next_coordinate = [x,y+1]
        remove_coordinate = [[x,y-1]]
        
        Next_coordinate_layer = find_correct_point(center_x, center_y, [x+1,y], [x-1,y], result, reference)
  
        if next_coordinate[0] == previous_point[0] and next_coordinate[1] == previous_point[1]:
            next_coordinate = [x-1,y-1]
            remove_coordinate = [[x,y-1]]
            
            Next_coordinate_layer = find_correct_point(center_x, center_y, [x+1,y], [x-1,y], result, reference)
        

    if result == -9 and np.sum(Position_matrix) == 4:#-20
        next_coordinate = [x,y+1]
        remove_coordinate = [[x,y-1]]
        
        Next_coordinate_layer = find_correct_point(center_x, center_y, [x+1,y], [x-1,y], result, reference)
  
        
        if next_coordinate[0] == previous_point[0] and next_coordinate[1] == previous_point[1]:
            next_coordinate = [x+1,y-1]
            remove_coordinate = [[x,y-1]]
            
            Next_coordinate_layer = find_correct_point(center_x, center_y, [x+1,y], [x-1,y], result, reference)









    if result == -6 and np.sum(Position_matrix) ==4: #16
        next_coordinate = [x+1,y+1]
        remove_coordinate = [[x+1,y]]
        
        Next_coordinate_layer = find_correct_point(center_x, center_y, [x,y+1], [x,y-1], result, reference)

            
        if next_coordinate[0] == previous_point[0] and next_coordinate[1] == previous_point[1]:
            next_coordinate = [x-1,y]
            remove_coordinate = [[x+1,y]]
           
            Next_coordinate_layer = find_correct_point(center_x, center_y, [x,y+1], [x,y-1], result, reference)



    



     # horizontal top left
    if result == -26 and np.sum(Position_matrix) == 4: #-2
        next_coordinate = [x+1,y]
        remove_coordinate = [[x-1,y]]
        
        Next_coordinate_layer = find_correct_point(center_x, center_y, [x,y+1], [x,y-1], result, reference)

        if next_coordinate[0] == previous_point[0] and next_coordinate[1] == previous_point[1]:
            next_coordinate = [x-1,y+1]
            remove_coordinate = [[x-1,y]]
            
            Next_coordinate_layer = find_correct_point(center_x, center_y, [x,y+1], [x,y-1], result, reference)
          
        

    if result == -11 and np.sum(Position_matrix) == 4:#13
        next_coordinate = [x+1,y]
        remove_coordinate = [[x-1,y]]
        
        Next_coordinate_layer = find_correct_point(center_x, center_y, [x,y+1], [x,y-1], result, reference)
   
        if next_coordinate[0] == previous_point[0] and next_coordinate[1] == previous_point[1]:
            next_coordinate = [x-1,y-1]
            remove_coordinate = [[x-1,y]]
            
            Next_coordinate_layer = find_correct_point(center_x, center_y, [x,y+1], [x,y-1], result, reference)

        
  


    if result == -41 and np.sum(Position_matrix) == 4: #-19
       next_coordinate = [x+1,y-1]
       remove_coordinate = [[x+1,y]]
       #Extend_coordinate = Extend_point_vertical(center_x, center_y, x, y)
       #Extend_coordinate = guess_orienHOV(center_x, center_y, x, y)
       Next_coordinate_layer = find_correct_point(center_x, center_y, [x,y+1], [x,y-1], result, reference)
      
       if next_coordinate[0] == previous_point[0] and next_coordinate[1] == previous_point[1]:
           next_coordinate = [x-1,y]
           remove_coordinate = [[x+1,y]]
           
           Next_coordinate_layer = find_correct_point(center_x, center_y, [x,y+1], [x,y-1], result, reference)
           
        

    # straight left top
    if result == -14 and np.sum(Position_matrix) == 4: #-3
        next_coordinate = [x-1,y+1]
        remove_coordinate = [[x+1,y]]
        print (remove_coordinate)
        
        Next_coordinate_layer = find_correct_point(center_x, center_y, [x+1,y], [x-1,y], result, reference)
    
            
        
        if next_coordinate[0] == previous_point[0] and next_coordinate[1] == previous_point[1]:
            next_coordinate = [x,y-1]
            remove_coordinate = [[x+1,y]]
            print ("xxx")
            print (remove_coordinate)
            
            Next_coordinate_layer = find_correct_point(center_x, center_y, [x+1,y], [x-1,y], result, reference)
          
  

    if result == 5 and np.sum(Position_matrix) ==4:
        next_coordinate = [x+1,y+1]
        
        Next_coordinate_layer = find_correct_point(center_x, center_y, [x,y-1], [x,y+1], result, reference)
       
            
        if next_coordinate[0] == previous_point[0] and next_coordinate[1] == previous_point[1]:
            next_coordinate = [x-1,y+1]
            
            Next_coordinate_layer = find_correct_point(center_x, center_y, [x,y-1], [x,y+1], result, reference)
           
            
    if result == -25 and np.sum(Position_matrix) == 4: #-19
       next_coordinate = [x+1,y-1]
       
       Next_coordinate_layer = find_correct_point(center_x, center_y, [x,y+1], [x,y-1], result, reference)
    
       if next_coordinate[0] == previous_point[0] and next_coordinate[1] == previous_point[1]:
           next_coordinate = [x-1,y]
           
           Next_coordinate_layer = find_correct_point(center_x, center_y, [x,y+1], [x,y-1], result, reference)
          


    if result == -21 and np.sum(Position_matrix) == 4: #-19
       next_coordinate = [x,y+1]
       remove_coordinate =[[x-1,y]]
       
       Next_coordinate_layer = find_correct_point(center_x, center_y, [x,y+1], [x,y-1], result, reference)
       
       if next_coordinate[0] == previous_point[0] and next_coordinate[1] == previous_point[1]:
           next_coordinate = [x+1,y-1]
           remove_coordinate =[[x-1,y]]
           
           Next_coordinate_layer = find_correct_point(center_x, center_y, [x,y+1], [x,y-1], result, reference)
        


    if result == 18 and np.sum(Position_matrix) == 4: #-19
       next_coordinate = [x+1,y+1]
       remove_coordinate =[[x-1,y]]
       
       Next_coordinate_layer = find_correct_point(center_x, center_y, [x,y+1], [x,y-1], result, reference)
     
       if next_coordinate[0] == previous_point[0] and next_coordinate[1] == previous_point[1]:
           next_coordinate = [x,y-1]
           remove_coordinate =[[x-1,y]]
           
           Next_coordinate_layer = find_correct_point(center_x, center_y, [x,y+1], [x,y-1], result, reference)
       

    '''
    if remove_coordinate == None:
       remove_coordinate = [0,0]
    else:
       remove_coordinate = remove_coordinate_14
       print (remove_coordinate)

   '''
        
    
    #print (result)    
    #print (next_coordinate)
    #print (Extend_coordinate)
    #print (remove_coordinate)


               
    return next_coordinate, Next_coordinate_layer, remove_coordinate






#### Fast


def Next_coordinate_fast(result,x,y,previous_point, center_x, center_y, Position_matrix, reference, pts):
    
    #remove_coordinate = remove_data
    # vertical 
    if result == 11: #3
       next_coordinate = [x,y+1]
       #extend point from the current position
       Extend_coordinate = Extend_point_horizontal(center_x, center_y, x, y, pts, reference)
      
        
        
       if next_coordinate[0] == previous_point[0] and next_coordinate[1] == previous_point[1]:
           
          next_coordinate = [x,y-1]
          Extend_coordinate = Extend_point_horizontal(center_x, center_y, x, y, pts, reference)
          
                                                                              
        
    
             
    # horizontal
    if result == -21: #5
        next_coordinate = [x+1,y]
        Extend_coordinate = Extend_point_vertical(center_x, center_y, x, y, pts, reference)
       

        
        if next_coordinate[0] == previous_point[0] and next_coordinate[1] == previous_point[1]:
            next_coordinate = [x-1,y]
            Extend_coordinate = Extend_point_vertical(center_x, center_y, x, y, pts, reference)
            

    # diagonal left
    if result == 24: #unchanged
        next_coordinate = [x+1,y+1]
        Extend_coordinate = guess_orienHOV(center_x, center_y, x, y, pts, reference)
        
                  
        
        if next_coordinate[0] == previous_point[0] and next_coordinate[1] == previous_point[1]:
            next_coordinate = [x-1,y-1]
            Extend_coordinate = guess_orienHOV(center_x, center_y, x, y, pts, reference)
            
            
    #diagonal right
    if result == -26: #unchanged
        next_coordinate = [x-1,y+1]
        Extend_coordinate = guess_orienHOV(center_x, center_y, x, y, pts, reference)
       
        
        if next_coordinate[0] == previous_point[0] and next_coordinate[1] == previous_point[1]:
            next_coordinate = [x+1,y-1]
            Extend_coordinate = guess_orienHOV(center_x, center_y, x, y, pts, reference)
            
    
    # straight left top
    if result == 2: #-3
        next_coordinate = [x-1,y+1]
        Extend_coordinate = Extend_point_horizontal(center_x, center_y, x, y, pts, reference)
       
            
        
        if next_coordinate[0] == previous_point[0] and next_coordinate[1] == previous_point[1]:
            next_coordinate = [x,y-1]
            Extend_coordinate = Extend_point_horizontal(center_x, center_y, x, y, pts, reference)

           
    # straight right top
    if result == 22:#17
        next_coordinate = [x+1,y+1]
        Extend_coordinate = Extend_point_horizontal(center_x, center_y, x, y, pts, reference)
       
        
        if next_coordinate[0] == previous_point[0] and next_coordinate[1] == previous_point[1]:
            next_coordinate = [x,y-1]
            Extend_coordinate = Extend_point_horizontal(center_x, center_y, x, y, pts, reference)
            
    # straight bottom right
    if result == -17:#-20
        next_coordinate = [x,y+1]
        Extend_coordinate = Extend_point_horizontal(center_x, center_y, x, y, pts, reference)
                
        if next_coordinate[0] == previous_point[0] and next_coordinate[1] == previous_point[1]:
            next_coordinate = [x+1,y-1]
            Extend_coordinate = Extend_point_horizontal(center_x, center_y, x, y, pts, reference)
           

    # straight bottom left
    if result == 13: #10
        next_coordinate = [x,y+1]
        Extend_coordinate = Extend_point_horizontal(center_x, center_y, x, y, pts, reference)
           
        if next_coordinate[0] == previous_point[0] and next_coordinate[1] == previous_point[1]:
            next_coordinate = [x-1,y-1]
            Extend_coordinate = Extend_point_horizontal(center_x, center_y, x, y, pts, reference)
        
           
            

    # horizontal top right
    if result == 10: #16
        next_coordinate = [x+1,y+1]
        Extend_coordinate = Extend_point_vertical(center_x, center_y, x, y, pts, reference)

            
        if next_coordinate[0] == previous_point[0] and next_coordinate[1] == previous_point[1]:
            next_coordinate = [x-1,y]
            Extend_coordinate = Extend_point_vertical(center_x, center_y, x, y, pts, reference)
        


    # horizontal bottom right
    if result == -25 and np.sum(Position_matrix) == 3: #-19
        next_coordinate = [x+1,y-1]
        Extend_coordinate = Extend_point_vertical(center_x, center_y, x, y, pts, reference)
        
        if next_coordinate[0] == previous_point[0] and next_coordinate[1] == previous_point[1]:
            next_coordinate = [x-1,y]
            Extend_coordinate = Extend_point_vertical(center_x, center_y, x, y, pts, reference)
            
        


    # horizontal top left
    if result == -22 and np.sum(Position_matrix) == 3: #-2
        next_coordinate = [x+1,y]
        Extend_coordinate = Extend_point_vertical(center_x, center_y, x, y, pts, reference)
       
           
        if next_coordinate[0] == previous_point[0] and next_coordinate[1] == previous_point[1]:
            next_coordinate = [x-1,y+1]
            Extend_coordinate = Extend_point_vertical(center_x, center_y, x, y, pts, reference)
        

    # horizontal bottom left
    if result == -7:#13
        next_coordinate = [x+1,y]
        Extend_coordinate = Extend_point_vertical(center_x, center_y, x, y, pts, reference)
       
        if next_coordinate[0] == previous_point[0] and next_coordinate[1] == previous_point[1]:
            next_coordinate = [x-1,y-1]
            Extend_coordinate = Extend_point_vertical(center_x, center_y, x, y, pts, reference)
            

    # arrow shape right
    if result == 4 and np.sum(Position_matrix) == 3:
        next_coordinate = [x-1,y+1]
        #Extend_coordinate = Extend_point_horizontal(center_x, center_y, x, y)
        Extend_coordinate = guess_orienHOV(center_x, center_y, x, y, pts, reference)
        
        if next_coordinate[0] == previous_point[0] and next_coordinate[1] == previous_point[1]:
            next_coordinate = [x-1,y-1]
            #Extend_coordinate = Extend_point_horizontal(center_x, center_y, x, y)
            Extend_coordinate = guess_orienHOV(center_x, center_y, x, y, pts, reference)
           

    # arrow shape left
    if result == -6:
        next_coordinate = [x+1,y+1]
        #Extend_coordinate = Extend_point_horizontal(center_x, center_y, x, y)
        Extend_coordinate = guess_orienHOV(center_x, center_y, x, y, pts, reference)
       
        if next_coordinate[0] == previous_point[0] and next_coordinate[1] == previous_point[1]:
            next_coordinate = [x+1,y-1]
            #Extend_coordinate = Extend_point_horizontal(center_x, center_y, x, y)
            Extend_coordinate = guess_orienHOV(center_x, center_y, x, y, pts, reference)
            

    # arrow shape down
    if result == 9:
        next_coordinate = [x+1,y+1]
        #Extend_coordinate = Extend_point_vertical(center_x, center_y, x, y)
        Extend_coordinate = guess_orienHOV(center_x, center_y, x, y, pts, reference)
        
        if next_coordinate[0] == previous_point[0] and next_coordinate[1] == previous_point[1]:
            next_coordinate = [x-1,y+1]
            #Extend_coordinate = Extend_point_vertical(center_x, center_y, x, y)
            Extend_coordinate = guess_orienHOV(center_x, center_y, x, y, pts, reference)
             
        

    # arrow shape up
    if result == -11:
        next_coordinate = [x+1,y-1]
        #Extend_coordinate = Extend_point_vertical(center_x, center_y, x, y)
        Extend_coordinate = guess_orienHOV(center_x, center_y, x, y, pts, reference)
            
        if next_coordinate[0] == previous_point[0] and next_coordinate[1] == previous_point[1]:
            next_coordinate = [x-1,y-1]
            #Extend_coordinate = Extend_point_vertical(center_x, center_y, x, y)
            Extend_coordinate = guess_orienHOV(center_x, center_y, x, y, pts, reference)
            


    # 4 point
    
    if result == 32 and np.sum(Position_matrix) == 4:
        next_coordinate = [x+1,y+1]
        
        Extend_coordinate = guess_orienHOV(center_x, center_y, x, y, pts, reference)
      
        
        if next_coordinate[0] == previous_point[0] and next_coordinate[1] == previous_point[1]:
            next_coordinate = [x-1,y-1]
            Extend_coordinate = guess_orienHOV(center_x, center_y, x, y, pts, reference)
            
    
    if result == 8 and np.sum(Position_matrix) == 4:
        next_coordinate = [x+1,y+1]
        Extend_coordinate = guess_orienHOV(center_x, center_y, x, y, pts, reference)
       
        
        if next_coordinate[0] == previous_point[0] and next_coordinate[1] == previous_point[1]:
            next_coordinate = [x-1,y-1]
            Extend_coordinate = guess_orienHOV(center_x, center_y, x, y, pts, reference)
           
      
    if result == 28 and np.sum(Position_matrix) == 4: #unchanged
        next_coordinate = [x+1,y+1]
        Extend_coordinate = guess_orienHOV(center_x, center_y, x, y, pts, reference)
         
        
        if next_coordinate[0] == previous_point[0] and next_coordinate[1] == previous_point[1]:
            next_coordinate = [x-1,y-1]
            Extend_coordinate = guess_orienHOV(center_x, center_y, x, y, pts, reference)
            
    
    if result == 20 and np.sum(Position_matrix) == 4: #unchanged
        next_coordinate = [x+1,y+1]
        Extend_coordinate = guess_orienHOV(center_x, center_y, x, y, pts, reference)
         
        
        if next_coordinate[0] == previous_point[0] and next_coordinate[1] == previous_point[1]:
            next_coordinate = [x-1,y-1]
            Extend_coordinate = guess_orienHOV(center_x, center_y, x, y, pts, reference)
            
    if result == -30 and np.sum(Position_matrix) == 4: #unchanged
        next_coordinate = [x-1,y+1]
        Extend_coordinate = guess_orienHOV(center_x, center_y, x, y, pts, reference)
        
        
        if next_coordinate[0] == previous_point[0] and next_coordinate[1] == previous_point[1]:
            next_coordinate = [x+1,y-1]
            Extend_coordinate = guess_orienHOV(center_x, center_y, x, y, pts, reference)
           
    

    if result == -18 and np.sum(Position_matrix) ==4 : #unchanged
        next_coordinate = [x-1,y+1]
        Extend_coordinate = guess_orienHOV(center_x, center_y, x, y, pts, reference)
        
        
        if next_coordinate[0] == previous_point[0] and next_coordinate[1] == previous_point[1]:
            next_coordinate = [x+1,y-1]
            Extend_coordinate = guess_orienHOV(center_x, center_y, x, y, pts, reference)
            
    if result == -42 and np.sum(Position_matrix) == 4: #unchanged
        next_coordinate = [x-1,y+1]
        Extend_coordinate = guess_orienHOV(center_x, center_y, x, y, pts, reference)
        
        
        if next_coordinate[0] == previous_point[0] and next_coordinate[1] == previous_point[1]:
            next_coordinate = [x+1,y-1]
            Extend_coordinate = guess_orienHOV(center_x, center_y, x, y, pts, reference)
            
    if result == -22 and np.sum(Position_matrix) == 4: #unchanged
        next_coordinate = [x-1,y+1]
        Extend_coordinate = guess_orienHOV(center_x, center_y, x, y, pts, reference)
        
        
        if next_coordinate[0] == previous_point[0] and next_coordinate[1] == previous_point[1]:
            next_coordinate = [x+1,y-1]
            Extend_coordinate = guess_orienHOV(center_x, center_y, x, y, pts, reference)
        

    
    if result == 26 and np.sum(Position_matrix) ==4:#17
        next_coordinate = [x+1,y+1]
        remove_coordinate = [[x,y+1]]
        Extend_coordinate = Extend_point_horizontal(center_x, center_y, x, y, pts, reference)
        
        
        if next_coordinate[0] == previous_point[0] and next_coordinate[1] == previous_point[1]:
            next_coordinate = [x,y-1]
            remove_coordinate = [[x,y+1]]
            Extend_coordinate = Extend_point_horizontal(center_x, center_y, x, y, pts, reference)
            
        
    if result == 6 and np.sum(Position_matrix) ==4: #-3
       next_coordinate = [x-1,y+1]
       remove_coordinate = [[x,y+1]]
       #Extend_coordinate = Extend_point_horizontal(center_x, center_y, x, y)
       Extend_coordinate = guess_orienHOV(center_x, center_y, x, y, pts, reference)
      
            
        
       if next_coordinate[0] == previous_point[0] and next_coordinate[1] == previous_point[1]:
           next_coordinate = [x,y-1]
           remove_coordinate = [[x,y+1]]
           Extend_coordinate = Extend_point_horizontal(center_x, center_y, x, y, pts, reference)
          
        
    if result == 21 and np.sum(Position_matrix) == 4: #10
        next_coordinate = [x,y+1]
        remove_coordinate = [[x,y-1]]
        #Extend_coordinate = Extend_point_horizontal(center_x, center_y, x, y)
        Extend_coordinate = guess_orienHOV(center_x, center_y, x, y, pts, reference)
        

        if next_coordinate[0] == previous_point[0] and next_coordinate[1] == previous_point[1]:
            next_coordinate = [x-1,y-1]
            remove_coordinate = [[x,y-1]]
            #Extend_coordinate = Extend_point_horizontal(center_x, center_y, x, y)
            Extend_coordinate = guess_orienHOV(center_x, center_y, x, y, pts, reference)
        
    if result == -9 and np.sum(Position_matrix) == 4:#-20
        next_coordinate = [x,y+1]
        remove_coordinate = [[x,y-1]]
        Extend_coordinate = Extend_point_horizontal(center_x, center_y, x, y, pts, reference)
        
        if next_coordinate[0] == previous_point[0] and next_coordinate[1] == previous_point[1]:
            next_coordinate = [x+1,y-1]
            remove_coordinate = [[x,y-1]]
            Extend_coordinate = Extend_point_horizontal(center_x, center_y, x, y, pts, reference)
        







    if result == -6 and np.sum(Position_matrix) ==4: #16
        next_coordinate = [x+1,y+1]
        remove_coordinate = [[x+1,y]]
        Extend_coordinate = Extend_point_vertical(center_x, center_y, x, y, pts, reference)
            
        if next_coordinate[0] == previous_point[0] and next_coordinate[1] == previous_point[1]:
            next_coordinate = [x-1,y]
            remove_coordinate = [[x+1,y]]
            Extend_coordinate = Extend_point_vertical(center_x, center_y, x, y, pts, reference)
        


    



     # horizontal top left
    if result == -26 and np.sum(Position_matrix) == 4: #-2
        next_coordinate = [x+1,y]
        remove_coordinate = [[x-1,y]]
        Extend_coordinate = Extend_point_vertical(center_x, center_y, x, y, pts, reference)
        #Extend_coordinate = guess_orienHOV(center_x, center_y, x, y)
        
        if next_coordinate[0] == previous_point[0] and next_coordinate[1] == previous_point[1]:
            next_coordinate = [x-1,y+1]
            remove_coordinate = [[x-1,y]]
            Extend_coordinate = Extend_point_vertical(center_x, center_y, x, y, pts, reference)
            

    if result == -11 and np.sum(Position_matrix) == 4:#13
        next_coordinate = [x+1,y]
        remove_coordinate = [[x-1,y]]
        Extend_coordinate = Extend_point_vertical(center_x, center_y, x, y, pts, reference)
        
        if next_coordinate[0] == previous_point[0] and next_coordinate[1] == previous_point[1]:
            next_coordinate = [x-1,y-1]
            remove_coordinate = [[x-1,y]]
            Extend_coordinate = Extend_point_vertical(center_x, center_y, x, y, pts, reference)
            
        
  


    if result == -41 and np.sum(Position_matrix) == 4: #-19
       next_coordinate = [x+1,y-1]
       remove_coordinate = [[x+1,y]]
       Extend_coordinate = Extend_point_vertical(center_x, center_y, x, y, pts, reference)
     
          
       if next_coordinate[0] == previous_point[0] and next_coordinate[1] == previous_point[1]:
           next_coordinate = [x-1,y]
           remove_coordinate = [[x+1,y]]
           Extend_coordinate = Extend_point_vertical(center_x, center_y, x, y, pts, reference)
           #Extend_coordinate = guess_orienHOV(center_x, center_y, x, y)
          
        

    # straight left top
    if result == -14 and np.sum(Position_matrix) == 4: #-3
        next_coordinate = [x-1,y+1]
        remove_coordinate = [[x+1,y]]
        print (remove_coordinate)
        Extend_coordinate = Extend_point_horizontal(center_x, center_y, x, y, pts, reference)
        #Extend_coordinate = guess_orienHOV(center_x, center_y, x, y)
        
            
        
        if next_coordinate[0] == previous_point[0] and next_coordinate[1] == previous_point[1]:
            next_coordinate = [x,y-1]
            remove_coordinate = [[x+1,y]]
            print ("xxx")
            print (remove_coordinate)
            Extend_coordinate = Extend_point_horizontal(center_x, center_y, x, y, pts, reference)
            #Extend_coordinate = guess_orienHOV(center_x, center_y, x, y)
            
  

    if result == 5 and np.sum(Position_matrix) ==4:
        next_coordinate = [x+1,y+1]
        #Extend_coordinate = Extend_point_vertical(center_x, center_y, x, y)
        Extend_coordinate = guess_orienHOV(center_x, center_y, x, y, pts, reference)
       
            
        if next_coordinate[0] == previous_point[0] and next_coordinate[1] == previous_point[1]:
            next_coordinate = [x-1,y+1]
            #Extend_coordinate = Extend_point_vertical(center_x, center_y, x, y)
            Extend_coordinate = guess_orienHOV(center_x, center_y, x, y, pts, reference)
            
    #Changed to GuessHOV        
    if result == -25 and np.sum(Position_matrix) == 4: #-19
       next_coordinate = [x+1,y-1]
       #Extend_coordinate = Extend_point_vertical(center_x, center_y, x, y)
       Extend_coordinate = guess_orienHOV(center_x, center_y, x, y, pts, reference)
      
       if next_coordinate[0] == previous_point[0] and next_coordinate[1] == previous_point[1]:
           next_coordinate = [x-1,y]
           #Extend_coordinate = Extend_point_vertical(center_x, center_y, x, y)
           Extend_coordinate = guess_orienHOV(center_x, center_y, x, y, pts, reference)

           

    if result == -21 and np.sum(Position_matrix) == 4: #-19
       next_coordinate = [x,y+1]
       remove_coordinate =[[x-1,y]]
       #Extend_coordinate = Extend_point_vertical(center_x, center_y, x, y)
       Extend_coordinate = guess_orienHOV(center_x, center_y, x, y, pts, reference)
       
       if next_coordinate[0] == previous_point[0] and next_coordinate[1] == previous_point[1]:
           next_coordinate = [x+1,y-1]
           remove_coordinate =[[x-1,y]]
           #Extend_coordinate = Extend_point_vertical(center_x, center_y, x, y)
           Extend_coordinate = guess_orienHOV(center_x, center_y, x, y, pts, reference)
           


    if result == 18 and np.sum(Position_matrix) == 4: #-19
       next_coordinate = [x+1,y+1]
       remove_coordinate =[[x-1,y]]
       #Extend_coordinate = Extend_point_vertical(center_x, center_y, x, y)
       Extend_coordinate = guess_orienHOV(center_x, center_y, x, y, pts, reference)
       
       if next_coordinate[0] == previous_point[0] and next_coordinate[1] == previous_point[1]:
           next_coordinate = [x,y-1]
           remove_coordinate =[[x-1,y]]
           #Extend_coordinate = Extend_point_vertical(center_x, center_y, x, y)
           Extend_coordinate = guess_orienHOV(center_x, center_y, x, y, pts, reference)
          

    '''
    if remove_coordinate == None:
       remove_coordinate = [0,0]
    else:
       remove_coordinate = remove_coordinate_14
       print (remove_coordinate)

   '''
        
    
    #print (result)    
    #print (next_coordinate)
    #print (Extend_coordinate)
    #print (remove_coordinate)


               
    return next_coordinate, Extend_coordinate #, Next_coordinate_layer, remove_coordinate

















































































    


def Closer2First(center_x, center_y, Extend_first, Extend_last):
    R1 = ((Extend_first[0] - center_x)**2 + (Extend_first[1]-center_y)**2)**(1/2)
    #print ("R1")
    #print (R1)
    R2 = ((Extend_last[0] - center_x)**2 + (Extend_last[1]-center_y)**2)**(1/2)



    #R1 = ((Extend_first[0] - center_x)**2 / (Extend_first[1]-center_y)**2)
    #R2 = ((Extend_last[0] - center_x)**2 / (Extend_last[1]-center_y)**2)


    
    if R2 < R1: 
       return 0
    else:
       return 1



def find_correct_point(cy,cx, X1, X2, result, reference):
    x1 = X1[0]
    y1 = X1[1]
    
    x2 = X2[0]
    y2 = X2[1]

    if x1 > np.shape(reference)[0]-1 or y1 > np.shape(reference)[1]-1:
        return [[x2,y2]]
    else:
        if reference[x1][y1] == 1:
            return [[x1,y1]]
    

    if x2 > np.shape(reference)[0]-1 or y2 > np.shape(reference)[1]-1:
        return [[x1,y1]]
    else:
        if reference[x2][y2] == 1:
            return [[x2,y2]]









def find_correct_point_fast( X1, X2, reference):
     #X1 ...... X0 ..... X2

    # reference_image[X1[0]][X1[1]] = 0 

    if reference[X1[0]][X1[1]] == 0:
        return True
    

    else:
        return False






    
    


def Extend_point_horizontal(cx, cy, x, y, pts,reference):
    #Extend_coordinate = [[x-3,y],[x-2,y],[x-1,y],[x,y],[x+1,y],[x+2,y],[x+3,y]]
    Extend_coordinate = Extend_coordinate_Hor_NP(x,y,pts)
    
    #if Closer2First(cx, cy, Extend_coordinate[0], Extend_coordinate[len(Extend_coordinate)-1]) == 1:
    if find_correct_point_fast(Extend_coordinate[0], Extend_coordinate[-1], reference) ==True:
       return Extend_coordinate
    else:
       #Extend_coordinate = [[x+3,y],[x+2,y],[x+1,y],[x,y],[x-1,y],[x-2,y],[x-3,y]]
       Extend_coordinate = Extend_coordinate_Hor_PN(x,y, pts)
       return Extend_coordinate
    


def Extend_point_vertical(cx, cy, x, y, pts,reference):
    #Extend_coordinate = [[x,y-3],[x,y-2],[x,y-1],[x,y],[x,y+1],[x,y+2],[x,y+3]]
    Extend_coordinate = Extend_coordinate_Ver_NP(x,y, pts)
    
    #if Closer2First(cx, cy, Extend_coordinate[0], Extend_coordinate[len(Extend_coordinate)-1]) == 1:
    if find_correct_point_fast(Extend_coordinate[0], Extend_coordinate[-1], reference) ==True:
       return Extend_coordinate
    else:
       
       #Extend_coordinate = [[x,y+3],[x,y+2],[x,y+1],[x,y],[x,y-1],[x,y-2],[x,y-3]]
       Extend_coordinate = Extend_coordinate_Ver_PN(x,y, pts)
       
       return Extend_coordinate  
    
    

def Extend_point_45(cx, cy, x, y, pts,reference):
    #Extend_coordinate = [[x-3,y+3],[x-2,y+2],[x-1,y+1],[x,y],[x+1,y-1],[x+2,y-2],[x+3,y-3]]
    Extend_coordinate = Extend_coordinate_45_LR(x,y, pts)
   
    #if Closer2First(cx, cy, Extend_coordinate[0], Extend_coordinate[len(Extend_coordinate)-1]) == 1:
    if find_correct_point_fast(Extend_coordinate[0], Extend_coordinate[-1], reference) ==True:
       return Extend_coordinate
    else:
       #Extend_coordinate = [[x+3,y-3],[x+2,y-2],[x+1,y-1],[x,y],[x-1,y+1],[x-2,y+2],[x-3,y+3]]
       Extend_coordinate = Extend_coordinate_45_RL(x,y, pts)
       return Extend_coordinate  


def Extend_point_45_2(cx, cy, x, y, pts,reference):
    #Extend_coordinate = [[x-3,y+3],[x-2,y+2],[x-1,y+1],[x,y],[x+1,y-1],[x+2,y-2],[x+3,y-3]]
    Extend_coordinate = Extend_coordinate_45_2_LR(x,y, pts)
   
    #if Closer2First(cx, cy, Extend_coordinate[0], Extend_coordinate[len(Extend_coordinate)-1]) == 1:
    if find_correct_point_fast(Extend_coordinate[0], Extend_coordinate[-1], reference) ==True:
       return Extend_coordinate
    else:
       #Extend_coordinate = [[x+3,y-3],[x+2,y-2],[x+1,y-1],[x,y],[x-1,y+1],[x-2,y+2],[x-3,y+3]]
       Extend_coordinate = Extend_coordinate_45_2_LR(x,y, pts)
       return Extend_coordinate  


    
def guess_orien(cx, cy, x, y, pts,reference):
    E_0 = Extend_point_horizontal(cx, cy, x, y, pts,reference)
    E_90 = Extend_point_vertical(cx, cy, x, y, pts, reference)
    E_45 = Extend_point_45(cx, cy, x, y, pts,reference)
    E_45_2 = Extend_point_45_2(cx, cy, x, y, pts, reference)

    D_E_0 = ((E_0[0][0] - cx)**2 + (E_0[0][1]-cy)**2)**(1/2)
    D_E_90 = ((E_90[0][0] - cx)**2 + (E_90[0][1]-cy)**2)**(1/2)
    D_E_45 = ((E_45[0][0] - cx)**2 + (E_45[0][1]-cy)**2)**(1/2)
    D_E_45_2 = ((E_45_2[0][0] - cx)**2 + (E_45_2[0][1]-cy)**2)**(1/2)
    closest = min([D_E_0, D_E_90, D_E_45, D_E_45_2])

    if closest == D_E_0:
        return E_0
    if closest == D_E_90:
        return E_90
    if closest == D_E_45:
        return E_45
    if closest == E_R_45_2:
        return E_45_2

def guess_orienHOV(cx, cy, x, y, pts, reference):
    E_0 = Extend_point_horizontal(cx, cy, x, y, pts, reference)
    E_90 = Extend_point_vertical(cx, cy, x, y, pts, reference)
    

    D_E_0 = ((E_0[0][0] - cx)**2 + (E_0[0][1]-cy)**2)**(1/2)
    D_E_90 = ((E_90[0][0] - cx)**2 + (E_90[0][1]-cy)**2)**(1/2)
    closest = min([D_E_0, D_E_90])
    
    D_E_0_tan = ((E_0[0][0] - cx)**2 / (E_0[0][1]-cy)**2)
    D_E_90_tan = ((E_90[0][0] - cx)**2 / (E_90[0][1]-cy)**2)
    closest_tan = max([D_E_0_tan, D_E_90_tan])
    
    # if using the later ones to calculate the distance (tangent) use max in the line below


    if closest == D_E_0 and closest_tan == D_E_0_tan:
       return E_0
    else:
       return E_90
    if closest == D_E_90 and closest_tan == D_E_90_tan:
       return E_90
    else:
        return E_0
    
       

    
    '''
    if closest == D_E_0:
        return E_0
    if closest == D_E_90:
        return E_90
    '''

def Extend_coordinate_Hor_PN(x,y,Length):
    Extend_coordinate = [];
    for i in range(Length,-Length-1,-1):
        Extend_coordinate.append([x+i,y])
    
    return Extend_coordinate

def Extend_coordinate_Hor_NP(x,y,Length):
    Extend_coordinate = [];
    for i in range(-Length,Length+1):
        Extend_coordinate.append([x+i,y])
    
    return Extend_coordinate



def Extend_coordinate_Ver_PN(x,y,Length):
    Extend_coordinate = [];
    for i in range(Length,-Length-1, -1):
        Extend_coordinate.append([x,y+i])
    return Extend_coordinate

def Extend_coordinate_Ver_NP(x,y,Length):
    Extend_coordinate = [];
    for i in range(-Length,Length+1):
        Extend_coordinate.append([x,y+i])
    return Extend_coordinate



def Extend_coordinate_45_LR(x,y,Length):
    #[[x-3,y+3],[x-2,y+2],[x-1,y+1],[x,y],[x+1,y-1],[x+2,y-2],[x+3,y-3]]
    Extended_coordinate = []
    for i in range(-Length,Length+1):
        Extend_coordinate.append([x+i,y-i])
    
    return Extend_coordinate

def Extend_coordinate_45_RL(x,y,Length):
    #[[x+3,y-3],[x+2,y-2],[x+1,y-1],[x,y],[x-1,y+1],[x-2,y+2],[x-3,y+3]]
    Extended_coordinate = []
    for i in range(-Length,Length+1):
        Extend_coordinate.append([x-i,y+i])
    
    return Extend_coordinate



def Extend_coordinate_45_2_LR(x,y,Length):
    #[[x-3,y+3],[x-2,y+2],[x-1,y+1],[x,y],[x+1,y-1],[x+2,y-2],[x+3,y-3]]
    Extended_coordinate = []
    for i in range(-Length,Length+1):
        Extend_coordinate.append([x+i,y-i])
    
    return Extend_coordinate
    


def Extend_coordinate_45_2_RL(x,y,Length):
    #[[x+3,y-3],[x+2,y-2],[x+1,y-1],[x,y],[x-1,y+1],[x-2,y+2],[x-3,y+3]]
    Extended_coordinate = []
    for i in range(-Length,Length+1):
        Extend_coordinate.append([x-i,y+i])
    
    return Extend_coordinate
    







    


def sum_mat(image, x,y):
    I = image
    
    sum_i = I[x-1][y+1] + I[x][y+1] + I[x+1][y+1] + I[x-1][y]+   I[x][y]+   I[x+1][y] + I[x-1][y-1]+ I[x][y-1]+ I[x+1][y-1]
    return sum_i


def check_line_connectivity(image, coordinate):
    image_matrix = get_image_matrix(image,coordinate[0],coordinate[1])
    Kernel_matrix = kernel_matrix()
    result = Operate_matrix(image_matrix, Kernel_matrix)
    x = coordinate[0]
    y = coordinate[1]
    #print (result)

    if sum_mat(image,coordinate[0],coordinate[1]) >3:
        
       #print (image_matrix)
       #print (coordinate[0],coordinate[1])
       print ("Danger")
       #plt.matshow(image)
       #plt.show
       
    

    if result == 11 or result == -21 or result == 24 or result == -26 or result == 2 or result == 22 or result == 13 or result == -17 or result == 10 or result == -25 or result == -22 or result == -7 or result == 9 or result == -11 or result == 4 or result == -6:
       return None
    
    if result == 3 or result == -3 or result == -15 or result == -9:
      
       return [x,y] 
        
    
    # center top, topright
    if result == 16:
       return [x,y+1]

    # center right, bottomright
    if result == -37:
       return [x+1,y]

    # center bottom, bottomleft
    if result == 17:
       return [x-1,y]

    # center left, topleft
    if result == -10:
       return [x-1,y]

    # center top, topright
    if result == -4:
       return [x,y+1]

    # center left, bottomleft
    if result == 5:
       return [x-1,y]

    #center bottom, bottomright
    if result == -13:
       return [x,y-1]

    #center right, topright
    if result == -2:
       return [x+1,y]




def diagonal_left():
    DL_matrix = [[1, 0, 0],
                 [0, 1, 0],
                 [0, 0, 1]]
    return DL_matrix

def diagonal_right():
    DR_matrix = [[0, 0, 1],
                 [0, 1, 0],
                 [1, 0, 0]]
    return DR_matrix
    


def check_four_point(image, coordinate):
    image_matrix = get_image_matrix(image,coordinate[0],coordinate[1])
    #image_matrix = list(np.divide(image_matrix,image_matrix))
    x = coordinate[0]
    y = coordinate[1]
    Kernel_matrix = kernel_matrix()
    
    result = Operate_matrix(image_matrix, Kernel_matrix)
    DR = diagonal_right()
    DL = diagonal_left()
    result_dia_R = Operate_matrix(image_matrix,DR)
    print("Dia")
    print (image_matrix)
    print (result_dia_R)
    result_dia_L = Operate_matrix(image_matrix,DL)
    print (result_dia_L)
    
    
    
    if result_dia_R == 3:
       print ("diagonal")
       return [[x+1,y],[x-1,y], [x,y+1],[x,y-1], [x-1,y+1],[x+1,y-1]]

    if result_dia_L == 3:
       print ("diagonal")
       return [[x+1,y],[x-1,y], [x,y+1],[x,y-1], [x+1,y+1],[x-1,y-1]]
    
    if Operate_matrix(image_matrix, Kernel_matrix) == -25:
        print ("yoyo")
        return [x,y-1]

    if Operate_matrix(image_matrix, Kernel_matrix) == 22:
        return [x+1,y]

    if Operate_matrix(image_matrix, Kernel_matrix) == -22:
        return [x,y+1]

    if Operate_matrix(image_matrix, Kernel_matrix) == 7:
        return [x-1,y]
    
    

def find_right_order(previous_point, Next_coordinate_layer_1, Next_coordinate_layer_2):
    P1 = ((Next_coordinate_layer_1[0][0] - previous_point[0])**2 + (Next_coordinate_layer_1[0][1]-previous_point[1])**2)**(1/2)
    P2 = ((Next_coordinate_layer_2[0][0] - previous_point[0])**2 + (Next_coordinate_layer_2[0][1]-previous_point[1])**2)**(1/2)
    closest = min([P1, P2])
    if closest == P1:
        return [[Next_coordinate_layer_1[0][0],Next_coordinate_layer_1[0][1]],[Next_coordinate_layer_2[0][0],Next_coordinate_layer_2[0][1]]]
    if closest == P2:
        return [[Next_coordinate_layer_2[0][0],Next_coordinate_layer_2[0][1]],[Next_coordinate_layer_1[0][0],Next_coordinate_layer_1[0][1]]]
    















###################################### unwrap open ends #################################################################





def Next_coordinate_open_ends(result,x,y,previous_point, center_x, center_y, Position_matrix, reference, pts):
    
    #remove_coordinate = remove_data
    # vertical 
    if result == 11: #3
       next_coordinate = [x,y+1]
       #extend point from the current position
       Extend_coordinate = Extend_point_horizontal_OE(center_x, center_y, x, y, pts, reference)
      
        
        
       if next_coordinate[0] == previous_point[0] and next_coordinate[1] == previous_point[1]:
           
          next_coordinate = [x,y-1]
          Extend_coordinate = Extend_point_horizontal_OE(center_x, center_y, x, y, pts, reference)
          
                                                                              
        
    
             
    # horizontal
    if result == -21: #5
        next_coordinate = [x+1,y]
        Extend_coordinate = Extend_point_vertical_OE(center_x, center_y, x, y, pts, reference)
       

        
        if next_coordinate[0] == previous_point[0] and next_coordinate[1] == previous_point[1]:
            next_coordinate = [x-1,y]
            Extend_coordinate = Extend_point_vertical_OE(center_x, center_y, x, y, pts, reference)
            

    # diagonal left
    if result == 24: #unchanged
        next_coordinate = [x+1,y+1]
        Extend_coordinate = guess_orienHOV_OE(center_x, center_y, x, y, pts, reference)
        
                  
        
        if next_coordinate[0] == previous_point[0] and next_coordinate[1] == previous_point[1]:
            next_coordinate = [x-1,y-1]
            Extend_coordinate = guess_orienHOV_OE(center_x, center_y, x, y, pts, reference)
            
            
    #diagonal right
    if result == -26: #unchanged
        next_coordinate = [x-1,y+1]
        Extend_coordinate = guess_orienHOV_OE(center_x, center_y, x, y, pts, reference)
       
        
        if next_coordinate[0] == previous_point[0] and next_coordinate[1] == previous_point[1]:
            next_coordinate = [x+1,y-1]
            Extend_coordinate = guess_orienHOV_OE(center_x, center_y, x, y, pts, reference)
            
    
    # straight left top
    if result == 2: #-3
        next_coordinate = [x-1,y+1]
        Extend_coordinate = Extend_point_horizontal_OE(center_x, center_y, x, y, pts, reference)
       
            
        
        if next_coordinate[0] == previous_point[0] and next_coordinate[1] == previous_point[1]:
            next_coordinate = [x,y-1]
            Extend_coordinate = Extend_point_horizontal_OE(center_x, center_y, x, y, pts, reference)

           
    # straight right top
    if result == 22:#17
        next_coordinate = [x+1,y+1]
        Extend_coordinate = Extend_point_horizontal_OE(center_x, center_y, x, y, pts, reference)
       
        
        if next_coordinate[0] == previous_point[0] and next_coordinate[1] == previous_point[1]:
            next_coordinate = [x,y-1]
            Extend_coordinate = Extend_point_horizontal_OE(center_x, center_y, x, y, pts, reference)
            
    # straight bottom right
    if result == -17:#-20
        next_coordinate = [x,y+1]
        Extend_coordinate = Extend_point_horizontal_OE(center_x, center_y, x, y, pts, reference)
                
        if next_coordinate[0] == previous_point[0] and next_coordinate[1] == previous_point[1]:
            next_coordinate = [x+1,y-1]
            Extend_coordinate = Extend_point_horizontal_OE(center_x, center_y, x, y, pts, reference)
           

    # straight bottom left
    if result == 13: #10
        next_coordinate = [x,y+1]
        Extend_coordinate = Extend_point_horizontal_OE(center_x, center_y, x, y, pts, reference)
           
        if next_coordinate[0] == previous_point[0] and next_coordinate[1] == previous_point[1]:
            next_coordinate = [x-1,y-1]
            Extend_coordinate = Extend_point_horizontal_OE(center_x, center_y, x, y, pts, reference)
        
           
            

    # horizontal top right
    if result == 10: #16
        next_coordinate = [x+1,y+1]
        Extend_coordinate = Extend_point_vertical_OE(center_x, center_y, x, y, pts, reference)

            
        if next_coordinate[0] == previous_point[0] and next_coordinate[1] == previous_point[1]:
            next_coordinate = [x-1,y]
            Extend_coordinate = Extend_point_vertical_OE(center_x, center_y, x, y, pts, reference)
        


    # horizontal bottom right
    if result == -25 and np.sum(Position_matrix) == 3: #-19
        next_coordinate = [x+1,y-1]
        Extend_coordinate = Extend_point_vertical_OE(center_x, center_y, x, y, pts, reference)
        
        if next_coordinate[0] == previous_point[0] and next_coordinate[1] == previous_point[1]:
            next_coordinate = [x-1,y]
            Extend_coordinate = Extend_point_vertical_OE(center_x, center_y, x, y, pts, reference)
            
        


    # horizontal top left
    if result == -22 and np.sum(Position_matrix) == 3: #-2
        next_coordinate = [x+1,y]
        Extend_coordinate = Extend_point_vertical_OE(center_x, center_y, x, y, pts, reference)
       
           
        if next_coordinate[0] == previous_point[0] and next_coordinate[1] == previous_point[1]:
            next_coordinate = [x-1,y+1]
            Extend_coordinate = Extend_point_vertical_OE(center_x, center_y, x, y, pts, reference)
        

    # horizontal bottom left
    if result == -7:#13
        next_coordinate = [x+1,y]
        Extend_coordinate = Extend_point_vertical_OE(center_x, center_y, x, y, pts, reference)
       
        if next_coordinate[0] == previous_point[0] and next_coordinate[1] == previous_point[1]:
            next_coordinate = [x-1,y-1]
            Extend_coordinate = Extend_point_vertical_OE(center_x, center_y, x, y, pts, reference)
            

    # arrow shape right
    if result == 4 and np.sum(Position_matrix) == 3:
        next_coordinate = [x-1,y+1]
        #Extend_coordinate = Extend_point_horizontal(center_x, center_y, x, y)
        Extend_coordinate = guess_orienHOV_OE(center_x, center_y, x, y, pts, reference)
        
        if next_coordinate[0] == previous_point[0] and next_coordinate[1] == previous_point[1]:
            next_coordinate = [x-1,y-1]
            #Extend_coordinate = Extend_point_horizontal(center_x, center_y, x, y)
            Extend_coordinate = guess_orienHOV_OE(center_x, center_y, x, y, pts, reference)
           

    # arrow shape left
    if result == -6:
        next_coordinate = [x+1,y+1]
        #Extend_coordinate = Extend_point_horizontal(center_x, center_y, x, y)
        Extend_coordinate = guess_orienHOV_OE(center_x, center_y, x, y, pts, reference)
       
        if next_coordinate[0] == previous_point[0] and next_coordinate[1] == previous_point[1]:
            next_coordinate = [x+1,y-1]
            #Extend_coordinate = Extend_point_horizontal(center_x, center_y, x, y)
            Extend_coordinate = guess_orienHOV_OE(center_x, center_y, x, y, pts, reference)
            

    # arrow shape down
    if result == 9:
        next_coordinate = [x+1,y+1]
        #Extend_coordinate = Extend_point_vertical(center_x, center_y, x, y)
        Extend_coordinate = guess_orienHOV_OE(center_x, center_y, x, y, pts, reference)
        
        if next_coordinate[0] == previous_point[0] and next_coordinate[1] == previous_point[1]:
            next_coordinate = [x-1,y+1]
            #Extend_coordinate = Extend_point_vertical(center_x, center_y, x, y)
            Extend_coordinate = guess_orienHOV_OE(center_x, center_y, x, y, pts, reference)
             
        

    # arrow shape up
    if result == -11:
        next_coordinate = [x+1,y-1]
        #Extend_coordinate = Extend_point_vertical(center_x, center_y, x, y)
        Extend_coordinate = guess_orienHOV_OE(center_x, center_y, x, y, pts, reference)
            
        if next_coordinate[0] == previous_point[0] and next_coordinate[1] == previous_point[1]:
            next_coordinate = [x-1,y-1]
            #Extend_coordinate = Extend_point_vertical(center_x, center_y, x, y)
            Extend_coordinate = guess_orienHOV_OE(center_x, center_y, x, y, pts, reference)
            


    # 4 point
    
    if result == 32 and np.sum(Position_matrix) == 4:
        next_coordinate = [x+1,y+1]
        
        Extend_coordinate = guess_orienHOV_OE(center_x, center_y, x, y, pts, reference)
      
        
        if next_coordinate[0] == previous_point[0] and next_coordinate[1] == previous_point[1]:
            next_coordinate = [x-1,y-1]
            Extend_coordinate = guess_orienHOV_OE(center_x, center_y, x, y, pts, reference)
            
    
    if result == 8 and np.sum(Position_matrix) == 4:
        next_coordinate = [x+1,y+1]
        Extend_coordinate = guess_orienHOV_OE(center_x, center_y, x, y, pts, reference)
       
        
        if next_coordinate[0] == previous_point[0] and next_coordinate[1] == previous_point[1]:
            next_coordinate = [x-1,y-1]
            Extend_coordinate = guess_orienHOV_OE(center_x, center_y, x, y, pts, reference)
           
      
    if result == 28 and np.sum(Position_matrix) == 4: #unchanged
        next_coordinate = [x+1,y+1]
        Extend_coordinate = guess_orienHOV_OE(center_x, center_y, x, y, pts, reference)
         
        
        if next_coordinate[0] == previous_point[0] and next_coordinate[1] == previous_point[1]:
            next_coordinate = [x-1,y-1]
            Extend_coordinate = guess_orienHOV_OE(center_x, center_y, x, y, pts, reference)
            
    
    if result == 20 and np.sum(Position_matrix) == 4: #unchanged
        next_coordinate = [x+1,y+1]
        Extend_coordinate = guess_orienHOV_OE(center_x, center_y, x, y, pts, reference)
         
        
        if next_coordinate[0] == previous_point[0] and next_coordinate[1] == previous_point[1]:
            next_coordinate = [x-1,y-1]
            Extend_coordinate = guess_orienHOV_OE(center_x, center_y, x, y, pts, reference)
            
    if result == -30 and np.sum(Position_matrix) == 4: #unchanged
        next_coordinate = [x-1,y+1]
        Extend_coordinate = guess_orienHOV_OE(center_x, center_y, x, y, pts, reference)
        
        
        if next_coordinate[0] == previous_point[0] and next_coordinate[1] == previous_point[1]:
            next_coordinate = [x+1,y-1]
            Extend_coordinate = guess_orienHOV_OE(center_x, center_y, x, y, pts, reference)
           
    

    if result == -18 and np.sum(Position_matrix) ==4 : #unchanged
        next_coordinate = [x-1,y+1]
        Extend_coordinate = guess_orienHOV_OE(center_x, center_y, x, y, pts, reference)
        
        
        if next_coordinate[0] == previous_point[0] and next_coordinate[1] == previous_point[1]:
            next_coordinate = [x+1,y-1]
            Extend_coordinate = guess_orienHOV_OE(center_x, center_y, x, y, pts, reference)
            
    if result == -42 and np.sum(Position_matrix) == 4: #unchanged
        next_coordinate = [x-1,y+1]
        Extend_coordinate = guess_orienHOV_OE(center_x, center_y, x, y, pts, reference)
        
        
        if next_coordinate[0] == previous_point[0] and next_coordinate[1] == previous_point[1]:
            next_coordinate = [x+1,y-1]
            Extend_coordinate = guess_orienHOV_OE(center_x, center_y, x, y, pts, reference)
            
    if result == -22 and np.sum(Position_matrix) == 4: #unchanged
        next_coordinate = [x-1,y+1]
        Extend_coordinate = guess_orienHOV_OE(center_x, center_y, x, y, pts, reference)
        
        
        if next_coordinate[0] == previous_point[0] and next_coordinate[1] == previous_point[1]:
            next_coordinate = [x+1,y-1]
            Extend_coordinate = guess_orienHOV_OE(center_x, center_y, x, y, pts, reference)
        

    
    if result == 26 and np.sum(Position_matrix) ==4:#17
        next_coordinate = [x+1,y+1]
        remove_coordinate = [[x,y+1]]
        Extend_coordinate = Extend_point_horizontal_OE(center_x, center_y, x, y, pts, reference)
        
        
        if next_coordinate[0] == previous_point[0] and next_coordinate[1] == previous_point[1]:
            next_coordinate = [x,y-1]
            remove_coordinate = [[x,y+1]]
            Extend_coordinate = Extend_point_horizontal_OE(center_x, center_y, x, y, pts, reference)
            
        
    if result == 6 and np.sum(Position_matrix) ==4: #-3
       next_coordinate = [x-1,y+1]
       remove_coordinate = [[x,y+1]]
       #Extend_coordinate = Extend_point_horizontal(center_x, center_y, x, y)
       Extend_coordinate = guess_orienHOV_OE(center_x, center_y, x, y, pts, reference)
      
            
        
       if next_coordinate[0] == previous_point[0] and next_coordinate[1] == previous_point[1]:
           next_coordinate = [x,y-1]
           remove_coordinate = [[x,y+1]]
           Extend_coordinate = Extend_point_horizontal_OE(center_x, center_y, x, y, pts, reference)
          
        
    if result == 21 and np.sum(Position_matrix) == 4: #10
        next_coordinate = [x,y+1]
        remove_coordinate = [[x,y-1]]
        #Extend_coordinate = Extend_point_horizontal(center_x, center_y, x, y)
        Extend_coordinate = guess_orienHOV_OE(center_x, center_y, x, y, pts, reference)
        

        if next_coordinate[0] == previous_point[0] and next_coordinate[1] == previous_point[1]:
            next_coordinate = [x-1,y-1]
            remove_coordinate = [[x,y-1]]
            #Extend_coordinate = Extend_point_horizontal(center_x, center_y, x, y)
            Extend_coordinate = guess_orienHOV_OE(center_x, center_y, x, y, pts, reference)
        
    if result == -9 and np.sum(Position_matrix) == 4:#-20
        next_coordinate = [x,y+1]
        remove_coordinate = [[x,y-1]]
        Extend_coordinate = Extend_point_horizontal_OE(center_x, center_y, x, y, pts, reference)
        
        if next_coordinate[0] == previous_point[0] and next_coordinate[1] == previous_point[1]:
            next_coordinate = [x+1,y-1]
            remove_coordinate = [[x,y-1]]
            Extend_coordinate = Extend_point_horizontal_OE(center_x, center_y, x, y, pts, reference)
        







    if result == -6 and np.sum(Position_matrix) ==4: #16
        next_coordinate = [x+1,y+1]
        remove_coordinate = [[x+1,y]]
        Extend_coordinate = Extend_point_vertical_OE(center_x, center_y, x, y, pts, reference)
            
        if next_coordinate[0] == previous_point[0] and next_coordinate[1] == previous_point[1]:
            next_coordinate = [x-1,y]
            remove_coordinate = [[x+1,y]]
            Extend_coordinate = Extend_point_vertical_OE(center_x, center_y, x, y, pts, reference)
        


    



     # horizontal top left
    if result == -26 and np.sum(Position_matrix) == 4: #-2
        next_coordinate = [x+1,y]
        remove_coordinate = [[x-1,y]]
        Extend_coordinate = Extend_point_vertical_OE(center_x, center_y, x, y, pts, reference)
        #Extend_coordinate = guess_orienHOV(center_x, center_y, x, y)
        
        if next_coordinate[0] == previous_point[0] and next_coordinate[1] == previous_point[1]:
            next_coordinate = [x-1,y+1]
            remove_coordinate = [[x-1,y]]
            Extend_coordinate = Extend_point_vertical_OE(center_x, center_y, x, y, pts, reference)
            

    if result == -11 and np.sum(Position_matrix) == 4:#13
        next_coordinate = [x+1,y]
        remove_coordinate = [[x-1,y]]
        Extend_coordinate = Extend_point_vertical_OE(center_x, center_y, x, y, pts, reference)
        
        if next_coordinate[0] == previous_point[0] and next_coordinate[1] == previous_point[1]:
            next_coordinate = [x-1,y-1]
            remove_coordinate = [[x-1,y]]
            Extend_coordinate = Extend_point_vertical_OE(center_x, center_y, x, y, pts, reference)
            
        
  


    if result == -41 and np.sum(Position_matrix) == 4: #-19
       next_coordinate = [x+1,y-1]
       remove_coordinate = [[x+1,y]]
       Extend_coordinate = Extend_point_vertical_OE(center_x, center_y, x, y, pts, reference)
     
          
       if next_coordinate[0] == previous_point[0] and next_coordinate[1] == previous_point[1]:
           next_coordinate = [x-1,y]
           remove_coordinate = [[x+1,y]]
           Extend_coordinate = Extend_point_vertical_OE(center_x, center_y, x, y, pts, reference)
           #Extend_coordinate = guess_orienHOV(center_x, center_y, x, y)
          
        

    # straight left top
    if result == -14 and np.sum(Position_matrix) == 4: #-3
        next_coordinate = [x-1,y+1]
        remove_coordinate = [[x+1,y]]
        print (remove_coordinate)
        Extend_coordinate = Extend_point_horizontal_OE(center_x, center_y, x, y, pts, reference)
        #Extend_coordinate = guess_orienHOV(center_x, center_y, x, y)
        
            
        
        if next_coordinate[0] == previous_point[0] and next_coordinate[1] == previous_point[1]:
            next_coordinate = [x,y-1]
            remove_coordinate = [[x+1,y]]
            print ("xxx")
            print (remove_coordinate)
            Extend_coordinate = Extend_point_horizontal_OE(center_x, center_y, x, y, pts, reference)
            #Extend_coordinate = guess_orienHOV(center_x, center_y, x, y)
            
  

    if result == 5 and np.sum(Position_matrix) ==4:
        next_coordinate = [x+1,y+1]
        #Extend_coordinate = Extend_point_vertical(center_x, center_y, x, y)
        Extend_coordinate = guess_orienHOV_OE(center_x, center_y, x, y, pts, reference)
       
            
        if next_coordinate[0] == previous_point[0] and next_coordinate[1] == previous_point[1]:
            next_coordinate = [x-1,y+1]
            #Extend_coordinate = Extend_point_vertical(center_x, center_y, x, y)
            Extend_coordinate = guess_orienHOV_OE(center_x, center_y, x, y, pts, reference)
            
    #Changed to GuessHOV        
    if result == -25 and np.sum(Position_matrix) == 4: #-19
       next_coordinate = [x+1,y-1]
       #Extend_coordinate = Extend_point_vertical(center_x, center_y, x, y)
       Extend_coordinate = guess_orienHOV_OE(center_x, center_y, x, y, pts, reference)
      
       if next_coordinate[0] == previous_point[0] and next_coordinate[1] == previous_point[1]:
           next_coordinate = [x-1,y]
           #Extend_coordinate = Extend_point_vertical(center_x, center_y, x, y)
           Extend_coordinate = guess_orienHOV_OE(center_x, center_y, x, y, pts, reference)

           

    if result == -21 and np.sum(Position_matrix) == 4: #-19
       next_coordinate = [x,y+1]
       remove_coordinate =[[x-1,y]]
       #Extend_coordinate = Extend_point_vertical(center_x, center_y, x, y)
       Extend_coordinate = guess_orienHOV_OE(center_x, center_y, x, y, pts, reference)
       
       if next_coordinate[0] == previous_point[0] and next_coordinate[1] == previous_point[1]:
           next_coordinate = [x+1,y-1]
           remove_coordinate =[[x-1,y]]
           #Extend_coordinate = Extend_point_vertical(center_x, center_y, x, y)
           Extend_coordinate = guess_orienHOV_OE(center_x, center_y, x, y, pts, reference)
           


    if result == 18 and np.sum(Position_matrix) == 4: #-19
       next_coordinate = [x+1,y+1]
       remove_coordinate =[[x-1,y]]
       #Extend_coordinate = Extend_point_vertical(center_x, center_y, x, y)
       Extend_coordinate = guess_orienHOV_OE(center_x, center_y, x, y, pts, reference)
       
       if next_coordinate[0] == previous_point[0] and next_coordinate[1] == previous_point[1]:
           next_coordinate = [x,y-1]
           remove_coordinate =[[x-1,y]]
           #Extend_coordinate = Extend_point_vertical(center_x, center_y, x, y)
           Extend_coordinate = guess_orienHOV_OE(center_x, center_y, x, y, pts, reference)
          

    '''
    if remove_coordinate == None:
       remove_coordinate = [0,0]
    else:
       remove_coordinate = remove_coordinate_14
       print (remove_coordinate)

   '''
        
    
    #print (result)    
    #print (next_coordinate)
    #print (Extend_coordinate)
    #print (remove_coordinate)


               
    return next_coordinate, Extend_coordinate #, Next_coordinate_layer, remove_coordinate







def Closer2First(center_x, center_y, Extend_first, Extend_last):
    R1 = ((Extend_first[0] - center_x)**2 + (Extend_first[1]-center_y)**2)**(1/2)
    #print ("R1")
    #print (R1)
    R2 = ((Extend_last[0] - center_x)**2 + (Extend_last[1]-center_y)**2)**(1/2)



    #R1 = ((Extend_first[0] - center_x)**2 / (Extend_first[1]-center_y)**2)
    #R2 = ((Extend_last[0] - center_x)**2 / (Extend_last[1]-center_y)**2)


    
    if R2 < R1: 
       return 0
    else:
       return 1







    
    


def Extend_point_horizontal_OE(cx, cy, x, y, pts,reference):
    #Extend_coordinate = [[x-3,y],[x-2,y],[x-1,y],[x,y],[x+1,y],[x+2,y],[x+3,y]]
    Extend_coordinate = Extend_coordinate_Hor_NP(x,y,pts)
    
    if Closer2First(cx, cy, Extend_coordinate[0], Extend_coordinate[len(Extend_coordinate)-1]) == 1:
    #if find_correct_point_fast(Extend_coordinate[0], Extend_coordinate[-1], reference) ==True:
       return Extend_coordinate
    else:
       #Extend_coordinate = [[x+3,y],[x+2,y],[x+1,y],[x,y],[x-1,y],[x-2,y],[x-3,y]]
       Extend_coordinate = Extend_coordinate_Hor_PN(x,y, pts)
       return Extend_coordinate
    


def Extend_point_vertical_OE(cx, cy, x, y, pts,reference):
    #Extend_coordinate = [[x,y-3],[x,y-2],[x,y-1],[x,y],[x,y+1],[x,y+2],[x,y+3]]
    Extend_coordinate = Extend_coordinate_Ver_NP(x,y, pts)
    
    if Closer2First(cx, cy, Extend_coordinate[0], Extend_coordinate[len(Extend_coordinate)-1]) == 1:
    #if find_correct_point_fast(Extend_coordinate[0], Extend_coordinate[-1], reference) ==True:
       return Extend_coordinate
    else:
       
       #Extend_coordinate = [[x,y+3],[x,y+2],[x,y+1],[x,y],[x,y-1],[x,y-2],[x,y-3]]
       Extend_coordinate = Extend_coordinate_Ver_PN(x,y, pts)
       
       return Extend_coordinate  
    
    

def Extend_point_45_OE(cx, cy, x, y, pts,reference):
    #Extend_coordinate = [[x-3,y+3],[x-2,y+2],[x-1,y+1],[x,y],[x+1,y-1],[x+2,y-2],[x+3,y-3]]
    Extend_coordinate = Extend_coordinate_45_LR(x,y, pts)
   
    if Closer2First(cx, cy, Extend_coordinate[0], Extend_coordinate[len(Extend_coordinate)-1]) == 1:
    #if find_correct_point_fast(Extend_coordinate[0], Extend_coordinate[-1], reference) ==True:
       return Extend_coordinate
    else:
       #Extend_coordinate = [[x+3,y-3],[x+2,y-2],[x+1,y-1],[x,y],[x-1,y+1],[x-2,y+2],[x-3,y+3]]
       Extend_coordinate = Extend_coordinate_45_RL(x,y, pts)
       return Extend_coordinate  


def Extend_point_45_2_OE(cx, cy, x, y, pts,reference):
    #Extend_coordinate = [[x-3,y+3],[x-2,y+2],[x-1,y+1],[x,y],[x+1,y-1],[x+2,y-2],[x+3,y-3]]
    Extend_coordinate = Extend_coordinate_45_2_LR(x,y, pts)
   
    if Closer2First(cx, cy, Extend_coordinate[0], Extend_coordinate[len(Extend_coordinate)-1]) == 1:
    #if find_correct_point_fast(Extend_coordinate[0], Extend_coordinate[-1], reference) ==True:
       return Extend_coordinate
    else:
       #Extend_coordinate = [[x+3,y-3],[x+2,y-2],[x+1,y-1],[x,y],[x-1,y+1],[x-2,y+2],[x-3,y+3]]
       Extend_coordinate = Extend_coordinate_45_2_LR(x,y, pts)
       return Extend_coordinate  


    
def guess_orien_OE(cx, cy, x, y, pts,reference):
    E_0 = Extend_point_horizontal_OE(cx, cy, x, y, pts,reference)
    E_90 = Extend_point_vertical_OE(cx, cy, x, y, pts, reference)
    E_45 = Extend_point_45_OE(cx, cy, x, y, pts,reference)
    E_45_2 = Extend_point_45_2_OE(cx, cy, x, y, pts, reference)

    D_E_0 = ((E_0[0][0] - cx)**2 + (E_0[0][1]-cy)**2)**(1/2)
    D_E_90 = ((E_90[0][0] - cx)**2 + (E_90[0][1]-cy)**2)**(1/2)
    D_E_45 = ((E_45[0][0] - cx)**2 + (E_45[0][1]-cy)**2)**(1/2)
    D_E_45_2 = ((E_45_2[0][0] - cx)**2 + (E_45_2[0][1]-cy)**2)**(1/2)
    closest = min([D_E_0, D_E_90, D_E_45, D_E_45_2])

    if closest == D_E_0:
        return E_0
    if closest == D_E_90:
        return E_90
    if closest == D_E_45:
        return E_45
    if closest == E_R_45_2:
        return E_45_2

def guess_orienHOV_OE(cx, cy, x, y, pts, reference):
    E_0 = Extend_point_horizontal_OE(cx, cy, x, y, pts, reference)
    E_90 = Extend_point_vertical_OE(cx, cy, x, y, pts, reference)
    

    D_E_0 = ((E_0[0][0] - cx)**2 + (E_0[0][1]-cy)**2)**(1/2)
    D_E_90 = ((E_90[0][0] - cx)**2 + (E_90[0][1]-cy)**2)**(1/2)
    closest = min([D_E_0, D_E_90])
    
    D_E_0_tan = ((E_0[0][0] - cx)**2 / (E_0[0][1]-cy)**2)
    D_E_90_tan = ((E_90[0][0] - cx)**2 / (E_90[0][1]-cy)**2)
    closest_tan = max([D_E_0_tan, D_E_90_tan])
    
    # if using the later ones to calculate the distance (tangent) use max in the line below


    if closest == D_E_0 and closest_tan == D_E_0_tan:
       return E_0
    else:
       return E_90
    if closest == D_E_90 and closest_tan == D_E_90_tan:
       return E_90
    else:
        return E_0
    
       

    
    '''
    if closest == D_E_0:
        return E_0
    if closest == D_E_90:
        return E_90
    '''


def determine_second(shape_image,first_position, x, y):
    identify_matrix = [[1,2,3],[4,0,5],[6,7,8]]
    val = np.sum(np.multiply(first_position, identify_matrix))     

    if val ==1:
        x = x-1
        y = y+1

    if val ==2:
        x=x
        y=y+1

    if val ==3:
        x=x+1
        y=y+1

    if val ==4:
        x=x-1
        y=y

    if val ==5:
        x=x+1
        y=y

    if val ==6:
        x=x-1
        y=y-1

    if val ==7:
        x=x
        y=y-1

    if val==8:
        x=x+1
        y=y+1

    return x,y














