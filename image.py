from contrastfunctions import *
from spatialfilters import *

class MyImage:
    def __init__(self, matrix, row, col):

        self.matrix = matrix
        self.row = row
        self.col = col


    def medianfilter(self,n):

        return np.copy(filtreMed(n,self.matrix,self.row,self.col))



    def moyfilter(self,n):

        return np.copy(filtreMoy(n,self.matrix,self.row,self.col))






