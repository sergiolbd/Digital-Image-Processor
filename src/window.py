from os import name
from PyQt5 import QtCore
from PyQt5.QtGui import QCursor, QImage, QPixmap, QWindow
from PyQt5.QtWidgets import QDockWidget, QLabel, QWidget
import numpy as np
from PIL import Image
import cv2
from newmonochrome import grayConversion
from histogram import histogram
from contraste import contrast
from brightness import brightness


class Window(QWidget): # Añadir Qwindow para hacer el onClick

    def __init__(self, nameImage, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.nameImage = nameImage
        self.arrayImage = []
        self.arrayHist = []
        self.contrast = None
        self.brigthness = None
        self.main = None
        self.image = None
        self.format = "PNG"
    
    def newWindow(self, main):

        # Transformamos a PNG para que no pierda información
        if self.nameImage.lower().endswith((".jpg", ".tif")) :
            img_png = Image.open(self.nameImage)
            self.format = img_png.format
            img_png.save(self.nameImage, format="PNG")
            
        imge = cv2.imread(self.nameImage)
        imarray = np.asarray(imge)
        imarray = cv2.cvtColor(imarray, cv2.COLOR_BGR2RGB)
        
        self.showImage(main, imarray)
        self.setValues(imarray)

    def setValues(self, imarray):
        # Transformacion a escala de grises
        self.arrayImage = grayConversion(imarray)
        # Obtenemos el array del histograma
        self.arrayHist = histogram(self.arrayImage, True, True, False, self.nameImage) # False no mustra el histograma
        #
        self.brillo()
        #
        self.contraste()

    def showImage(self, main, arrayImage):
        self.main = main
        qimage = QImage(arrayImage, arrayImage.shape[1], arrayImage.shape[0], arrayImage.strides[0],                                                                                                                                                
                     QImage.Format_RGB888) 
        img = QLabel(self.nameImage)
        
        ## Mostrar posicion
        img.setMouseTracking(True)
        img.mouseMoveEvent = self.getPixel
        main.setFalse()
        main.windowsStatus.append(True)
        
        img.setPixmap(QPixmap.fromImage(qimage))
        self.image = qimage
        item = QDockWidget(self.nameImage, main)
        item.setWidget(img)
        item.mouseDoubleClickEvent = self.setStatus
        main.addDockWidget(QtCore.Qt.DockWidgetArea.LeftDockWidgetArea, item)
        
    def change(self, newBrightness, newContrast):
        A = newContrast / self.contrast
        B = newBrightness - (A * self.brightness)

        lut = [round(A * Vin + B) for Vin in range(256)]

        arrayResult = np.zeros([self.arrayImage.shape[0], self.arrayImage.shape[1], 3], np.uint8)

        for x in range(0, self.arrayImage.shape[0]): 
            for y in range(0, self.arrayImage.shape[1]): 
                Vout = lut[self.arrayImage[x][y][0]]
                if Vout < 0: Vout = 0
                if Vout > 255: Vout = 255
                arrayResult[x][y][0] = Vout
                arrayResult[x][y][1] = Vout
                arrayResult[x][y][2] = Vout

        return arrayResult

    def contraste(self):
        self.contrast = contrast(self.arrayHist, self.arrayImage.shape, self.brightness)
    
    def brillo(self):
        self.brightness = brightness(self.arrayHist, self.arrayImage.shape)
    
    def getName(self):
        return self.nameImage
    
    def getArray(self):
        return self.arrayImage

    def getHist(self):
        self.arrayHist = histogram(self.arrayImage, True, True, False, self.nameImage)
        return self.arrayHist

    def setName(self, nameImage):
        self.nameImage = nameImage

    def setArray(self, arrayImage):
        self.arrayImage = arrayImage
        
    def getPixel(self, event):
        x = event.x()
        y = event.y()
        if x < self.arrayImage.shape[1] and y < self.arrayImage.shape[0] and x >= 0 and y >= 0:
            self.main.statusBar().showMessage("X: " + str(x) + "    Y: " + str(y) + "   RGB:" + str(self.arrayImage[y][x]))

    def setStatus(self, event):
        self.main.setFalse()
        for i in range(len(self.main.windows)):
            if self.main.windows[i].getName() == self.nameImage:
                self.main.windowsStatus[i] = True
                
    def save(self, path):
        self.image.save(str(path))
        