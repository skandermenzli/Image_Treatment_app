import tkinter as tk
from tkinter import *
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image, ImageTk
import math
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,
NavigationToolbar2Tk)

from tkinter import filedialog
from contrastfunctions import egaliseHist
from spatialfilters import *
from image import MyImage

root = Tk()

root.title('image app')
root.geometry("800x600")
root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=3)
root.columnconfigure(2,weight=1)
frameBtn1 = LabelFrame(root, text="Buttons",)
frameBtn1.grid(row=0, column=0,sticky=tk.NE)
frameImg = LabelFrame(root, text="Image", padx=15, pady=15)
frameImg.grid(row=0, column=1)
frameBtn2 = LabelFrame(root, text="Buttons",)
frameBtn2.grid(row=0, column=2,sticky=tk.NE)

def read_file(filename:str):

        file = open(str(filename), "r")
        format = file.readline()
        print(file.readline())

        taille = file.readline()
        nb_col, nb_lig = taille.split(' ', 2)
        print(file.readline())
        tab = []
        for line in file:
            tab.extend([int(c) for c in line.split()])
        matrix = np.reshape(tab, [int(nb_lig), int(nb_col)])
        print(matrix)


        return matrix,format,nb_col, nb_lig







def setImage(matrix):
    global img
    img = ImageTk.PhotoImage(image=Image.fromarray(matrix))

    canvas = Canvas(frameImg)
    canvas.grid(row=0, column=0)
    canvas.create_image(20, 20, anchor=NW, image=img)

    label_mean = Label(frameImg, text="Mean : " + str(matrix.mean()))
    label_var = Label(frameImg, text="Variance : " + str(matrix.var()))
    label_mean.grid(row=5, column=0)
    label_var.grid(row=6, column=0)
def openImage():
    global img
    global matrix
    global nb_col
    global nb_row
    global image
    global original
    filename= filedialog.askopenfilename(initialdir="Images",title="choose image")

    matrix,format,nb_col, nb_row = read_file(filename)
    image = MyImage(matrix,int(nb_row),int(nb_col))
    original = MyImage(np.copy(matrix),int(nb_row),int(nb_col))
    original.matrix[0][0] = 999
    #image.matrix = original.matrix
    #print(original.matrix)
    #print(image.matrix)

    setImage(matrix)

    format_label = Label(frameImg,text="image foramt : "+format )
    label_col = Label(frameImg,text="Number of Columns : "+nb_col )
    label_row = Label(frameImg, text="Number of Rows : " + nb_row)

    format_label.grid(row=2,column=0)
    label_row.grid(row=3,column=0)
    label_col.grid(row=4, column=0)


    def hist():
        top =Toplevel()
        top.title("Histograme")

        fig = Figure(figsize=(5, 5), dpi=100)
        plot1 = fig.add_subplot(111)
        plot1.hist(matrix)
        canvas = FigureCanvasTkAgg(fig, master=top)
        canvas.draw()
        canvas.get_tk_widget().pack()
        toolbar = NavigationToolbar2Tk(canvas, top)
        toolbar.update()
        # placing the toolbar on the Tkinter window
        canvas.get_tk_widget().pack()


    btn_hist = Button(frameImg,text="Hist",padx=10,pady=5,command=hist)
    btn_hist.grid(row=7,column=0)


def saveImage():
    file = open("Images/image.pgm", "w")
    file.write("P2\n")
    file.write("# chat.pgm nbre de ligne =")
    file.write(str(image.row))
    file.write(" nbre de colonne = ")
    file.write(str(image.col))
    file.write("\n")
    file.write(str(image.row))
    file.write(" ")
    file.write(str(image.col))
    # file.write(x , " ", y )
    file.write("\n255")
    for i in range(image.row):
        file.write("\n")
        for j in range(image.col):
            file.write(str(image.matrix[i][j]))
            file.write(" ")
def restoreImage():
    image.matrix = np.copy(original.matrix)
    setImage(image.matrix)
def egalise():
    matrix_eg = egaliseHist(matrix,int(nb_row),int(nb_col))
    setImage(matrix_eg)

def noise():
    matrix_bruit = createNoise(matrix,int(nb_row),int(nb_col))
    setImage(matrix_bruit)


def applyMedian():
    n = int(e1.get())
    image.matrix = image.medianfilter(n)
    setImage(image.matrix)


def applyMoy():
    n = int(e2.get())
    image.matrix = image.moyfilter(n)
    setImage(image.matrix)


## buttons

openFile= tk.Button(frameBtn1,text="Open Image",padx=10,pady=5,command=openImage)
openFile.grid(row=0,column=0,sticky=tk.W)

saveFile = tk.Button(frameBtn1,text="Save Image",padx=10,pady=5,command=saveImage)
saveFile.grid(row=1,column=0,sticky=tk.W)

restoreFile = tk.Button(frameBtn1,text="Restore Image",padx=10,pady=5,command=restoreImage)
restoreFile.grid(row=2,column=0,sticky=tk.W)





btn_egalisehist= tk.Button(frameBtn2,text="Egalisation Hist",padx=10,pady=5,command=egalise)
btn_egalisehist.grid(row=1,column=3,sticky=tk.E)
btn_noise= tk.Button(frameBtn2,text="Add noise",padx=10,pady=5,command=noise)
btn_noise.grid(row=2,column=3,sticky=tk.E)
img = ImageTk.PhotoImage(image=Image.open("images/placeholder.png").resize((300,222)))

e1 = tk.Entry(frameBtn2,width=4,font=('Arial 16'))
e1.grid(row=3,column=2)

btn_median = tk.Button(frameBtn2,text="Median filter",padx=10,pady=5,command=applyMedian)
btn_median.grid(row=3,column=3)

e2 = tk.Entry(frameBtn2,width=4,font=('Arial 16'))
e2.grid(row=4,column=2)

btn_moy = tk.Button(frameBtn2,text="Moeyenne filter",padx=10,pady=5,command=applyMoy)
btn_moy.grid(row=4,column=3)



label = Label(frameImg,image=img)
label.grid(row=0,column=0)



root.mainloop()
