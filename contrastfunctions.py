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

