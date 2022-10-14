from tkinter import *
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd
from PIL import ImageTk, Image
import numpy as np
from math import sqrt
import cv2
import webbrowser


def select_file():
    global imagePlace, imgPreview, filename, imgOriginal
    filetypes = (
        ('All files', '*.*'),
        ('jpg files', '*.jpg'),
        ('png files', '*.png')
    )

    try:
        filename = fd.askopenfilename(
            title='Open a file',
            initialdir='/',
            filetypes=filetypes)
        imgPreview = Image.open(filename).convert("RGB")
        imgOriginal = Image.open(filename).convert("RGB")
        imgPreview.thumbnail((866, 541))
        photo2 = ImageTk.PhotoImage(imgPreview)
    except:
        img = Image.open("icons/background.png").convert("RGB")
        img.thumbnail((866, 541))
        photo2 = ImageTk.PhotoImage(img)
    ImagePlaceBoost.config(image=photo2)
    ImagePlaceBoost.photo_ref = photo2
    ImagePlaceOutros.config(image=photo2)
    ImagePlaceOutros.photo_ref = photo2
    ImagePlaceLP.config(image=photo2)
    ImagePlaceLP.photo_ref = photo2
    ImagePlaceHP.config(image=photo2)
    ImagePlaceHP.photo_ref = photo2
    ImagePlaceBP.config(image=photo2)
    ImagePlaceBP.photo_ref = photo2
    ImagePlaceMorf.config(image=photo2)
    ImagePlaceMorf.photo_ref = photo2

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
            imgPreview = Image.open(filename).convert("RGB")
            imgOriginal = Image.open(filename).convert("RGB")
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

def distance(point1,point2):
    return sqrt((point1[0]-point2[0])**2 + (point1[1]-point2[1])**2)

def lpRGB(D0, imgShape, img):
    original = np.fft.fft2(img)
    centerf = np.fft.fftshift(original)
    base = np.zeros(imgShape[:2])
    rows, cols = imgShape[:2]
    center = (rows / 2, cols / 2)
    for x in range(cols):
        for y in range(rows):
            if distance((y,x),center) < D0 or distance((y,x),center) > 100:
                base[y, x] = 1
    LowPassCenterIdeal = centerf * base
    DesLowPassIdeal = np.fft.ifftshift(LowPassCenterIdeal)
    lpIdeal = np.fft.ifft2(DesLowPassIdeal)
    return abs(lpIdeal)

def lpImage(event):
    global filename, imagePlace, imgPreview, imgOriginal
    value = ValueBoostTab3.get()
    ValueBoostTab3.config(state="disabled")
    try:
        img = cv2.imread(filename)
    except:
        img = cv2.imread("icons/background.png")
    b, g, r = cv2.split(img)
    D0 = int(value) * 10.2
    lpColor = (np.dstack((lpRGB(D0, r.shape, r), lpRGB(D0, g.shape, g), lpRGB(D0, b.shape, b))))
    lpColor = lpColor/np.amax(lpColor)
    try:
        imgPreview = Image.fromarray((lpColor * 255).astype(np.uint8), "RGB")
        imgOriginal = Image.fromarray((lpColor * 255).astype(np.uint8), "RGB")
        imgPreview.thumbnail((866, 541))
        photo2 = ImageTk.PhotoImage(imgPreview)
        ImagePlaceLP.config(image=photo2)
        ImagePlaceLP.photo_ref = photo2
        ValueBoostTab3.config(state="active")
    except:
        pass

def hpRGB(D0, imgShape, img):
    original = np.fft.fft2(img)
    centerf = np.fft.fftshift(original)
    base = np.ones(imgShape[:2])
    rows, cols = imgShape[:2]
    center = (rows / 2, cols / 2)
    for x in range(cols):
        for y in range(rows):
            if distance((y,x),center) < D0 or distance((y,x),center) > 100:
                base[y, x] = 0
    LowPassCenterIdeal = centerf * base
    DesLowPassIdeal = np.fft.ifftshift(LowPassCenterIdeal)
    lpIdeal = np.fft.ifft2(DesLowPassIdeal)
    return abs(lpIdeal)

