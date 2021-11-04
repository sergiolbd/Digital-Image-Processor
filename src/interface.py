from PyQt5 import QtCore
from PyQt5.QtWidgets import QDockWidget, QLabel, QMainWindow, QAction, qApp, QApplication, QFileDialog, QWidget, QMenu, QMessageBox
from openImage import SelectFileWindow
from PyQt5.QtGui import QPixmap, QImage
from PIL import Image
import numpy as np
import cv2 
import matplotlib.pyplot as plot
from histogram import histogram
from newmonochrome import grayConversion
from brightness import brightness
from contraste import contrast


class basicMenubar(QMainWindow):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)        
        
        self.initUI() 
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
        
        exitAction = QAction('&Exit', self)        
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(qApp.quit)

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(openAction)
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
        imagen = cv2.imread(self.openImages[-1])
        imarray = np.asarray(imagen)
        # Al abrir la imagen obtenemos su version B&W la cual se usará para todas las operaciones, y su hist
        self.gray.append(grayConversion(imarray))
        self.hist.append(histogram(self.gray[-1], True, True, False))
        # Mostramos en ventana externa donde permite ver la posición de cada pixel y su valor RGB
        cv2.imshow(self.openImages[-1], imarray)

        # imagen = QImage(self.openImages[-1])
        # img = QLabel(fileImage)
        # img.setPixmap(QPixmap.fromImage(imagen))
        # item = QDockWidget(fileImage, self)
        # item.setWidget(img)
        # self.addDockWidget(QtCore.Qt.DockWidgetArea.LeftDockWidgetArea, item)
        
    def abrirHistograma(self, normalized, cumulative):
        histogram(self.gray[-1], normalized, cumulative, True)

    def blancoYnegro(self):
        cv2.imshow(self.openImages[-1] + 'gray', self.gray[-1])

    def show_info(self):
        imarray = self.gray[-1]
        im = Image.open(self.openImages[-1])
        formato = "\nTipo fichero: " + im.format
        size = "\nTamaño: " + str(imarray.shape)
        ruta = "\nRuta:" + self.openImages[-1]
        
        # Obtener el menor y mayor pixel (con imarray[...,0] accedemos al primer canal)
        max = str(np.max(imarray[...,0]))
        min = str(np.min(imarray[...,0]))
        rango = "\nRango valores: ["+ min + "," + max + "]"

        brillo = brightness(self.hist[-1], imarray.shape)
        brillostr = "\nBrillo: " + str(brillo)
        contraste =  contrast(self.hist[-1], imarray.shape, brillo)
        contrastestr = "\nContraste: " + str(contraste)

        mensaje = ruta + formato + size + rango + brillostr + contrastestr
        QMessageBox.about(self, "Información de la imagen", mensaje)
        



