from os import name
from PyQt5 import QtCore
from PyQt5.QtGui import QImage, QPixmap, QWindow
from PyQt5.QtWidgets import QDockWidget, QLabel
import numpy as np
from PIL import Image
import cv2
from newmonochrome import grayConversion
from histogram import histogram
from contraste import contrast
from brightness import brightness


class Window(): # Añadir Qwindow para hacer el onClick

    def __init__(self, nameImage):
        self.nameImage = nameImage
        self.arrayImage = []
        self.arrayHist = []
        self.contrast = None
        self.brigthness = None
    
    def newWindow(self, main):

        # Transformamos a PNG para que no pierda información
        if self.nameImage.lower().endswith((".jpg", ".tif")) :
            img_png = Image.open(self.nameImage)
            img_png.save(self.nameImage, format="PNG")
            print('1')
            
        imge = cv2.imread(self.nameImage)
        imarray = np.asarray(imge)
        imarray = cv2.cvtColor(imarray, cv2.COLOR_BGR2RGB)
        self.showImage(main, imarray)
        self.setValues(imarray)

        print(self.brightness)
        print(self.contrast)
        new = Window('fisg')
        newArray = self.change(170, self.contrast)
        new.setValues(newArray)
        new.showImage(main, newArray)
        print(new.brightness)
        print(new.contrast)


    def setValues(self, imarray):
        # Transformacion a escala de grises
        self.arrayImage = grayConversion(imarray)
        # Obtenemos el array del histograma
        self.arrayHist = histogram(self.arrayImage, True, True, False) # False no mustra el histograma
        #
        self.brillo()
        #
        self.contraste()


    def showImage(self, main, arrayImage):

        qimage = QImage(arrayImage, arrayImage.shape[1], arrayImage.shape[0], arrayImage.strides[0],                                                                                                                                                
                     QImage.Format_RGB888) 
        img = QLabel(self.nameImage)
        img.setPixmap(QPixmap.fromImage(qimage))
        item = QDockWidget(self.nameImage, main)
        item.setWidget(img)
        main.addDockWidget(QtCore.Qt.DockWidgetArea.LeftDockWidgetArea, item)

    def change(self, newBrightness, newContrast):
        # Hacer la LUT
        # Se necesita la A y la B 
        # A = contraste nuevo / contraste anterior
        A = newContrast / self.contrast
        B = newBrightness - (A * self.brightness)

        lut = [round(A * Vin + B) for Vin in range(256)]

        arrayResult = np.zeros([self.arrayImage.shape[0], self.arrayImage.shape[1], 3], np.uint8)

        for x in range(0, self.arrayImage.shape[0]): 
            for y in range(0, self.arrayImage.shape[1]): 
                Vout = lut[self.arrayImage[x][y][0]]
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
        return self.arrayHist

    def setName(self, nameImage):
        self.nameImage = nameImage

    def setArray(self, arrayImage):
        self.arrayImage = arrayImage