def hpImage(event):
    global filename, imagePlace, imgPreview, imgOriginal
    value = ValueBoostTab4.get()
    ValueBoostTab4.config(state="disabled")
    try:
        img = cv2.imread(filename)
    except:
        img = cv2.imread("icons/background.png")
    b, g, r = cv2.split(img)
    D0 = int(value) * 10.2
    hpColor = (np.dstack((hpRGB(D0, r.shape, r), hpRGB(D0, g.shape, g), hpRGB(D0, b.shape, b))))
    hpColor = hpColor/np.amax(hpColor)
    try:
        imgPreview = Image.fromarray((hpColor * 255).astype(np.uint8), "RGB")
        imgOriginal = Image.fromarray((hpColor * 255).astype(np.uint8), "RGB")
        imgPreview.thumbnail((866, 541))
        photo2 = ImageTk.PhotoImage(imgPreview)
        ImagePlaceHP.config(image=photo2)
        ImagePlaceHP.photo_ref = photo2
        ValueBoostTab4.config(state="active")
    except:
        pass

def bpRGB(D0, D1, imgShape, img):
    original = np.fft.fft2(img)
    centerf = np.fft.fftshift(original)
    base = np.zeros(imgShape[:2])
    rows, cols = imgShape[:2]
    center = (rows / 2, cols / 2)
    for x in range(cols):
        for y in range(rows):
            if distance((y, x), center) < D0 or distance((y, x), center) > D1:
                base[y, x] = 1
    LowPassCenterIdeal = centerf * base
    DesLowPassIdeal = np.fft.ifftshift(LowPassCenterIdeal)
    bpIdeal = np.fft.ifft2(DesLowPassIdeal)
    return abs(bpIdeal)

def converteValores(value):
    l1 = [0, 1, 2, 3, 4, 5]
    l2 = [10, 9, 8, 7, 6, 5]
    local = l2.index(value)
    return l1[local]

def bpImage(event):
    global filename, imagePlace, imgPreview, imgOriginal
    valueLow = ValueBoostTab5Low.get()
    valueHigh = ValueBoostTab5High.get()
    ValueBoostTab5Low.config(state="disabled")
    ValueBoostTab5High.config(state="disabled")
    try:
        img = cv2.imread(filename)
    except:
        img = cv2.imread("icons/background.png")
    b, g, r = cv2.split(img)
    D0 = int(converteValores(valueLow)) * 10.2
    D1 = int(valueHigh) * 10.2
    bpColor = (np.dstack((bpRGB(D0, D1, r.shape, r), bpRGB(D0, D1, g.shape, g), bpRGB(D0, D1, b.shape, b))))
    bpColor = bpColor/np.amax(bpColor)
    try:
        imgPreview = Image.fromarray((bpColor * 255).astype(np.uint8), "RGB")
        imgOriginal = Image.fromarray((bpColor * 255).astype(np.uint8), "RGB")
        imgPreview.thumbnail((866, 541))
        photo2 = ImageTk.PhotoImage(imgPreview)
        ImagePlaceBP.config(image=photo2)
        ImagePlaceBP.photo_ref = photo2
        ValueBoostTab5High.config(state="active")
        ValueBoostTab5Low.config(state="active")
    except:
        pass

def saveImage():
    global imgOriginal, imgPreview
    filename = fd.asksaveasfilename(initialdir="/",
                                    defaultextension="*.*",
                                    filetypes=(("jpg files","¨*.jpg"),
                                               ("png files","*.png"),
                                               ("all files","*.*")))
    if not filename:
        return
    imgOriginal.save(filename)

def opengit():
    webbrowser.open("https://github.com/Davi4076018")

