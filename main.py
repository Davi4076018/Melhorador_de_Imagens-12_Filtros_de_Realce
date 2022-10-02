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
        ImagePlaceBoost.config(image=photo2)
        ImagePlaceBoost.photo_ref = photo2
        ImagePlaceOutros.config(image=photo2)
        ImagePlaceOutros.photo_ref = photo2
    except:
        img = Image.open("icons/background.png")
        img.thumbnail((866, 541))
        photo2 = ImageTk.PhotoImage(img)
        ImagePlaceBoost.config(image=photo2)
        ImagePlaceBoost.photo_ref = photo2
        ImagePlaceOutros.config(image=photo2)
        ImagePlaceOutros.photo_ref = photo2

def convRGB(kernel, arqImage):
    imageCv = cv2.imread(filename)
    b, g, r = cv2.split(imageCv)
    cr = cv2.filter2D(src=r, ddepth=-1, kernel=kernel)
    cg = cv2.filter2D(src=g, ddepth=-1, kernel=kernel)
    cb = cv2.filter2D(src=b, ddepth=-1, kernel=kernel)
    return (np.dstack((cr, cg, cb)))

def boostImage(value):
    global filename, imagePlace, imgPreview, imgOriginal
    boost = 5 + (int(value) * 0.1)
    kernelBoost = np.array([
        [0, -1, 0],
        [-1, boost, -1],
        [0, -1, 0]
    ])
    try:
        crgb = convRGB(kernelBoost, filename)
        imgPreview = Image.fromarray(crgb, "RGB")
        imgOriginal = Image.fromarray(crgb, "RGB")
        imgPreview.thumbnail((866, 541))
        photo2 = ImageTk.PhotoImage(imgPreview)
        ImagePlaceBoost.config(image=photo2)
        ImagePlaceBoost.photo_ref = photo2
    except:
        pass

def outrosFiltros(tipo):
    global filename, imagePlace, imgPreview, imgOriginal
    if tipo == 1:
        try:
            imgPreview = Image.open(filename)
            imgOriginal = Image.open(filename)
            imgPreview.thumbnail((866, 541))
            photo2 = ImageTk.PhotoImage(imgPreview)
            ImagePlaceOutros.config(image=photo2)
            ImagePlaceOutros.photo_ref = photo2
        except:
            img = Image.open("icons/background.png")
            img.thumbnail((866, 541))
            photo2 = ImageTk.PhotoImage(img)
            ImagePlaceOutros.config(image=photo2)
            ImagePlaceOutros.photo_ref = photo2
    else:
        if tipo == 2:
            # kernel Gaussiano
            kernelAtual = np.array([
                [0.0625, 0.125, 0.0625],
                [0.1250, 0.250, 0.1250],
                [0.0625, 0.125, 0.0625]
            ])
        elif tipo == 3:
            # kernel Laplaciano
            kernelAtual = np.array([
                [0, 1, 0],
                [1, -4, 1],
                [0, 1, 0]
            ])
        elif tipo == 4:
            # kernel Crista
            kernelAtual = np.array([
                [-1, -1, -1],
                [-1, 8, -1],
                [-1, -1, -1]
            ])
        elif tipo == 5:
            # kernel Gradiente
            kernelsobelx = np.array([
                [-1, 0, 1],
                [-2, 0, 2],
                [-1, 0, 1]
            ])
            kernelsobely = np.array([
                [-1, -2, -1],
                [0, 0, 0],
                [1, 2, 1]
            ])
            kernelAtual = np.add(kernelsobelx, kernelsobely)
        try:
            crgb = convRGB(kernelAtual, filename)
            imgPreview = Image.fromarray(crgb, "RGB")
            imgOriginal = Image.fromarray(crgb, "RGB")
            imgPreview.thumbnail((866, 541))
            photo2 = ImageTk.PhotoImage(imgPreview)
            ImagePlaceOutros.config(image=photo2)
            ImagePlaceOutros.photo_ref = photo2
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
tab2 = ttk.Frame(tabControl)

# cor do background
sist['bg'] = "#00a2ed"

tabControl.add(tab1, text='Filtro Boost')
tabControl.add(tab2, text='Outros Filtros')
tabControl.pack(expand=1, fill="both")

# Cor e estilo dos tabs
style = ttk.Style()

style.theme_create('Meutema', settings={
    ".": {
        "configure": {
            "background": "#15141B",  # cor dentro dos tabs
        }
    },
    "TNotebook": {
        "configure": {
            "background": "#0d1117",  # Cor da margem
            "tabmargins": [0, 0, 0, 0],  # margins: left, top, right, separator
        }
    },
    "TNotebook.Tab": {
        "configure": {
            "background": '#22212c',  # Cor do tab não selecionado
            "padding": [5, 1],
            # espaço do texto as extremidades do tab
        },
        "map": {
            "background": [("selected", "#15141B")],  # Cor do tab selecionado
            "expand": [("selected", [2, 0, 2, 2])]  # Margens do texto
        }
    }
})

style.theme_use('Meutema')
style.configure('TNotebook.Tab', font=('URW Gothic L','11','bold'), padding=[10, 2], foreground = "#61FEC9")

#icons
iconimage = PhotoImage(file=r"icons/image.png").subsample(1, 1)
iconsave = PhotoImage(file=r"icons/save-64.png").subsample(1, 1)
icongit = PhotoImage(file=r"icons/github.png").subsample(1, 1)
iconOriginal = PhotoImage(file=r"icons/IconOriginal.png").subsample(1, 1)
iconCrista = PhotoImage(file=r"icons/IconRidge.png").subsample(1, 1)
iconGaussiano = PhotoImage(file=r"icons/IconGaussiano.png").subsample(1, 1)
iconLaplaciano = PhotoImage(file=r"icons/IconLaplaciano.png").subsample(1, 1)
iconGradiente = PhotoImage(file=r"icons/IconGradiente.png").subsample(1, 1)


