from tkinter import *
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd
from PIL import ImageTk, Image
import numpy as np
import cv2
import webbrowser


def select_file():
    global imagePlace, imgPreview, filename, imgOriginal
    filetypes = (
        ('jpg files', '*.jpg'),
        ('png files', '*.png'),
        ('All files', '*.*')
    )

    try:
        filename = fd.askopenfilename(
            title='Open a file',
            initialdir='/',
            filetypes=filetypes)
        imgPreview = Image.open(filename)
        imgOriginal = Image.open(filename)
        imgPreview.thumbnail((866, 541))
        photo2 = ImageTk.PhotoImage(imgPreview)
        ImagePlace.config(image=photo2)
        ImagePlace.photo_ref = photo2
    except:
        img = Image.open("icons/background.png")
        img.thumbnail((866, 541))
        photo2 = ImageTk.PhotoImage(img)
        ImagePlace.config(image=photo2)
        ImagePlace.photo_ref = photo2

def boostImage(value):
    global filename, imagePlace, imgPreview, imgOriginal
    boost = 5 + (int(value) * 0.1)
    kernelBoost = np.array([
        [0, -1, 0],
        [-1, boost, -1],
        [0, -1, 0]
    ])
    try:
        imageCv = cv2.imread(filename)
        b, g, r = cv2.split(imageCv)
        cr = cv2.filter2D(src=r, ddepth=-1, kernel=kernelBoost)
        cg = cv2.filter2D(src=g, ddepth=-1, kernel=kernelBoost)
        cb = cv2.filter2D(src=b, ddepth=-1, kernel=kernelBoost)
        crgb = np.dstack((cr,cg,cb))
        imgPreview = Image.fromarray(crgb, "RGB")
        imgOriginal = Image.fromarray(crgb, "RGB")
        imgPreview.thumbnail((866, 541))
        photo2 = ImageTk.PhotoImage(imgPreview)
        ImagePlace.config(image=photo2)
        ImagePlace.photo_ref = photo2
    except:
        pass

def saveImage():
    global imgOriginal, imgPreview
    filename = fd.asksaveasfilename(initialdir="/",
                                    defaultextension="*.*",
                                    filetypes=(("jpg files","¨*.jpg"),
                                               ("png files","*.png"),
                                               ("all files","*.*")))
    print(filename)
    if not filename:
        return
    imgOriginal.save(filename)

def opengit():
    webbrowser.open("https://github.com/Davi4076018")

# criação da janela
sist=tk.Tk()

# titulo da janela
sist.title('Melhorador de Imagens - Filtro Boost')

# tamanho da janela

sist.resizable(False, False)
sist.geometry("953x568")



#criação dos tabs

tabControl = ttk.Notebook(sist)

tab1 = ttk.Frame(tabControl)
#tab2 = ttk.Frame(tabControl)

# cor do background
sist['bg'] = "#00a2ed"

tabControl.add(tab1, text='Boost')
#tabControl.add(tab2, text='Tab 2')
tabControl.pack(expand=1, fill="both")

# Cor e estilo dos tabs
style = ttk.Style()

style.theme_create('Meutema', settings={
    ".": {
        "configure": {
            "background": "#4d194d",  # cor dentro dos tabs
        }
    },
    "TNotebook": {
        "configure": {
            "background": "#391339",  # Cor da margem
            "tabmargins": [0, 0, 0, 0],  # margins: left, top, right, separator
        }
    },
    "TNotebook.Tab": {
        "configure": {
            "background": 'White',  # Cor do tab não selecionado
            "padding": [5, 1],
            # espaço do texto as extremidades do tab
        },
        "map": {
            "background": [("selected", "#4d194d")],  # Cor do tab selecionado
            "expand": [("selected", [2, 0, 2, 2])]  # Margens do texto
        }
    }
})

style.theme_use('Meutema')

#icons
iconimage = PhotoImage(file=r"icons/image.png").subsample(1, 1)
iconsave = PhotoImage(file=r"icons/save-64.png").subsample(1, 1)
icongit = PhotoImage(file=r"icons/github.png").subsample(1, 1)

# open button
open_button = Button(
    tab1,
    bg="#4d194d",
    command=select_file,
    image= iconimage,
    highlightbackground = "black",
    bd=2,
    width = 75,
    height = 75,
    wraplength=250)

save_button = Button(
    tab1,
    bg="#4d194d",
    command=saveImage,
    image= iconsave,
    highlightbackground = "white",
    bd=2,
    width = 75,
    height = 75,
    wraplength=250)

git_button = Button(
    tab1,
    bg="#4d194d",
    command=opengit,
    image= icongit,
    highlightbackground = "white",
    bd=2,
    width = 75,
    height = 75,
    wraplength=250)

#imagem padrão
img = Image.open("icons/background.png")
img.thumbnail((866, 541))
tkimage = ImageTk.PhotoImage(img)


ImagePlace = Label(tab1,
                   image=tkimage,
                   text = (" "),
                   bg = "Black",
                   fg = "White",
                   bd = 2,
                   relief = "solid",
                   width = 866,
                   height = 541,
                   justify = CENTER,
                   wraplength=250)

ValueBoost = Scale(tab1,
                   bg="#4d194d",
                   from_=1,
                   to=10,
                   fg="white",
                   command=boostImage,
                   font = "Crimson",
                   width = 75,
                   length = 297,
                   tickinterval = 1)

#Organização do Layout por Grid
ImagePlace.grid(row = 1, column=1, sticky ='w', rowspan = 3)
open_button.grid(row = 1, column=2, sticky = 'nw')
ValueBoost.grid(row = 1, column=2, sticky = 'nw', rowspan = 3, pady=81)
save_button.grid(row = 3, column=2, sticky = 'sw', pady=80)
git_button.grid(row = 3, column=2, sticky = 'sw')

#looping da janela
sist.mainloop()