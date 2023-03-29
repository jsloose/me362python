import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np

#Import images
IL = mpimg.imread("imageL.jpg")
IR = mpimg.imread("imageR.jpg")

#Grab calibration points
N = 6

imgplotL1 = plt.imshow(IL)
uvL = plt.ginput(N)

imgplotR1 = plt.imshow(IR)
uvR = plt.ginput(N)

#Associated calibration point values
x = [4, 8, 10, 4, 0, 0]
y = [2, 10, 0, 0, 2, 12]
z = [0, 0, 6, 8, 6, 8]

xyz = [[x],[y],[z]];

#Populate the needed DLC matrices
MatrixL = np.zeros(2*N,11)
MatrixR = np.zeros(2*N,11)

for i in range(N):
    MatrixL[2*i-1][1] = x[i]
    MatrixL[2*i-1][2] = y[i]
    MatrixL[2*i-1][3] = z[i]
    MatrixL[2*i-1][4] = 1
    MatrixL[2*i-1][9] = -uvL[i][1]*x[i]
    MatrixL[2*i-1][10] = -uvL[i][1]*y[i]
    MatrixL[2*i-1][11] = -uvL[i][1]*z[i]

    MatrixL[2*i][5] = x[i]
    MatrixL[2*i][6] = y[i]
    MatrixL[2*i][7] = z[i]
    MatrixL[2*i][8] = 1
    MatrixL[2*i][9] = -uvL[i][2]*x[i]
    MatrixL[2*i][10] = -uvL[i][2]*y[i]
    MatrixL[2*i][11] = -uvL[i][2]*z[i]

for i in range(N):
    MatrixR[2*i-1][1] = x[i]
    MatrixR[2*i-1][2] = y[i]
    MatrixR[2*i-1][3] = z[i]
    MatrixR[2*i-1][4] = 1
    MatrixR[2*i-1][9] = -uvR[i][1]*x[i]
    MatrixR[2*i-1][10] = -uvR[i][1]*y[i]
    MatrixR[2*i-1][11] = -uvR[i][1]*z[i]

    MatrixR[2*i][5] = x[i]
    MatrixR[2*i][6] = y[i]
    MatrixR[2*i][7] = z[i]
    MatrixR[2*i][8] = 1
    MatrixR[2*i][9] = -uvR[i][2]*x[i]
    MatrixR[2*i][10] = -uvR[i][2]*y[i]
    MatrixR[2*i][11] = -uvR[i][2]*z[i]

MatrixL_2 = np.zeros(2*N,1)
MatrixR_2 = np.zeros(2*N,1)

for i in range(N):
    MatrixL_2[2*i-1][1] = uvL[i][1]
    MatrixL_2[2*i][1] = uvL[i][2]

for i in range(N):
    MatrixR_2[2*i-1][1] = uvR[i][1]
    MatrixR_2[2*i][1] = uvR[i][2]

FL = MatrixL
gL = MatrixL_2
FR = MatrixR
gR = MatrixR_2

A = MatrixL
b = MatrixL_2

#Solve for the L and R matrices
x = np.divide(A,b)

L = x

A = MatrixR
b = MatrixR_2

x = np.divide(A,b)

R = x

#Select points in 3D space to solve for
imgplotL2 = plt.imshow(IL)
uvL_ref = plt.ginput(1)

imgplotR2 = plt.imshow(IR)
uvR_ref = plt.ginput(1)

#Populate the needed matrices and solve for x, y, and z
A = [[L[1] - L[9]*uvL_ref[1], L[2] - L[10]*uvL_ref[1], L[3] - L[11]*uvL_ref[1]],...
     [L[5] - L[9]*uvL_ref[2], L[6] - L[10]*uvL_ref[2], L[7] - L[11]*uvL_ref[2]],...
     [R[1] - R[9]*uvR_ref[1], R[2] - R[10]*uvR_ref[1], R[3] - R[11]*uvR_ref[1]],...
     [R[5] - R[9]*uvR_ref[2], R[6] - R[10]*uvR_ref[2], R[7] - R[11]*uvR_ref[2]]]

b = [[uvL_ref[1] - L[4]],...
     [uvL_ref[2] - L[8]],...
     [uvR_ref[1] - R[4]],...
     [uvR_ref[2] - R[8]]]

x = np.divide(A.b)

x_position = x[1]
y_position = x[2]
z_position = x[3]