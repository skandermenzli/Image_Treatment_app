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
root.geometry("800x650")
root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=3)
root.columnconfigure(2,weight=1)
frameBtn1 = LabelFrame(root, text="Buttons",)
frameBtn1.grid(row=0, column=0,sticky=tk.NE)
frameImg = LabelFrame(root, text="Image", padx=15, pady=15)
frameImg.grid(row=0, column=1)
frameBtn2 = LabelFrame(root, text="Filters",)
frameBtn2.grid(row=0, column=2,sticky=tk.NE)

def read_file(filename:str):

        color = False
        file = open(str(filename), "r")
        format = file.readline()
        info = file.readline()
        if(info.find(".PPM")!=-1):
            color = True
        print("color:",str(color))
        taille = file.readline()
        nb_col, nb_lig = taille.split(' ', 2)
        print(file.readline())
        tab = []

        for line in file:
            tab.extend([int(float(c)) for c in line.split()])

        if(color):
            matrix = np.reshape(tab, [int(nb_lig), int(nb_col),3])
        else:
            matrix = np.reshape(tab, [int(nb_lig), int(nb_col)])
        print(matrix)


        return matrix,format,nb_col, nb_lig







def setImage(matrix):
    global img
    #img = ImageTk.PhotoImage(image=Image.fromarray(matrix,"RGB"))
    img = plt.imshow(matrix, cmap='gray')
    fig = Figure(figsize=(4, 4), dpi=100)
    plot = fig.add_subplot()
    plot.imshow(matrix, cmap='gray')

    canvas =  FigureCanvasTkAgg(fig,master=frameImg)
    canvas.draw()
    canvas.get_tk_widget().grid(row=0, column=0)
    #canvas.grid(row=0, column=0)
    #canvas.create_image(20, 20, anchor=NW, image=img)
    

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

    setImage(image.matrix)

    format_label = Label(frameImg,text="image foramt : "+format )
    label_col = Label(frameImg,text="Number of Columns : "+nb_col )
    label_row = Label(frameImg, text="Number of Rows : " + nb_row)

    format_label.grid(row=2,column=0)
    label_row.grid(row=3,column=0)
    label_col.grid(row=4, column=0)

    btn_linear.config(state="normal")
    btn_egalisehist.config(state="normal")
    btn_median.config(state="normal")
    btn_moy.config(state="normal")
    btn_noise.config(state="normal")
    saveFile.config(state="normal")
    restoreFile.config(state="normal")
    btn_ceiling.config(state="normal")
    btn_ceiling_or.config(state="normal")
    btn_ceiling_and.config(state="normal")
    btn_ostu.config(state="normal")




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
    file.write(str(image.col))
    file.write(" ")
    file.write(str(image.row))
    # file.write(x , " ", y )
    file.write("\n255")
    for i in range(image.row):
        file.write("\n")
        for j in range(image.col):
            file.write(str(image.matrix[i][j]))
            file.write(" ")

    top = Toplevel(root)
    top.geometry("150x60")
    label = Label(top,text="Image saved!!" ,padx=6).pack()
def restoreImage():
    image.matrix = np.copy(original.matrix)
    setImage(image.matrix)
def egalise():
    image.matrix = image.egaliseHist()
    setImage(image.matrix)

def noise():
    image.matrix = image.saltAndPepper()
    setImage(image.matrix)


def applyMedian():
    n = int(e1.get())
    image.matrix = image.medianfilter(n)
    setImage(image.matrix)


def applyMoy():
    n = int(e2.get())
    image.matrix = image.moyfilter(n)
    setImage(image.matrix)


def openBox():
    top = Toplevel(root,padx=6,pady=6)
    top.geometry("300x150")
    lx1 = Label(top,text="x1:" ,padx=6).grid(row=0,column=0)
    xe1 = tk.Entry(top, width=6, font=('Arial 12'))
    xe1.grid(row=0,column=1)
    ly1 = Label(top, text="y1:" ,padx=6).grid(row=0, column=3)
    ye1 = tk.Entry(top, width=6, font=('Arial 12'))
    ye1.grid(row=0, column=4)
    lx2 = Label(top, text="x2:" ,padx=6).grid(row=1, column=0)
    xe2 = tk.Entry(top, width=6, font=('Arial 12'))
    xe2.grid(row=1,column=1)
    ly2 = Label(top, text="y2:", padx=6).grid(row=1, column=3)
    ye2 = tk.Entry(top, width=6, font=('Arial 12'))
    ye2.grid(row=1, column=4)


    def transform():
        x1 = int(xe1.get())
        x2 = int(xe2.get())
        y1 = int(ye1.get())
        y2 = int(ye2.get())
        image.matrix = image.linear_transform(x1,x2,y1,y2)
        setImage(image.matrix)
        top.destroy()


    btn_trf = tk.Button(top, text="Transform", padx=10, pady=5, command=transform).grid(row=2, column=2)