def openOpcoes():
    global iconOpcao2, iconSalvar, iconFechar, iconDilationValue\
        , iconErosionValue, iconKernel1, iconKernel2, iconKernel3, iconKernel4\
        , iconKernel1O, iconKernel2O, iconKernel3O, iconKernel4O, iconKernelTitle\
        , kerneltab6, dvaluetab6, evaluetab6, iconManter, iconResete, iconManterO\
        , iconSalvarO, mantertab6, imgPreview, imgOriginal
    kernelvalue = kerneltab6
    dilationValue = dvaluetab6
    erosionValue = evaluetab6
    mantervalue = mantertab6
    opcaoScreen = Toplevel()
    opcaoScreen.resizable(False, False)
    opcaoScreen.geometry('500x500')
    opcaoScreen.grab_set()
    opcaoScreen['bg'] = "#0d1117"
    titleopcoes = ttk.Label(opcaoScreen,
                        image=iconOpcao2,
                        background="#0d1117")

    titleKernel = ttk.Label(opcaoScreen,
                            image=iconKernelTitle,
                            background="#0d1117")

    labelValueErosion = ttk.Label(opcaoScreen,
                            image=iconErosionValue,
                            background="#0d1117")

    labelValueDilation = ttk.Label(opcaoScreen,
                                  image=iconDilationValue,
                                  background="#0d1117")


    ErosionValueEntry = Entry(opcaoScreen,
                         bg='#15141B',
                         font=('URW Gothic L','11','bold'),
                         fg='#5ef5c2',
                         justify='right')
    DilationValueEntry = Entry(opcaoScreen,
                          bg='#15141B',
                          font=('URW Gothic L','11','bold'),
                          fg='#5ef5c2',
                          justify='right')


    separatortitle = ttk.Separator(opcaoScreen, orient=tk.HORIZONTAL)
    separatortitle2 = ttk.Separator(opcaoScreen, orient=tk.HORIZONTAL)
    separatortitle3 = ttk.Separator(opcaoScreen, orient=tk.HORIZONTAL)

    def closeOpcoes():
        opcaoScreen.destroy()

    def kernelselect(value):
        global kernelvalue
        kernelvalue = value
        if kernelvalue == 1:
            Kernel1button.config(image=iconKernel1O)
            Kernel2button.config(image=iconKernel2)
            Kernel3button.config(image=iconKernel3)
            Kernel4button.config(image=iconKernel4)
        elif kernelvalue == 2:
            Kernel2button.config(image=iconKernel2O)
            Kernel1button.config(image=iconKernel1)
            Kernel3button.config(image=iconKernel3)
            Kernel4button.config(image=iconKernel4)
        elif kernelvalue == 3:
            Kernel3button.config(image=iconKernel3O)
            Kernel2button.config(image=iconKernel2)
            Kernel1button.config(image=iconKernel1)
            Kernel4button.config(image=iconKernel4)
        elif kernelvalue == 4:
            Kernel4button.config(image=iconKernel4O)
            Kernel2button.config(image=iconKernel2)
            Kernel3button.config(image=iconKernel3)
            Kernel1button.config(image=iconKernel1)

    def saveOpcoes():
        global kernelvalue, kerneltab6, dilationValue, erosionValue, dvaluetab6, evaluetab6
        kerneltab6 = kernelvalue
        dvaluetab6 = int(DilationValueEntry.get())
        evaluetab6 = int(ErosionValueEntry.get())
        save_buttonOpcao.config(image=iconSalvarO)

    def resetOpcoes():
        global imgPreview, imgOriginal
        try:
            img = np.array(Image.open(filename).convert("RGB"))
        except:
            img = np.array(Image.open("icons/background.png").convert("RGB"))
        imgPreview = Image.fromarray(img, "RGB")
        imgOriginal = Image.fromarray(img, "RGB")
        imgPreview.thumbnail((866, 541))
        photo2 = ImageTk.PhotoImage(imgPreview)
        ImagePlaceMorf.config(image=photo2)
        ImagePlaceMorf.photo_ref = photo2


    def manterOpcoes():
        global mantertab6, mantervalue
        if mantertab6 == 1:
            mantervalue = 0
            mantertab6 = mantervalue
            manter_buttonOpcao.config(image=iconManter)
        else:
            mantervalue = 1
            mantertab6 =  mantervalue
            manter_buttonOpcao.config(image=iconManterO)

    def salvamanterstatus():
        global mantertab6
        if mantertab6 == 1:
            manter_buttonOpcao.config(image=iconManterO)

    Kernel1button = Button(
        opcaoScreen,
        bg="#15141B",
        command=lambda: kernelselect(1),
        image=iconKernel1O,
        highlightbackground="#A177FE",
        bd=2)

    Kernel2button = Button(
        opcaoScreen,
        bg="#15141B",
        command=lambda: kernelselect(2),
        image=iconKernel2,
        highlightbackground="#A177FE",
        bd=2)

    Kernel3button = Button(
        opcaoScreen,
        bg="#15141B",
        command=lambda: kernelselect(3),
        image=iconKernel3,
        highlightbackground="#A177FE",
        bd=2)

    Kernel4button = Button(
        opcaoScreen,
        bg="#15141B",
        command=lambda: kernelselect(4),
        image=iconKernel4,
        highlightbackground="#A177FE",
        bd=2)


    close_buttonOpcao = Button(
        opcaoScreen,
        bg="#15141B",
        command=closeOpcoes,
        image=iconFechar,
        highlightbackground="#A177FE",
        bd=2)

    save_buttonOpcao = Button(
        opcaoScreen,
        bg="#15141B",
        command=saveOpcoes,
        image=iconSalvar,
        highlightbackground="#A177FE",
        bd=2)

    reset_buttonOpcao = Button(
        opcaoScreen,
        bg="#15141B",
        command=resetOpcoes,
        image=iconResete,
        highlightbackground="#A177FE",
        bd=2)

    manter_buttonOpcao = Button(
        opcaoScreen,
        bg="#15141B",
        command=manterOpcoes,
        image=iconManter,
        highlightbackground="#A177FE",
        bd=2)

    titleopcoes.place(x=175, y=0)
    separatortitle.place(x=20, y=40, width=460)
    labelValueErosion.place(x=40, y=70, width=460)
    labelValueDilation.place(x=37, y=120, width=460)
    DilationValueEntry.place(x=185, y=80, width=250, height=25)
    ErosionValueEntry.place(x=185, y=130, width=250, height=25)
    separatortitle2.place(x=20, y=190, width=460)
    titleKernel.place(x=175, y=190)
    Kernel1button.place(x=20, y=260, width=100, height=100)
    Kernel2button.place(x=140, y=260, width=100, height=100)
    Kernel3button.place(x=260, y=260, width=100, height=100)
    Kernel4button.place(x=380, y=260, width=100, height=100)
    separatortitle3.place(x=20, y=400, width=460)
    manter_buttonOpcao.place(x=20, y=435, width=100, height=50)
    reset_buttonOpcao.place(x=140, y=435, width=100, height=50)
    save_buttonOpcao.place(x=260, y=435, width=100, height=50)
    close_buttonOpcao.place(x=380, y=435, width=100, height=50)

    kernelselect(kernelvalue)
    salvamanterstatus()
    DilationValueEntry.insert(0, str(dilationValue))
    ErosionValueEntry.insert(0, str(erosionValue))

