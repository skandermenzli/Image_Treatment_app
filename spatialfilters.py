
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


def seuilManuel(img,seuils):
    x,y,z =img.shape
    img_seuil = img
    for i in range(x):
        for j in range(y):
            for k in range(z):
                if(img[i][j][k]<seuils[k]):
                    img_seuil[i][j][k] = 0
                else:
                    img_seuil[i][j][k] = 255
    return img_seuil


def seuilManuelOu(img):
    x,y,z =img.shape
    img_seuil = img
    for i in range(x):
        for j in range(y):
                for k in range(z):
                    if(img[i][j][k]==255):
                        img_seuil[i][j] = np.array([255,255,255])
                        break
    return img_seuil


def seuilManuelEt(img):
    x, y, z = img.shape

    img_seuil = img
    for i in range(x):
        for j in range(y):
            l = 0
            for k in range(z):
                if (img[i][j][k] == 255):
                    l += 1

            if (l != 3):
                img_seuil[i][j] = np.zeros(z)
    return img_seuil


def threshold_otsu_impl(image, nbins=0.1):
    # validate grayscale
    if len(image.shape) == 1 or len(image.shape) > 2:
        print("must be a grayscale image.")
        return

    # validate multicolored
    if np.min(image) == np.max(image):
        print("the image must have multiple colors")
        return

    all_colors = image.flatten()
    total_weight = len(all_colors)
    least_variance = -1
    least_variance_threshold = -1

    # create an array of all possible threshold values which we want to loop through
    color_thresholds = np.arange(np.min(image) + nbins, np.max(image) - nbins, nbins)

    # loop through the thresholds to find the one with the least within class variance
    for color_threshold in color_thresholds:
        bg_pixels = all_colors[all_colors < color_threshold]
        weight_bg = len(bg_pixels) / total_weight
        variance_bg = np.var(bg_pixels)

        fg_pixels = all_colors[all_colors >= color_threshold]
        weight_fg = len(fg_pixels) / total_weight
        variance_fg = np.var(fg_pixels)

        within_class_variance = weight_fg * variance_fg + weight_bg * variance_bg
        if least_variance == -1 or least_variance > within_class_variance:
            least_variance = within_class_variance
            least_variance_threshold = color_threshold
        print("trace:", within_class_variance, color_threshold)

    return least_variance_threshold

def ostuBinary(matrix,row,col):
    threshold = threshold_otsu_impl(matrix)
    print("this is the threshold: ",threshold)
    for i in range(row):
        for j in range(col):
            if(matrix[i,j]>threshold):
                #foreground
                matrix[i,j] = 0
            else:
                matrix[i, j] = 255

    return matrix