def ceil():
    top = Toplevel(root, padx=6, pady=6)
    top.geometry("350x100")
    c1_l = Label(top, text="ceil1:", padx=6).grid(row=0, column=0)
    ce1 = tk.Entry(top, width=6, font=('Arial 12'))
    ce1.grid(row=0, column=1)
    c2_l = Label(top, text="ceil2:", padx=6).grid(row=0, column=2)
    ce2 = tk.Entry(top, width=6, font=('Arial 12'))
    ce2.grid(row=0, column=3)
    c3_l = Label(top, text="ceil3:", padx=6).grid(row=0, column=4)
    ce3 = tk.Entry(top, width=6, font=('Arial 12'))
    ce3.grid(row=0, column=5)

    def applyCeil():
        c1 = int(ce1.get())
        c2 = int(ce2.get())
        c3 = int(ce3.get())
        image.matrix = image.seuilManuel([c1,c2,c3])
        setImage(image.matrix)
        top.destroy()

    btn_apply = tk.Button(top, text="Apply", padx=10, pady=5, command=applyCeil).grid(row=2, column=2,sticky=tk.S)


def applyOr():
    image.matrix = image.seuilOr()
    setImage(image.matrix)

def applyAnd():
    image.matrix = image.seuilAnd()
    setImage(image.matrix)


def applyOtsu():
    image.matrix = image.otsu()
    setImage(image.matrix)




## buttons

openFile= tk.Button(frameBtn1,text="Open Image",padx=10,pady=5,command=openImage)
openFile.grid(row=0,column=0,sticky=tk.W)

saveFile = tk.Button(frameBtn1,text="Save Image",padx=10,pady=5,command=saveImage,state= DISABLED)
saveFile.grid(row=1,column=0,sticky=tk.W)

restoreFile = tk.Button(frameBtn1,text="Restore Image",padx=10,pady=5,command=restoreImage,state= DISABLED)
restoreFile.grid(row=2,column=0,sticky=tk.W)





btn_egalisehist= tk.Button(frameBtn2,text="Egalisation Hist",padx=10,pady=5,command=egalise,state= DISABLED)
btn_egalisehist.grid(row=1,column=3,sticky=tk.E)
btn_noise= tk.Button(frameBtn2,text="Add noise",padx=10,pady=5,command=noise,state= DISABLED)
btn_noise.grid(row=2,column=3,sticky=tk.E)
img = ImageTk.PhotoImage(image=Image.open("images/placeholder.png").resize((300,222)))

e1 = tk.Entry(frameBtn2,width=4,font=('Arial 16'))
e1.grid(row=3,column=2)

btn_median = tk.Button(frameBtn2,text="Median filter",padx=10,pady=5,command=applyMedian,state= DISABLED)
btn_median.grid(row=3,column=3,sticky=tk.E)

e2 = tk.Entry(frameBtn2,width=4,font=('Arial 16'))
e2.grid(row=4,column=2)

btn_moy = tk.Button(frameBtn2,text="Moeyenne filter",padx=10,pady=5,command=applyMoy,state= DISABLED)
btn_moy.grid(row=4,column=3,sticky=tk.E)

btn_linear = tk.Button(frameBtn2,text="Linear transform",padx=10,pady=5,command=openBox,state= DISABLED)
btn_linear.grid(row=5,column=3)

btn_ceiling = tk.Button(frameBtn2,text="Manuel ceil",padx=10,pady=5,command=ceil,state= DISABLED)
btn_ceiling.grid(row=6,column=3,sticky=tk.E)

btn_ceiling_or = tk.Button(frameBtn2,text="Or ceil",padx=10,pady=5,command=applyOr,state= DISABLED)
btn_ceiling_or.grid(row=7,column=3,sticky=tk.E)

btn_ceiling_and = tk.Button(frameBtn2,text="And ceil",padx=10,pady=5,command=applyAnd,state= DISABLED)
btn_ceiling_and.grid(row=8,column=3,sticky=tk.E)

btn_ostu = tk.Button(frameBtn2,text="Otsu",padx=10,pady=5,command=applyOtsu,state= DISABLED)
btn_ostu.grid(row=9,column=3,sticky=tk.E)



label = Label(frameImg,image=img)
label.grid(row=0,column=0)



root.mainloop()