kerneltab6 = 1
evaluetab6 = 1
dvaluetab6 = 1
mantertab6 = 0

def erosionOrdilation(type):
    global kerneltab6, evaluetab6, dvaluetab6, mantertab6, imgPreview, imgOriginal
    if mantertab6 == 0:
        try:
            img = np.array(Image.open(filename).convert("RGB"))
        except:
            img = np.array(Image.open("icons/background.png").convert("RGB"))
    else:
        try:
            img = np.array(imgOriginal.convert("RGB"))
        except:
            img = np.array(cv2.imread("icons/background.png").convert("RGB"))
    if kerneltab6 == 1:
        kernelatual = np.array([
        [0, 1, 0],
        [1, 1, 1],
        [0, 1, 0]
        ], np.uint8)
    elif kerneltab6 == 2:
        kernelatual = np.array([
            [1, 1, 1],
            [1, 1, 1],
            [1, 1, 1]
        ], np.uint8)
    elif kerneltab6 == 3:
        kernelatual = np.array([
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [1, 1, 1, 1, 1],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0]
        ], np.uint8)
    elif kerneltab6 == 4:
        kernelatual = np.array([
            [0, 0, 1, 0, 0],
            [0, 0, 1, 0, 0],
            [0, 0, 1, 0, 0],
            [0, 0, 1, 0, 0],
            [0, 0, 1, 0, 0]
        ], np.uint8)
    if type == 1:
        img = cv2.erode(img, kernelatual, iterations=evaluetab6)
    elif type == 2:
        img = cv2.dilate(img, kernelatual, iterations=dvaluetab6)
    elif type == 3:
        img = cv2.erode(img, kernelatual, iterations=evaluetab6)
        img = cv2.dilate(img, kernelatual, iterations=dvaluetab6)
    elif type == 4:
        img = cv2.dilate(img, kernelatual, iterations=dvaluetab6)
        img = cv2.erode(img, kernelatual, iterations=evaluetab6)
    """""""""
    fig, ax = plt.subplots(nrows=2, ncols=2)
    ax[0, 0].imshow(img, cmap='gray')
    ax[0, 0].set_title("img", fontsize=8, pad=10)
    fig.subplots_adjust(hspace=0.2, wspace=0)
    plt.show()
    """""""""
    try:
        imgPreview = Image.fromarray(img, "RGB")
        imgOriginal = Image.fromarray(img, "RGB")
        imgPreview.thumbnail((866, 541))
        photo2 = ImageTk.PhotoImage(imgPreview)
        ImagePlaceMorf.config(image=photo2)
        ImagePlaceMorf.photo_ref = photo2
    except:
        pass

