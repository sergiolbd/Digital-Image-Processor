from PyQt5.QtWidgets import QMainWindow, QAction, qApp, QApplication, QFileDialog, QWidget, QMenu
from openImage import SelectFileWindow
from PyQt5.QtGui import QPixmap, QImage
from PIL import Image
import numpy as np
import cv2 
import matplotlib.pyplot as plot
from histogram import histogram
from newmonochrome import grayConversion


class basicMenubar(QMainWindow):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)        
        
        self.initUI() 
        self.openImages = []  # Rutas de imagenes abiertas
        self.openRgb = []   # RGB de cada imagen
        
    def initUI(self):    
        
        self.setGeometry(400, 400, 400, 400)
        self.statusBar()

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

        #---------------------------------------------

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

        #---------------------------------------------

        brightAction = QAction('&Brightness/Contranst', self)        
        brightAction.triggered.connect(qApp.quit)

        menubar3 = self.menuBar()
        fileMenu3 = menubar3.addMenu('&Image')
        new_submenu = QMenu('Histograma', self)
        
        # Histograma no acumulado
        submenu_noacumulado = QMenu('No acumulado', self)

        first_action = QAction('No normalizado', self)
        first_action.triggered.connect(self.abrirHistograma) 
        second_action = QAction('Normalizado', self)
        second_action.triggered.connect(self.abrirHistogramaN) 

        submenu_noacumulado.addAction(first_action)
        submenu_noacumulado.addAction(second_action)
        new_submenu.addMenu(submenu_noacumulado)

        # Histograma acumulado
        submenu_acum = QMenu('Acumulado', self)

        third_action = QAction('No normalizado', self)
        third_action.triggered.connect(self.abrirHistogramaA) 
        fourth_action = QAction('Normalizado', self)
        fourth_action.triggered.connect(self.abrirHistogramaNA) 
        
        submenu_acum.addAction(third_action)
        submenu_acum.addAction(fourth_action)
        new_submenu.addMenu(submenu_acum)
        
        fileMenu3.addMenu(new_submenu)
        fileMenu3.addAction(brightAction)
        
        #---------------------------------------------

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
        fileImage, ok = QFileDialog.getOpenFileName(self, 'Select Image...')
        self.openImages.append(fileImage)
        print(self.openImages[-1])
        imagen = cv2.imread(self.openImages[-1]) 
        self.openRgb.append(np.asarray(imagen))
        # Mostramos en ventana externa donde permite ver la posición de cada pixel y su valor RGB
        cv2.imshow(self.openImages[-1], self.openRgb[-1])
        
    def abrirHistograma(self):
        histogram(self.openImages[-1], False, False)

    def abrirHistogramaN(self):
        histogram(self.openImages[-1], True, False)

    def abrirHistogramaA(self):
        histogram(self.openImages[-1], False, True)

    def abrirHistogramaNA(self):
        histogram(self.openImages[-1], True, True)

    def blancoYnegro(self):
        pos = -1 # Imagen que se a seleccionado
        gray = grayConversion(self.openRgb[pos])

        cv2.imshow(self.openImages[pos] + 'gray', gray)
        



