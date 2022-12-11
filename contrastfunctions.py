import numpy as np
import math


def egaliseHist(matrix,row,col):
    hist = np.zeros(256)
    for i in range(row):
        for j in range(col):
            hist[matrix[i, j]] = hist[matrix[i, j]] + 1

    histc = np.zeros(256)
    histc[0] = hist[0]
    for i in range(1, 256):
        histc[i] = histc[i - 1] + hist[i]

    pc = histc / (row*col)
    lut = np.zeros(256)
    for i in range(256):
        lut[i] = math.floor(pc[i] * 255)


    matrix_hist = np.zeros((row,col))


    for i in range(row):
        for j in range(col):
            matrix_hist[i, j] = lut[matrix[i, j]]

    return matrix_hist

def create_lut(x1,x2,y1,y2):
    a1 = y1/x1
    a2 = (y2-y1)/(x2-x1)
    b2 = y2 - a2*x2
    a3 = (255-y2)/(255-x2)
    b3 = 255 - a3*255
    lut = np.zeros(256)
    for i in range(256):
        if(i < x1):
            lut[i] = i*a1
        elif(x1<=i<x2):
            lut[i] = i*a2 +b2
        else:
            lut[i] = i*a3 +b3
    return lut

def lineraTransform(x1,x2,y1,y2,matrix,row,col):
    lut = create_lut(x1,x2,y1,y2)

    matrix_t = np.zeros((row, col))

    for i in range(row):
        for j in range(col):
            matrix_t[i, j] = math.floor(lut[matrix[i, j]])

    return matrix_t