# criação da janela
sist=tk.Tk()

# titulo da janela
sist.title('Melhorador de Imagens - 12 Filtros de Realce')

# tamanho da janela

sist.resizable(False, False)
sist.geometry("953x568")



#criação dos tabs

tabControl = ttk.Notebook(sist)

tab1 = ttk.Frame(tabControl)
tab2 = ttk.Frame(tabControl)
tab3 = ttk.Frame(tabControl)
tab4 = ttk.Frame(tabControl)
tab5 = ttk.Frame(tabControl)
tab6 = ttk.Frame(tabControl)

# cor do background
sist['bg'] = "#15141B"

tabControl.add(tab1, text='Filtro Boost')
tabControl.add(tab2, text='Outros Filtros')
tabControl.add(tab3, text='Filtro Passa-Baixa')
tabControl.add(tab4, text='Filtro Passa-Alta')
tabControl.add(tab5, text='Filtro Passa-Banda')
tabControl.add(tab6, text='Filtros Morfológicos ')
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
iconOpcao = PhotoImage(file=r"icons/IconOpcao.png").subsample(1, 1)
iconOpcao2 = PhotoImage(file=r"icons/IconOpcao2x.png").subsample(1, 1)
iconErosao = PhotoImage(file=r"icons/IconErosao.png").subsample(1, 1)
iconDilatacao = PhotoImage(file=r"icons/IconDilatacao.png").subsample(1, 1)
iconAbertura = PhotoImage(file=r"icons/IconAbertura.png").subsample(1, 1)
iconFechamento = PhotoImage(file=r"icons/IconFechamento.png").subsample(1, 1)
iconSalvar = PhotoImage(file=r"icons/IconSalvar.png").subsample(1, 1)
iconFechar = PhotoImage(file=r"icons/IconFechar.png").subsample(1, 1)
iconDilationValue = PhotoImage(file=r"icons/IconDilationValue.png").subsample(1, 1)
iconErosionValue = PhotoImage(file=r"icons/IconErosionValue.png").subsample(1, 1)
iconKernel1 = PhotoImage(file=r"icons/IconKernel1.png").subsample(1, 1)
iconKernel2 = PhotoImage(file=r"icons/IconKernel2.png").subsample(1, 1)
iconKernel3 = PhotoImage(file=r"icons/IconKernel3.png").subsample(1, 1)
iconKernel4 = PhotoImage(file=r"icons/IconKernel4.png").subsample(1, 1)
iconKernel1O = PhotoImage(file=r"icons/IconKernel1Orange.png").subsample(1, 1)
iconKernel2O = PhotoImage(file=r"icons/IconKernel2Orange.png").subsample(1, 1)
iconKernel3O = PhotoImage(file=r"icons/IconKernel3Orange.png").subsample(1, 1)
iconKernel4O = PhotoImage(file=r"icons/IconKernel4Orange.png").subsample(1, 1)
iconKernelTitle = PhotoImage(file=r"icons/IconKernelTitle.png").subsample(1, 1)
iconResete = PhotoImage(file=r"icons/IconResetar.png").subsample(1, 1)
iconManter = PhotoImage(file=r"icons/IconManter.png").subsample(1, 1)
iconSalvarO= PhotoImage(file=r"icons/IconSalvar0.png").subsample(1, 1)
iconManterO = PhotoImage(file=r"icons/IconManter0.png").subsample(1, 1)

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
                   width = 25,
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