#imagem padrão
img = Image.open("icons/background.png")
img.thumbnail((866, 541))
tkimage = ImageTk.PhotoImage(img)

# Tab 1 components

open_buttonTab1 = Button(
    tab1,
    bg="#15141B",
    command=select_file,
    image= iconimage,
    highlightbackground="#A177FE",
    bd=2,
    width = 75,
    height = 75,
    wraplength=250)

save_buttonTab1 = Button(
    tab1,
    bg="#15141B",
    command=saveImage,
    image= iconsave,
    highlightbackground = "#A177FE",
    bd=2,
    width = 75,
    height = 75,
    wraplength=250)

git_buttonTab1 = Button(
    tab1,
    bg="#15141B",
    command=opengit,
    image= icongit,
    highlightbackground = "#A177FE",
    bd=2,
    width = 75,
    height = 75,
    wraplength=250)

ImagePlaceBoost = Label(tab1,
                        image=tkimage,
                        highlightbackground = "#A177FE",
                        text = (" "),
                        bg = "Black",
                        fg = "#A177FE",
                        bd = 2,
                        relief = "solid",
                        width = 866,
                        height = 541,
                        justify = CENTER,
                        wraplength=250)

ValueBoost = Scale(tab1,
                   highlightbackground = "#A177FE",
                   bg="#15141B",
                   from_=1,
                   to=10,
                   fg="#A177FE",
                   command=boostImage,
                   font=('Crimson','12','bold'),
                   width = 75,
                   length = 297,
                   tickinterval = 1)

# Segundo Tab

ImagePlaceOutros = Label(tab2,
                        image=tkimage,
                        text = (" "),
                        bg = "Black",
                        fg = "#A177FE",
                        bd = 2,
                        relief = "solid",
                        width = 866,
                        height = 541,
                        justify = CENTER,
                        wraplength=250)



open_buttonTab2 = Button(
    tab2,
    bg="#15141B",
    command=select_file,
    image= iconimage,
    highlightbackground = "black",
    bd=2,
    width = 75,
    height = 75,
    wraplength=250)

save_buttonTab2 = Button(
    tab2,
    bg="#15141B",
    command=saveImage,
    image= iconsave,
    highlightbackground = "#A177FE",
    bd=2,
    width = 75,
    height = 75,
    wraplength=250)

git_buttonTab2 = Button(
    tab2,
    bg="#15141B",
    command=opengit,
    image= icongit,
    highlightbackground = "#A177FE",
    bd=2,
    width = 75,
    height = 75,
    wraplength=250)

original_buttonTab2 = Button(
    tab2,
    bg="#15141B",
    command=lambda: outrosFiltros(1),
    image=iconOriginal,
    highlightbackground="#A177FE",
    bd=2,
    width=75,
    height=55,
    wraplength=250)

filtGaussiano_buttonTab2 = Button(
    tab2,
    bg="#15141B",
    command=lambda: outrosFiltros(2),
    image=iconGaussiano,
    highlightbackground="#A177FE",
    bd=2,
    width=75,
    height=56,
    wraplength=250)

filtLaplaciano_buttonTab2 = Button(
    tab2,
    bg="#15141B",
    command=lambda: outrosFiltros(3),
    image=iconLaplaciano,
    highlightbackground="#A177FE",
    bd=2,
    width=75,
    height=55,
    wraplength=250)

filtCrista_buttonTab2 = Button(
    tab2,
    bg="#15141B",
    command=lambda: outrosFiltros(4),
    image=iconCrista,
    highlightbackground="#A177FE",
    bd=2,
    width=75,
    height=53,
    wraplength=250)

filtGradiente_buttonTab2 = Button(
    tab2,
    bg="#15141B",
    command=lambda: outrosFiltros(5),
    image=iconGradiente,
    highlightbackground="#A177FE",
    bd=2,
    width=75,
    height=55,
    wraplength=250)

#Organização do Layout por Grid - 1 Tab
ImagePlaceBoost.grid(row = 1, column=1, sticky ='w', rowspan = 3)
open_buttonTab1.grid(row = 1, column=2, sticky ='nw')
ValueBoost.grid(row = 1, column=2, sticky = 'nw', rowspan = 3, pady=81)
save_buttonTab1.grid(row = 3, column=2, sticky ='sw', pady=80)
git_buttonTab1.grid(row = 3, column=2, sticky ='sw')

#Organização do Layout por Grid - 2 Tab
ImagePlaceOutros.grid(row = 1, column=1, sticky ='w', rowspan = 3)
open_buttonTab2.grid(row = 1, column=2, sticky ='nw')
original_buttonTab2.grid(row = 1, column=2, sticky = 'nw', rowspan = 2, pady=81)
filtGaussiano_buttonTab2.grid(row = 2, column=2, sticky ='nw', pady=23)
filtCrista_buttonTab2.grid(row = 3, column=2, sticky = 'nw')
filtLaplaciano_buttonTab2.grid(row = 2, column=2, sticky = 'sw')
filtGradiente_buttonTab2.grid(row = 3, column=2, sticky = 'nw', pady=58)
save_buttonTab2.grid(row = 3, column=2, sticky ='sw', pady=80)
git_buttonTab2.grid(row = 3, column=2, sticky ='sw')


#filtCrista_buttonTab2.grid(row = 2, column=2, sticky ='nw', pady=23)
#filtGaussiano_buttonTab2.grid(row = 2, column=2, sticky = 'sw')
#filtLaplaciano_buttonTab2.grid(row = 3, column=2, sticky = 'nw')

#looping da janela
sist.mainloop()