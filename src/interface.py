import math
from PyQt5.QtCore import Qt
from PyQt5 import QtGui
from PyQt5.QtWidgets import QDockWidget, QLabel, QMainWindow, QAction, qApp, QApplication, QFileDialog, QWidget, QMenu, QMessageBox, QInputDialog, QSlider, QHBoxLayout
from PyQt5.QtGui import QPixmap, QImage, QWindowStateChangeEvent
from PIL import Image
import numpy as np

import matplotlib.pyplot as plot
from numpy.lib.function_base import append
from histogram import histogram
from newmonochrome import grayConversion
from brightness import brightness
from contraste import contrast
from entropia import entropy
from sections_linear_tansformations import sectionsLinearTrasformations
from specificationHistogram import histogramSpecification
from ecualizehistogram import histogramEqualize
from gammaCorrection import correctionGamma
from imageDifference import imageDifference
from window import Window
from slider import Slider
import cv2

class basicMenubar(QMainWindow):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)        
        self.windowsStatus = []
        self.windows = []
        
        self.initUI() 
        
    def initUI(self):    
        
        self.setGeometry(400, 400, 400, 400)
        self.statusBar()

        #------------------File---------------------------

        openAction = QAction('&Open', self)        
        openAction.setShortcut('Ctrl+O')
        openAction.setStatusTip('Open Imagen')
        openAction.triggered.connect(self.seleccionar_archivo)
        
        saveAction = QAction('&Save', self)        
        saveAction.setShortcut('Ctrl+S')
        saveAction.setStatusTip('Save Imagen')
        saveAction.triggered.connect(self.save_image)

        exitAction = QAction('&Exit', self)        
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(qApp.quit)

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(openAction)
        fileMenu.addAction(saveAction)
        fileMenu.addAction(exitAction)

        #-------------------Edit--------------------------

        copyAction = QAction('&Black', self)        
        copyAction.setStatusTip('Blanco y negro')
        copyAction.triggered.connect(self.blancoYnegro)           
        
        ROIAction = QAction('&Region of Interest', self)        
        ROIAction.setShortcut('Ctrl+R')
        ROIAction.setStatusTip('Select a ROI in Image')
        ROIAction.triggered.connect(self.selectROI)

        # Transformaciones lineales
        new_submenu2 = QMenu('Transformaciones lineales', self)
        brillo_contraste = QAction('Brillo/Contraste', self)
        brillo_contraste.triggered.connect(self.brightnessContrast)
        portramos = QAction('Por tramos', self)
        portramos.triggered.connect(self.sections)


        new_submenu2.addAction(brillo_contraste)
        new_submenu2.addAction(portramos)

        # Transformaciones no lineales
        new_submenu3 = QMenu('Transformaciones no lineales', self)
        esp_hist = QAction('Especificación del histograma', self)
        esp_hist.triggered.connect(self.specification)
        ecualizacion = QAction('Ecualización del histograma', self)
        ecualizacion.triggered.connect(self.equalize)
        gamma = QAction('Corrección Gamma', self)
        gamma.triggered.connect(self.gammaCorrection)
        difference = QMenu('Diferencia de imágenes', self)
        distribution = QAction('Distribución de valores', self)
        distribution.triggered.connect(self.distributionValues)
        changeMap = QAction('Mapa de cambios', self)
        changeMap.triggered.connect(self.changeMap)
        
        new_submenu3.addAction(esp_hist)
        new_submenu3.addAction(ecualizacion)
        new_submenu3.addAction(gamma)
        difference.addAction(distribution)
        difference.addAction(changeMap)
        new_submenu3.addMenu(difference)

        menubar2 = self.menuBar()
        fileMenu2 = menubar2.addMenu('&Edit')
        fileMenu2.addAction(copyAction)
        fileMenu2.addAction(ROIAction)
        fileMenu2.addMenu(new_submenu2)
        fileMenu2.addMenu(new_submenu3)

        #--------------------Image-------------------------

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
        self.newImagen(fileImage)
        for x in self.windows: print(x.getName())
        
    def save_image(self):
        indice = self.windowsStatus.index(True)
        path, ok = QFileDialog.getSaveFileName(self, "Guardar imagen", "default", "Images(*.jpg *.png *.bmp)")
        self.windows[indice].save(path)
            
    def abrirHistograma(self, normalized, cumulative):
        indice = self.windowsStatus.index(True)
        histogram(self.windows[indice].getArray(), normalized, cumulative, True, self.windows[indice].getName())

    def blancoYnegro(self):
        indice = self.windowsStatus.index(True)
        self.windows.append(self.windows[indice])
        ###### Cambiar nombre de la imagen
        self.windows[indice].showImage(self, self.windows[indice].getArray())

    def show_info(self):
        indice = self.windowsStatus.index(True)
        imarray = self.windows[indice].getArray()
        formato = "\nTipo imagen: " + self.windows[indice].format
        size = "\nTamaño: " + str(imarray.shape)
        ruta = "\nRuta:" + self.windows[indice].getName()
        
        # Obtener el menor y mayor pixel (con imarray[...,0] accedemos al primer canal)
        max = str(np.max(imarray[...,0]))
        min = str(np.min(imarray[...,0]))
        rango = "\nRango valores: ["+ min + "," + max + "]"

        brillo = brightness(self.windows[indice].getHist(), imarray.shape)
        brillostr = "\nBrillo: " + str(brillo)
        contraste =  contrast(self.windows[indice].getHist(), imarray.shape, brillo)
        contrastestr = "\nContraste: " + str(contraste)
        entropia = entropy(self.windows[indice].getHist(), imarray.shape)
        entropiastr = "\nEntropia: " + str(entropia)
        numofbits = math.ceil(entropia)
        numofbitsstr = "\nNº de bits: " + str(numofbits)

        mensaje = ruta + formato + size + rango + brillostr + contrastestr + entropiastr + numofbitsstr
        QMessageBox.about(self, "Información de la imagen", mensaje)

    def brightnessContrast(self):
        Slider(self)
        
    # Intentando hacer una selección de una region de interes sin necesidad del raton
    def selectROI(self):
        indice = self.windowsStatus.index(True)
        imarray = self.windows[indice].getArray()
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

        newRoi = Window(self.windows[indice].getName() + '_ROI') ## Revisar para poner bien el nombre
        newRoi.setArray(imarray2)
        self.windows.append(newRoi)
        self.windows[-1].showImage(self, imarray2)
        self.windows[-1].setValues(imarray2)

    def newImagen(self, nameImage):
        new = Window(nameImage)
        new.newWindow(self)
        self.windows.append(new)

    def sections(self):
        indice = self.windowsStatus.index(True)
        numofsections, ok = QInputDialog.getInt(self, "Number of sections ", "numofsections:", 1, 0, 5)
        points = []
        x = []
        y = []
        for i in range(1,numofsections+1):
            x1, ok = QInputDialog.getInt(self, "Tramo {} : x1".format(i), "x1:", 1, 0, 255)
            y1, ok = QInputDialog.getInt(self, "Tramo {} : y1".format(i), "y1:", 1, 0, 255)
            x2, ok = QInputDialog.getInt(self, "Tramo {} : x2".format(i), "x2:", 1, 0, 255)
            y2, ok = QInputDialog.getInt(self, "Tramo {} : y2".format(i), "y2:", 1, 0, 255)
            points.append(((x1,y1), (x2,y2)))
            x.append(x1)
            x.append(x2)
            y.append(y1)
            y.append(y2)

        # Mostrar los tramos introducidos
        fig, ax = plot.subplots()
        ax.plot(x, y)
        plot.show()

        imarray2 = sectionsLinearTrasformations(self.windows[indice].getArray(), numofsections, points)
        
        newsection = Window(self.windows[indice].getName() + '_Sections') ## Revisar para poner bien el nombre
        newsection.setArray(imarray2)
        self.windows.append(newsection)
        self.windows[-1].showImage(self, imarray2)
        self.windows[-1].setValues(imarray2)

    def specification(self):###################### Revisar como poner los indices
        imarray2 = histogramSpecification(
                                            self.windows[-2].getHist(),
                                            self.windows[-1].getHist(), 
                                            self.windows[-2].getArray(),
                                            self.windows[-1].getArray())

        newsection = Window(self.windows[-2].getName() + '_specification') ## Revisar para poner bien el nombre
        newsection.setArray(imarray2)
        self.windows.append(newsection)
        self.windows[-1].showImage(self, imarray2)
        self.windows[-1].setValues(imarray2)

    def equalize(self):
        indice = self.windowsStatus.index(True)
        imarray2 = histogramEqualize(self.windows[indice].getHist(), self.windows[indice].getArray())

        newsection = Window(self.windows[indice].getName() + '_equalize') ## Revisar para poner bien el nombre
        newsection.setArray(imarray2)
        self.windows.append(newsection)
        self.windows[-1].showImage(self, imarray2)
        self.windows[-1].setValues(imarray2)

    def gammaCorrection(self):
        indice = self.windowsStatus.index(True)
        gammaValue, ok = QInputDialog.getDouble(self, "Gamma Value ", "Y:", 1.00, 1/20, 20, 2)

        imarray2 = correctionGamma(self.windows[indice].getHist(), self.windows[indice].getArray(), gammaValue)

        newsection = Window(self.windows[indice].getName() + '_Gamma') ## Revisar para poner bien el nombre
        newsection.setArray(imarray2)
        self.windows.append(newsection)
        self.windows[-1].showImage(self, imarray2)
        self.windows[-1].setValues(imarray2)

    def changeMap(self): ##################### Revisar para poder el indice
        T, ok = QInputDialog.getInt(self, "T", "T:", 1, 0, 255)

        imarray2 = imageDifference(self.windows[-2].getArray(), self.windows[-1].getArray(), T, False)

        newsection = Window(self.windows[-1].getName() + 'Diference') ## Revisar para poner bien el nombre
        newsection.setArray(imarray2)
        self.windows.append(newsection)
        self.windows[-1].showImage(self, imarray2)
        self.windows[-1].setValues(imarray2)

    def distributionValues(self):  ##################### Revisar para poder el indice
        imageDifference(self.windows[-2].getArray(), self.windows[-1].getArray(), 0, True)
               
    # Pone como no principales todas las ventanas
    def setFalse(self):
        for i in range(len(self.windowsStatus)):
            self.windowsStatus[i] = False