# Tab 3 components

open_buttonTab3 = Button(
    tab3,
    bg="#15141B",
    command=select_file,
    image= iconimage,
    highlightbackground="#A177FE",
    bd=2,
    width = 75,
    height = 75,
    wraplength=250)

save_buttonTab3 = Button(
    tab3,
    bg="#15141B",
    command=saveImage,
    image= iconsave,
    highlightbackground = "#A177FE",
    bd=2,
    width = 75,
    height = 75,
    wraplength=250)

git_buttonTab3 = Button(
    tab3,
    bg="#15141B",
    command=opengit,
    image= icongit,
    highlightbackground = "#A177FE",
    bd=2,
    width = 75,
    height = 75,
    wraplength=250)

ImagePlaceLP = Label(tab3,
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

ValueBoostTab3 = Scale(tab3,
                   highlightbackground = "#A177FE",
                   bg="#15141B",
                   from_=1,
                   to=10,
                   fg="#A177FE",
                   font=('Crimson','12','bold'),
                   width = 25,
                   length = 297,
                   tickinterval = 1)

ValueBoostTab3.bind("<ButtonRelease-1>", lpImage)

# Tab 4 components

open_buttonTab4 = Button(
    tab4,
    bg="#15141B",
    command=select_file,
    image= iconimage,
    highlightbackground="#A177FE",
    bd=2,
    width = 75,
    height = 75,
    wraplength=250)

save_buttonTab4 = Button(
    tab4,
    bg="#15141B",
    command=saveImage,
    image= iconsave,
    highlightbackground = "#A177FE",
    bd=2,
    width = 75,
    height = 75,
    wraplength=250)

git_buttonTab4 = Button(
    tab4,
    bg="#15141B",
    command=opengit,
    image= icongit,
    highlightbackground = "#A177FE",
    bd=2,
    width = 75,
    height = 75,
    wraplength=250)

ImagePlaceHP = Label(tab4,
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

ValueBoostTab4 = Scale(tab4,
                   highlightbackground = "#A177FE",
                   bg="#15141B",
                   from_=1,
                   to=10,
                   fg="#A177FE",
                   font=('Crimson','12','bold'),
                   width = 25,
                   length = 297,
                   tickinterval = 1)

ValueBoostTab4.bind("<ButtonRelease-1>", hpImage)

# Tab 4 components

open_buttonTab5 = Button(
    tab5,
    bg="#15141B",
    command=select_file,
    image= iconimage,
    highlightbackground="#A177FE",
    bd=2,
    width = 75,
    height = 75,
    wraplength=250)

save_buttonTab5 = Button(
    tab5,
    bg="#15141B",
    command=saveImage,
    image= iconsave,
    highlightbackground = "#A177FE",
    bd=2,
    width = 75,
    height = 75,
    wraplength=250)

git_buttonTab5 = Button(
    tab5,
    bg="#15141B",
    command=opengit,
    image= icongit,
    highlightbackground = "#A177FE",
    bd=2,
    width = 75,
    height = 75,
    wraplength=250)

ImagePlaceBP = Label(tab5,
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

ValueBoostTab5Low = Scale(tab5,
                   highlightbackground = "#A177FE",
                   bg="#15141B",
                   from_=10,
                   to=5,
                   fg="#A177FE",
                   command=boostImage,
                   font=('Crimson','11','bold'),
                   width = 28,
                   length = 150,
                   tickinterval = 1)

ValueBoostTab5High = Scale(tab5,
                   highlightbackground = "#A177FE",
                   bg="#15141B",
                   from_=5,
                   to=10,
                   fg="#A177FE",
                   command=boostImage,
                   font=('Crimson','11','bold'),
                   width = 28,
                   length = 144,
                   tickinterval = 1)

ValueBoostTab5Low.bind("<ButtonRelease-1>", bpImage)
ValueBoostTab5High.bind("<ButtonRelease-1>", bpImage)

# Tab 6 components

open_buttonTab6 = Button(
    tab6,
    bg="#15141B",
    command=select_file,
    image= iconimage,
    highlightbackground="#A177FE",
    bd=2,
    width = 75,
    height = 75,
    wraplength=250)

save_buttonTab6 = Button(
    tab6,
    bg="#15141B",
    command=saveImage,
    image= iconsave,
    highlightbackground = "#A177FE",
    bd=2,
    width = 75,
    height = 75,
    wraplength=250)

git_buttonTab6 = Button(
    tab6,
    bg="#15141B",
    command=opengit,
    image= icongit,
    highlightbackground = "#A177FE",
    bd=2,
    width = 75,
    height = 75,
    wraplength=250)

ImagePlaceMorf = Label(tab6,
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

opcao_buttonTab6 = Button(
    tab6,
    bg="#15141B",
    command=openOpcoes,
    image=iconOpcao,
    highlightbackground="#A177FE",
    bd=2,
    width=75,
    height=55,
    wraplength=250)

erosao_buttonTab6 = Button(
    tab6,
    bg="#15141B",
    command=lambda: erosionOrdilation(1),
    image=iconErosao,
    highlightbackground="#A177FE",
    bd=2,
    width=75,
    height=57,
    wraplength=250)

dilatacao_buttonTab6 = Button(
    tab6,
    bg="#15141B",
    command=lambda: erosionOrdilation(2),
    image=iconDilatacao,
    highlightbackground="#A177FE",
    bd=2,
    width=75,
    height=55,
    wraplength=250)

abertura_buttonTab6 = Button(
    tab6,
    bg="#15141B",
    command=lambda: erosionOrdilation(3),
    image=iconAbertura,
    highlightbackground="#A177FE",
    bd=2,
    width=75,
    height=52,
    wraplength=250)

fechamento_buttonTab6 = Button(
    tab6,
    bg="#15141B",
    command=lambda: erosionOrdilation(4),
    image=iconFechamento,
    highlightbackground="#A177FE",
    bd=2,
    width=75,
    height=54,
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

#Organização do Layout por Grid - 3 Tab
ImagePlaceLP.grid(row = 1, column=1, sticky ='w', rowspan = 3)
open_buttonTab3.grid(row = 1, column=2, sticky ='nw')
ValueBoostTab3.grid(row = 1, column=2, sticky = 'nw', rowspan = 3, pady=81)
save_buttonTab3.grid(row = 3, column=2, sticky ='sw', pady=80)
git_buttonTab3.grid(row = 3, column=2, sticky ='sw')

#Organização do Layout por Grid - 4 Tab
ImagePlaceHP.grid(row = 1, column=1, sticky ='w', rowspan = 3)
open_buttonTab4.grid(row = 1, column=2, sticky ='nw')
ValueBoostTab4.grid(row = 1, column=2, sticky = 'nw', rowspan = 3, pady=81)
save_buttonTab4.grid(row = 3, column=2, sticky ='sw', pady=80)
git_buttonTab4.grid(row = 3, column=2, sticky ='sw')

#Organização do Layout por Grid - 5 Tab
ImagePlaceBP.grid(row = 1, column=1, sticky ='w', rowspan = 3)
open_buttonTab5.grid(row = 1, column=2, sticky ='nw')
ValueBoostTab5Low.grid(row = 1, column=2, sticky = 'nw', rowspan = 3, pady=81)
ValueBoostTab5High.grid(row = 2, column=2, sticky = 'nw', rowspan = 3, pady=81)
save_buttonTab5.grid(row = 3, column=2, sticky ='sw', pady=80)
git_buttonTab5.grid(row = 3, column=2, sticky ='sw')

#Organização do Layout por Grid - 6 Tab
ImagePlaceMorf.grid(row = 1, column=1, sticky ='w', rowspan = 3)
open_buttonTab6.grid(row = 1, column=2, sticky ='nw')
opcao_buttonTab6.grid(row = 1, column=2, sticky = 'nw', rowspan = 2, pady=81)
erosao_buttonTab6.grid(row = 2, column=2, sticky ='nw', pady=23)
abertura_buttonTab6.grid(row = 3, column=2, sticky = 'nw')
dilatacao_buttonTab6.grid(row = 2, column=2, sticky = 'sw')
fechamento_buttonTab6.grid(row = 3, column=2, sticky = 'nw', pady=58)
save_buttonTab6.grid(row = 3, column=2, sticky ='sw', pady=80)
git_buttonTab6.grid(row = 3, column=2, sticky ='sw')


#looping da janela
sist.mainloop()