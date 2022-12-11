
import numpy as np
import random


### filtre Moyenne

def filtreMoy(n ,img ,M ,N):
    mask = np.ones([n, n], dtype = int)
    mask = mask / ( n *n)
    img_new = img
    n2 = int( n /2)


    for i in range(1, M- n2):
        for j in range(1, N - n2):
            temp = 0
            for k in range(-n2, n2 + 1):
                for l in range(-n2, n2 + 1):
                    temp += mask[l, k] * img[i - l, j - k]

            img_new[i, j] = temp

    return img_new




### filtre Median

def filtreMed(n, img, M, N):
    img_new = img
    n2 = int(n / 2)
    for i in range(1, M - n2):
        for j in range(1, N - n2):
            temp = []
            for k in range(-n2, n2 + 1):
                for l in range(-n2, n2 + 1):
                    temp.append(img[i - l, j - k])

            temp.sort()
            print(temp)
            img_new[i, j] = temp[int(n * n / 2)]
    return img_new


def createNoise(matrix,row,col):
    matrix_bruit = matrix
    for i in range(row):
        for j in range(col):
            x = random.randint(0, 20)
            if (x == 20):
                matrix_bruit[i, j] = 255
            elif (x == 0):
                matrix_bruit[i, j] = 0

    return matrix_bruit