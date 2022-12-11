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


    def saltAndPepper(self):
        return np.copy(createNoise(self.matrix,self.row,self.col))



    def egaliseHist(self):
        return np.copy(egaliseHist(self.matrix,self.row,self.col))

    def linear_transform(self,x1,x2,y1,y2):
        return np.copy(lineraTransform(x1,x2,y1,y2,self.matrix,self.row,self.col))

    def seuilManuel(self,seuils):
        return np.copy(seuilManuel(self.matrix,seuils))

    def seuilOr(self):
        return np.copy(seuilManuelOu(self.matrix))

    def seuilAnd(self):
        return np.copy(seuilManuelEt(self.matrix))






