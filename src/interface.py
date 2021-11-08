import math
from PyQt5 import QtCore
from PyQt5.QtWidgets import QDockWidget, QLabel, QMainWindow, QAction, qApp, QApplication, QFileDialog, QWidget, QMenu, QMessageBox, QInputDialog
from PyQt5.QtGui import QPixmap, QImage
from PIL import Image
import numpy as np

import matplotlib.pyplot as plot
from numpy.lib.function_base import append
from histogram import histogram
from newmonochrome import grayConversion
from brightness import brightness
from contraste import contrast
from entropia import entropy
from window import Window
import cv2



class basicMenubar(QMainWindow):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)        
        
        self.initUI() 
        self.windows = []
        #self.windows2 = ("name": window) /// self.windows2["nombre ventana"] = window
        self.openImages = []  # Rutas de imagenes abiertas
        self.openRgb = []   # RGB de cada imagen
        self.hist = []
        self.gray = [] # Lista para almacenar el array de la imagen en blanco y negro
        
    def initUI(self):    
        
        self.setGeometry(400, 400, 400, 400)
        self.statusBar()

        #------------------File---------------------------

        openAction = QAction('&Open', self)        
        openAction.setShortcut('Ctrl+O')
        openAction.setStatusTip('Open Imagen')
        openAction.triggered.connect(self.seleccionar_archivo)

        ROIAction = QAction('&ROI', self)        
        ROIAction.setShortcut('Ctrl+R')
        ROIAction.setStatusTip('Select region of interest')
        ROIAction.triggered.connect(self.selectROI)
        
        exitAction = QAction('&Exit', self)        
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(qApp.quit)

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(openAction)
        fileMenu.addAction(ROIAction)
        fileMenu.addAction(exitAction)

        #-------------------Edit--------------------------

        copyAction = QAction('&Black', self)        
        copyAction.setStatusTip('Blanco y negro')
        copyAction.triggered.connect(self.blancoYnegro)           
        
        ROIAction = QAction('&Region of Interest', self)        
        ROIAction.setShortcut('Ctrl+R')
        ROIAction.setStatusTip('Select a ROI in Image')
        ROIAction.triggered.connect(qApp.quit)

        menubar2 = self.menuBar()
        fileMenu2 = menubar2.addMenu('&Edit')
        fileMenu2.addAction(copyAction)
        fileMenu2.addAction(ROIAction)

        #--------------------Image-------------------------

        brightAction = QAction('&Brightness/Contranst', self)        
        brightAction.triggered.connect(qApp.quit)

        infoAction = QAction('&Información', self)
        infoAction.setStatusTip('Mostrar información sobre la imagen')
        infoAction.triggered.connect(self.show_info)

        menubar3 = self.menuBar()
        fileMenu3 = menubar3.addMenu('&Image')
        new_submenu = QMenu('Histograma', self)
        
        # Histograma no acumulado
        submenu_noacumulado = QMenu('No acumulado', self)

        first_action = QAction('No normalizado', self)
        first_action.triggered.connect(lambda:self.abrirHistograma(False, False)) 
        second_action = QAction('Normalizado', self)
        second_action.triggered.connect(lambda:self.abrirHistograma(True, False)) 

        submenu_noacumulado.addAction(first_action)
        submenu_noacumulado.addAction(second_action)
        new_submenu.addMenu(submenu_noacumulado)

        # Histograma acumulado
        submenu_acum = QMenu('Acumulado', self)

        third_action = QAction('No normalizado', self)
        third_action.triggered.connect(lambda:self.abrirHistograma(False, True)) 
        fourth_action = QAction('Normalizado', self)
        fourth_action.triggered.connect(lambda:self.abrirHistograma(True, True)) 
        
        submenu_acum.addAction(third_action)
        submenu_acum.addAction(fourth_action)
        new_submenu.addMenu(submenu_acum)
        
        fileMenu3.addMenu(new_submenu)
        fileMenu3.addAction(infoAction)
        fileMenu3.addAction(brightAction)
        
        #--------------------Help-------------------------

        aboutAction = QAction('&About', self)        
        aboutAction.triggered.connect(qApp.quit)

        menubar4 = self.menuBar()
        fileMenu4 = menubar4.addMenu('&Help')
        fileMenu4.addAction(aboutAction)

        #---------------------------------------------
        
        self.setWindowTitle('Procesamiento digital de imágenes')    
        self.show()

    def seleccionar_archivo(self):
        # Obtenemos la ruta de la image a abrir
        fileImage, ok = QFileDialog.getOpenFileName(self, 'Select Image...', "../Images/")
        self.openImages.append(fileImage)
        
        self.newImagen(fileImage)
            
    def abrirHistograma(self, normalized, cumulative):
        histogram(self.windows[-1].getArray(), normalized, cumulative, True)

    def blancoYnegro(self):
        self.windows.append(self.windows[-1])
        ###### Cambiar nombre de la imagen
        self.windows[-1].showImage(self, self.windows[-1].getArray())

    def show_info(self):
        imarray = self.windows[-1].getArray()
        im = Image.open(self.openImages[-1])
        formato = "\nTipo fichero: " + im.format
        size = "\nTamaño: " + str(imarray.shape)
        ruta = "\nRuta:" + self.windows[-1].getName()
        
        # Obtener el menor y mayor pixel (con imarray[...,0] accedemos al primer canal)
        max = str(np.max(imarray[...,0]))
        min = str(np.min(imarray[...,0]))
        rango = "\nRango valores: ["+ min + "," + max + "]"

        brillo = brightness(self.windows[-1].getHist(), imarray.shape)
        brillostr = "\nBrillo: " + str(brillo)
        contraste =  contrast(self.windows[-1].getHist(), imarray.shape, brillo)
        contrastestr = "\nContraste: " + str(contraste)
        entropia = entropy(self.windows[-1].getHist(), imarray.shape)
        entropiastr = "\nEntropia: " + str(entropia)
        numofbits = math.ceil(entropia)
        numofbitsstr = "\nNº de bits: " + str(numofbits)

        mensaje = ruta + formato + size + rango + brillostr + contrastestr + entropiastr + numofbitsstr
        QMessageBox.about(self, "Información de la imagen", mensaje)

    # Intentando hacer una selección de una region de interes sin necesidad del raton
    def selectROI(self):
        imarray = self.windows[-1].getArray()
        maxX = imarray.shape[0]
        maxY = imarray.shape[1]
        x1, ok = QInputDialog.getInt(self, "x1", "x1:", 1, 0, maxX)
        y1, ok = QInputDialog.getInt(self, "y1", "y1:", 1, 0, maxY)
        x2, ok = QInputDialog.getInt(self, "x2", "x2:", 1, 0, maxX)
        y2, ok = QInputDialog.getInt(self, "y2", "y2:", 1, 0, maxY)

        imarray2 = np.zeros([x2-x1, y2-y1, 3], np.uint8)
        
        # Recorremos la imagen y generamos una nueva con la región
        k = 0
        for i in range(x1, x2):
            l = 0
            for j in range(y1, y2):
                imarray2[k][l][0] = imarray[i][j][0]
                imarray2[k][l][1] = imarray[i][j][1]
                imarray2[k][l][2] = imarray[i][j][2]
                l += 1
            k += 1

        newRoi = Window(self.windows[-1].getName() + '_ROI') ## Revisar para poner bien el nombre
        newRoi.setArray(imarray2)
        self.windows.append(newRoi)
        self.windows[-1].showImage(self, imarray2)
        self.windows[-1].setValues(imarray2)

    def newImagen(self, nameImage):
        new = Window(nameImage)
        new.newWindow(self)
        self.windows.append(new)
        
        



