import numpy as np





#Kernel_matrix =[ [5, 2, 15],
#                 [-4, 1,-13],
#                 [10, 8, -20]   ]

Kernel_matrix =[ [-5, 4, 15],
                 [-4, -1,-16],
                 [10, 8, -20]   ]



Matrix_list = [ [ [0, 1, 0],
                  [0, 1, 0],           #11
                  [0, 1, 0] ],
                
                 [ [0, 0, 0],
                   [1, 1, 1],          # -21
                   [0, 0, 0] ],

                 [ [0, 0, 1],
                   [0, 1, 0],          # 24
                   [1, 0, 0] ],

                 [ [1, 0, 0],
                   [0, 1, 0],          #-26
                   [0, 0, 1] ],


                 [ [1, 0, 0],
                   [0, 1, 0],          #2
                   [0, 1, 0] ],
 
                 [ [0, 0, 1],
                   [0, 1, 0],          #22
                   [0, 1, 0] ],


                 [ [0, 1, 0],
                   [0, 1, 0],           #13
                   [1, 0, 0] ],


                 [ [0, 1, 0],
                   [0, 1, 0],           #-17
                   [0, 0, 1] ],


                ]






def check_corners(Position_matrix,x,y):
    #print (Position_matrix)
    S=0
    Diagonal_check =[ [[1, 0, 0],
                       [0, 0, 0],           #-25
                       [0, 0, 1] ],
                
                 [ [0, 0, 1],
                   [0, 0, 0],          # 25
                   [1, 0, 0] ],

                 [ [1, 0, 1],
                   [0, 0, 0],          # 10
                   [0, 0, 0] ],

                 [ [0, 0, 0],
                   [0, 0, 0],          #-10
                   [1, 0, 1] ],


                 [ [1, 0, 0],
                   [0, 0, 0],          #5
                   [1, 0, 0] ],
 
                 [ [0, 0, 1],
                   [0, 0, 0],          #-5
                   [0, 0, 1] ],

                 [ [0, 1, 0],
                   [0, 0, 0],          #
                   [0, 0, 1]],

                 [ [0,0,0],
                   [1,0,0],
                   [0,0,1]],

                 [ [1,0,0],
                   [1,1,1],
                   [0,0,0] ]

                 
                   

                

                ]


     # reference
     # x-1,y+1    x,y+1     x+1,y+1
     # x-1,y      x,y       x+1,y
     # x-1,y-1    x,y-1     x+1,y-1

    R1 = [x-1,y+1]
    R2 = [x,y+1]
    R3 = [x+1,y+1]
    R4 = [x-1,y]
    R5 = [x,y]
    R6 = [x+1,y]
    R7 = [x-1,y-1]
    R8 = [x,y-1]
    R9 = [x+1,y-1]

    # 1  2  3
    # 4  5  6
    # 7  8  9
    

    if np.sum(np.multiply(np.multiply(Diagonal_check[0],Position_matrix),Kernel_matrix)) == -25:
       #print (Diagonal_check[0])
       A =  [[1,0,0],
             [0,1,0],
             [0,0,1]]
       #print (np.multiply(A,Position_matrix))
       remove_coordinate = [R2, R3, R6, R4, R7, R8]
       S = 1
       return A, remove_coordinate


    if np.sum(np.multiply(np.multiply(Diagonal_check[1],Position_matrix),Kernel_matrix)) == 25:
        A = [[0,0,1],
             [0,1,0],
             [1,0,0]]
        #print (np.multiply(A,Position_matrix))
        remove_coordinate = [R1, R2, R4, R6, R8, R9]
        S=1
        return A, remove_coordinate

    if np.sum(np.multiply(np.multiply(Diagonal_check[2],Position_matrix),Kernel_matrix)) == 10 and np.sum(np.multiply(Position_matrix,Kernel_matrix)) != 17:
        A = [[1,0,1],             [0,1,0],             [0,0,0]]

        #A = [[1,0,0],             [0,1,0],             [0,1,0]]
        
        print (np.multiply(A,Position_matrix))
        remove_coordinate = [R2, R4, R6, R7, R8, R9]
        S=1
        return A, remove_coordinate

    if np.sum(np.multiply(np.multiply(Diagonal_check[2],Position_matrix),Kernel_matrix)) == 10 and np.sum(np.multiply(Position_matrix,Kernel_matrix)) == 17:
        A = [[1,0,0],
             [0,1,0],
             [0,1,0]]
         
        #print (np.multiply(A,Position_matrix))
        remove_coordinate = [R2, R3, R4, R6, R7, R9]
        S=1
        return A, remove_coordinate
        

    if np.sum(np.multiply(np.multiply(Diagonal_check[3],Position_matrix),Kernel_matrix)) == -10 and np.sum(np.multiply(Position_matrix,Kernel_matrix)) != -7:
        A = [[0,0,0],
             [0,1,0],
             [1,0,1]]
        #print (np.multiply(A,Position_matrix))
        remove_coordinate = [R1, R2, R3, R4, R6, R8]
        S=1
        return A, remove_coordinate


    if np.sum(np.multiply(np.multiply(Diagonal_check[3],Position_matrix),Kernel_matrix)) == -10 and np.sum(np.multiply(Position_matrix,Kernel_matrix)) == -7:
        A = [[0,1,0],
             [0,1,0],
             [1,0,0]]
        #print (np.multiply(A,Position_matrix))
        remove_coordinate = [R1, R3, R4, R6, R8, R9]
        S=1
        return A, remove_coordinate
    

    if np.sum(np.multiply(np.multiply(Diagonal_check[4],Position_matrix),Kernel_matrix)) == 5:
        A = [[1,0,0],
             [0,1,0],
             [1,0,0]]
        #print (np.multiply(A,Position_matrix))
        remove_coordinate = [R2, R3, R4, R6, R8, R9]
        return A, remove_coordinate

    if np.sum(np.multiply(np.multiply(Diagonal_check[5],Position_matrix),Kernel_matrix)) == -5 and np.sum(np.multiply(Position_matrix,Kernel_matrix)) != -10:
        A = [[0,0,1],
             [0,1,0],
             [0,0,1]]
        #print (np.multiply(A,Position_matrix))
        remove_coordinate = [R1, R2, R4, R6, R7, R8]
        S=1
        return A, remove_coordinate

    if np.sum(np.multiply(np.multiply(Diagonal_check[5],Position_matrix),Kernel_matrix)) == -5 and np.sum(np.multiply(Position_matrix,Kernel_matrix)) == -10:
        A = [[0,0,1],
             [1,1,0],
             [0,0,0]]
       # print (np.multiply(A,Position_matrix))
        remove_coordinate = [R1, R2, R6, R7, R8, R9]
        S=1
        return A, remove_coordinate


    

    if S==0:
        return None, [[0,0]]
    
    '''
    if np.sum(np.multiply(np.multiply(Diagonal_check[7],Position_matrix),Kernel_matrix)) == -24:
        print (Position_matrix)
        A = [[0,0,0],
             [1,1,0],
             [0,0,1]]
        print (np.multiply(A,Position_matrix))
        return A

    if np.sum(np.multiply(np.multiply(Diagonal_check[6],Position_matrix),Kernel_matrix)) == -16:
        print (Position_matrix)
        A = [[0,1,0],
             [0,1,0],
             [0,0,1]]
        print (np.multiply(A,Position_matrix))
        return A

    if np.sum(np.multiply(np.multiply(Diagonal_check[8],Position_matrix),Kernel_matrix)) == -26:
        print (Position_matrix)
        A = [[1,0,0],
             [0,1,1],
             [0,0,0]]
        print (np.multiply(A,Position_matrix))
        return A
    '''
   








#print (Matrix_list[0])

    
