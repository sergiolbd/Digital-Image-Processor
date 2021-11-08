from os import name
from PyQt5 import QtCore
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QDockWidget, QLabel
import numpy as np
from PIL import Image
import cv2
from newmonochrome import grayConversion
from histogram import histogram


class Window():

    def __init__(self, nameImage):
        self.nameImage = nameImage
        self.arrayImage = []
        self.arrayHist = []
    
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

    def setValues(self, imarray):
        # Transformacion a escala de grises
        self.arrayImage = grayConversion(imarray)
        # Obtenemos el array del histograma
        self.arrayHist = histogram(self.arrayImage, True, True, False) # False no mustra el histograma

    def showImage(self, main, arrayImage):

        qimage = QImage(arrayImage, arrayImage.shape[1], arrayImage.shape[0], arrayImage.strides[0],                                                                                                                                                
                     QImage.Format_RGB888) 
        img = QLabel(self.nameImage)
        img.setPixmap(QPixmap.fromImage(qimage))
        item = QDockWidget(self.nameImage, main)
        item.setWidget(img)
        main.addDockWidget(QtCore.Qt.DockWidgetArea.LeftDockWidgetArea, item)

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
