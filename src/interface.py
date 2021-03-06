import math
from PyQt5.QtWidgets import QMainWindow, QAction, qApp, QFileDialog, QMenu, QMessageBox, QInputDialog
import numpy as np

import matplotlib.pyplot as plot
from drawRotation import drawRotation
from histogram import histogram
from horizontally import flip
from newmonochrome import grayConversion
from brightness import brightness
from contraste import contrast
from entropia import entropy
from rotate import rotate
from rotation import rotation
from scalling import scallingTransform
from sections_linear_tansformations import sectionsLinearTrasformations
from specificationHistogram import histogramSpecification
from ecualizehistogram import histogramEqualize
from gammaCorrection import correctionGamma
from imageDifference import imageDifference
from window import Window
from slider import Slider

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
        new_submenu2 = QMenu('Linear transformations', self)
        brillo_contraste = QAction('Brillo/Contraste', self)
        brillo_contraste.triggered.connect(self.brightnessContrast)
        portramos = QAction('Por tramos', self)
        portramos.triggered.connect(self.sections)


        new_submenu2.addAction(brillo_contraste)
        new_submenu2.addAction(portramos)

        # Transformaciones no lineales
        new_submenu3 = QMenu('Nonlinear transformations', self)
        esp_hist = QAction('Especificaci??n del histograma', self)
        esp_hist.triggered.connect(self.specification)
        ecualizacion = QAction('Ecualizaci??n del histograma', self)
        ecualizacion.triggered.connect(self.equalize)
        gamma = QAction('Correcci??n Gamma', self)
        gamma.triggered.connect(self.gammaCorrection)
        difference = QMenu('Diferencia de im??genes', self)
        distribution = QAction('Distribuci??n de valores/Imagen diferencia', self)
        distribution.triggered.connect(self.distributionValues)
        changeMap = QAction('Mapa de cambios', self)
        changeMap.triggered.connect(self.changeMap)
        
        new_submenu3.addAction(esp_hist)
        new_submenu3.addAction(ecualizacion)
        new_submenu3.addAction(gamma)
        difference.addAction(distribution)
        difference.addAction(changeMap)
        new_submenu3.addMenu(difference)

        # Transformaciones
        new_submenu4 = QMenu('Transform', self)
        horizontally = QAction('Flip Horizontally', self)
        horizontally.triggered.connect(self.flipHorizontally)
        vertically = QAction('Flip Vertically', self)
        vertically.triggered.connect(self.flipVertically)
        transposed = QAction('Transposed', self)
        transposed.triggered.connect(self.transposed)
        new_submenu5 = QMenu('Rotate', self)
        rotate90 = QAction('90??', self)
        rotate90.triggered.connect(lambda:self.rotate(90))
        rotate180 = QAction('180??', self)
        rotate180.triggered.connect(lambda:self.rotate(180))
        rotate270 = QAction('270??', self)
        rotate270.triggered.connect(lambda:self.rotate(270))
        new_submenu5.addAction(rotate90)
        new_submenu5.addAction(rotate180)
        new_submenu5.addAction(rotate270)

        new_submenu4.addAction(horizontally)
        new_submenu4.addAction(vertically)
        new_submenu4.addAction(transposed)
        new_submenu4.addMenu(new_submenu5)

        # Transformaci??n de escalado
        new_submenu6 = QMenu('Scalling transformations', self)
        neighbor = QAction('Interpolaci??n del vecino m??s pr??ximo', self)
        neighbor.triggered.connect(lambda:self.scalling(True))
        bilinear = QAction('Interpolaci??n bilineal', self)
        bilinear.triggered.connect(lambda:self.scalling(False))

        new_submenu6.addAction(neighbor)
        new_submenu6.addAction(bilinear)

        # Transformaciones de rotaci??n
        new_submenu7 = QMenu('Rotation transformations', self)
        rotate = QMenu('Rotate', self)
        rotateNeighbor = QAction('Vecino m??s pr??ximo', self)
        rotateNeighbor.triggered.connect(lambda:self.rotationTransformation(True))
        rotateBilinear = QAction('Bilineal', self)
        rotateBilinear.triggered.connect(lambda:self.rotationTransformation(False))
        drawAndRotate = QAction('Rotar y Pintar', self)
        drawAndRotate.triggered.connect(self.drawRotate)

        new_submenu7.addMenu(rotate)
        rotate.addAction(rotateNeighbor)
        rotate.addAction(rotateBilinear)
        new_submenu7.addAction(drawAndRotate)
 

        menubar2 = self.menuBar()
        fileMenu2 = menubar2.addMenu('&Edit')
        fileMenu2.addAction(copyAction)
        fileMenu2.addAction(ROIAction)
        fileMenu2.addMenu(new_submenu2)
        fileMenu2.addMenu(new_submenu3)
        fileMenu2.addMenu(new_submenu4)
        fileMenu2.addMenu(new_submenu6)
        fileMenu2.addMenu(new_submenu7)

        #--------------------Image-------------------------

        infoAction = QAction('&Informaci??n', self)
        infoAction.setStatusTip('Mostrar informaci??n sobre la imagen')
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
        
        self.setWindowTitle('Procesamiento digital de im??genes')    
        self.show()

    def seleccionar_archivo(self):
        # Obtenemos la ruta de la image a abrir
        fileImage, ok = QFileDialog.getOpenFileName(self, 'Select Image...', "../Images/")
        self.newImagen(fileImage)
        
    def save_image(self):
        indice = self.windowsStatus.index(True)
        path, ok = QFileDialog.getSaveFileName(self, "Guardar imagen", "default", "Images(*.jpg *.png *.bmp)")
        self.windows[indice].save(path)
            
    def abrirHistograma(self, normalized, cumulative):
        indice = self.windowsStatus.index(True)
        histogram(self.windows[indice].getArray(), normalized, cumulative, True, self.windows[indice].getName())

    def blancoYnegro(self):
        indice = self.windowsStatus.index(True)
        new = Window(self.windows[indice].getName() + "BN" + str(len(self.windows)))
        new.setArray(self.windows[indice].getArray)
        self.windows.append(new)
        self.windows[-1].showImage(self, self.windows[indice].getArray())
        self.windows[-1].setValues(self.windows[indice].getArray())

    def show_info(self):
        indice = self.windowsStatus.index(True)
        imarray = self.windows[indice].getArray()
        formato = "\nTipo imagen: " + self.windows[indice].format
        size = "\nTama??o: " + str(imarray.shape)
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
        numofbitsstr = "\nN?? de bits: " + str(numofbits)

        mensaje = ruta + formato + size + rango + brillostr + contrastestr + entropiastr + numofbitsstr
        QMessageBox.about(self, "Informaci??n de la imagen", mensaje)

    def brightnessContrast(self):
        Slider(self)
        
    # Selecci??n de una region de interes sin necesidad del raton
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
        
        # Recorremos la imagen y generamos una nueva con la regi??n
        k = 0
        for i in range(x1, x2):
            l = 0
            for j in range(y1, y2):
                imarray2[k][l][0] = imarray[i][j][0]
                imarray2[k][l][1] = imarray[i][j][1]
                imarray2[k][l][2] = imarray[i][j][2]
                l += 1
            k += 1

        newRoi = Window(self.windows[indice].getName() + '_ROI' + str(len(self.windows)))
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
        x1, ok = QInputDialog.getInt(self, "Tramo {} : x1".format(1), "x1:", 1, 0, 255)
        y1, ok = QInputDialog.getInt(self, "Tramo {} : y1".format(1), "y1:", 1, 0, 255)
        x2, ok = QInputDialog.getInt(self, "Tramo {} : x2".format(1), "x2:", 1, 0, 255)
        y2, ok = QInputDialog.getInt(self, "Tramo {} : y2".format(1), "y2:", 1, 0, 255)
        points.append(((x1,y1), (x2,y2)))
        x.append(x1)
        x.append(x2)
        y.append(y1)
        y.append(y2)
        for i in range(2,numofsections+1):
            x1 = x[-1]
            y1 = y[-1]
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
        
        newsection = Window(self.windows[indice].getName() + '_Sections' + str(len(self.windows))) 
        newsection.setArray(imarray2)
        self.windows.append(newsection)
        self.windows[-1].showImage(self, imarray2)
        self.windows[-1].setValues(imarray2)

    def specification(self):
        # Extraccion de las imagenes
        indice = self.windowsStatus.index(True)
        image1 = self.windows[indice]
        fileImage, ok = QFileDialog.getOpenFileName(self, 'Select Image...', "../Images/")
        self.newImagen(fileImage)
        image2 = self.windows[-1]
        
        imarray2 = histogramSpecification(
                                            image1.getHist(),
                                            image2.getHist(), 
                                            image1.getArray(),
                                            image2.getArray(),
                                            image1.getName())

        newsection = Window(image1.getName() + '_specification') 
        newsection.setArray(imarray2)
        self.windows.append(newsection)
        self.windows[-1].showImage(self, imarray2)
        self.windows[-1].setValues(imarray2)

    def equalize(self):
        indice = self.windowsStatus.index(True)
        imarray2 = histogramEqualize(self.windows[indice].getHist(), self.windows[indice].getArray())

        newsection = Window(self.windows[indice].getName() + '_equalize' + str(len(self.windows)))
        newsection.setArray(imarray2)
        self.windows.append(newsection)
        self.windows[-1].showImage(self, imarray2)
        self.windows[-1].setValues(imarray2)

    def gammaCorrection(self):
        indice = self.windowsStatus.index(True)
        gammaValue, ok = QInputDialog.getDouble(self, "Gamma Value ", "Y:", 1.00, 1/20, 20, 2)

        imarray2 = correctionGamma(self.windows[indice].getHist(), self.windows[indice].getArray(), gammaValue)

        newsection = Window(self.windows[indice].getName() + '_Gamma' + str(len(self.windows)))
        newsection.setArray(imarray2)
        self.windows.append(newsection)
        self.windows[-1].showImage(self, imarray2)
        self.windows[-1].setValues(imarray2)

    def changeMap(self): 
        # Extraccion de las imagenes
        indice = self.windowsStatus.index(True)
        image1 = self.windows[indice]
        fileImage, ok = QFileDialog.getOpenFileName(self, 'Select Image...', "../Images/")
        self.newImagen(fileImage)
        image2 = self.windows[-1]
        
        T, ok = QInputDialog.getInt(self, "T", "T:", 1, 0, 255)
        
        imarray2 = imageDifference(image1.getArray(), image2.getArray(), T, False)

        newsection = Window(self.windows[indice].getName() + 'MapaCambios' + str(len(self.windows)))
        newsection.setArray(imarray2)
        self.windows.append(newsection)
        self.windows[-1].showImage(self, imarray2)
        self.windows[-1].setValues(imarray2)

    def distributionValues(self):
        # Extraccion de las imagenes
        indice = self.windowsStatus.index(True)
        image1 = self.windows[indice]
        fileImage, ok = QFileDialog.getOpenFileName(self, 'Select Image...', "../Images/")
        self.newImagen(fileImage)
        image2 = self.windows[-1]
        
        imarray2 = imageDifference(image1.getArray(), image2.getArray(), 0, True)
        newsection = Window(self.windows[indice].getName() + 'Diference' + str(len(self.windows)))
        newsection.setArray(imarray2)
        self.windows.append(newsection)
        self.windows[-1].showImage(self, imarray2)
        self.windows[-1].setValues(imarray2)
               
    # Pone como no principales todas las ventanas
    def setFalse(self):
        for i in range(len(self.windowsStatus)):
            self.windowsStatus[i] = False


            # ------------------------------- Pr??ctica 2 ------------------------------
    def flipHorizontally(self):
        indice = self.windowsStatus.index(True)

        imarray2 = flip(self.windows[indice].getArray(), 'H')
        
        newsection = Window(self.windows[indice].getName() + 'Flip Horizontally' + str(len(self.windows))) 
        newsection.setArray(imarray2)
        self.windows.append(newsection)
        self.windows[-1].showImage(self, imarray2)
        self.windows[-1].setValues(imarray2)

    def flipVertically(self):
        indice = self.windowsStatus.index(True)

        imarray2 = flip(self.windows[indice].getArray(), 'V')
        
        newsection = Window(self.windows[indice].getName() + 'Flip Vertically' + str(len(self.windows))) 
        newsection.setArray(imarray2)
        self.windows.append(newsection)
        self.windows[-1].showImage(self, imarray2)
        self.windows[-1].setValues(imarray2)

    def transposed(self):
        indice = self.windowsStatus.index(True)

        imarray2 = flip(self.windows[indice].getArray(), 'T')
        
        newsection = Window(self.windows[indice].getName() + 'Transposed' + str(len(self.windows))) 
        newsection.setArray(imarray2)
        self.windows.append(newsection)
        self.windows[-1].showImage(self, imarray2)
        self.windows[-1].setValues(imarray2) 

    def rotate(self, degree):
        indice = self.windowsStatus.index(True)

        if degree == 90:
            imarray2 = rotate(self.windows[indice].getArray())
        elif degree == 180:
            imarray2 = rotate(self.windows[indice].getArray())
            imarray2 = rotate(imarray2)
        elif degree == 270:
            imarray2 = rotate(self.windows[indice].getArray())
            imarray2 = rotate(imarray2)
            imarray2 = rotate(imarray2)        

        newsection = Window(self.windows[indice].getName() + 'Transposed' + str(len(self.windows))) 
        newsection.setArray(imarray2)
        self.windows.append(newsection)
        self.windows[-1].showImage(self, imarray2)
        self.windows[-1].setValues(imarray2) 

    def scalling(self, flag):
        indice = self.windowsStatus.index(True)
        imarray = self.windows[indice].getArray()
        x = imarray.shape[1]
        y = imarray.shape[0]

        width, ok = QInputDialog.getInt(self, "Size x", "X:", x, 0, x * 5)
        height, ok = QInputDialog.getInt(self, "Size y", "Y:", y, 0, y * 5)

        imarray2 = scallingTransform(self.windows[indice].getArray(), height, width, flag)
        
        newsection = Window(self.windows[indice].getName() + 'Scalling Transform' + str(len(self.windows))) 
        newsection.setArray(imarray2)
        self.windows.append(newsection)
        self.windows[-1].showImage(self, imarray2)
        self.windows[-1].setValues(imarray2) 
    
    def rotationTransformation(self, flag):
        indice = self.windowsStatus.index(True)

        angle, ok = QInputDialog.getInt(self, "Rotate", "Angle:", -360, 0, 360)

        imarray2 = rotation(self.windows[indice].getArray(), angle, flag)
        
        newsection = Window(self.windows[indice].getName() + 'Rotation Transformation' + str(len(self.windows))) 
        newsection.setArray(imarray2)
        self.windows.append(newsection)
        self.windows[-1].showImage(self, imarray2)
        self.windows[-1].setValues(imarray2) 

    def drawRotate(self):
        indice = self.windowsStatus.index(True)

        angle, ok = QInputDialog.getInt(self, "Rotate", "Angle:", -360, 0, 360)

        imarray2 = drawRotation(self.windows[indice].getArray(), angle)
        
        newsection = Window(self.windows[indice].getName() + 'Rotation Transformation' + str(len(self.windows))) 
        newsection.setArray(imarray2)
        self.windows.append(newsection)
        self.windows[-1].showImage(self, imarray2)
        self.windows[-1].setValues(imarray2)
