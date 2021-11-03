from PyQt5.QtWidgets import QMainWindow, QAction, qApp, QApplication, QFileDialog, QWidget
from openImage import SelectFileWindow
from PyQt5.QtGui import QPixmap, QImage
from PIL import Image
import numpy as np
import cv2 
import matplotlib.pyplot as plot


class basicMenubar(QMainWindow):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)        
        
        self.initUI()        
        
    def initUI(self):    
        
        self.setGeometry(400, 400, 400, 400)
        self.statusBar()

        openAction = QAction('&Open', self)        
        openAction.setShortcut('Ctrl+O')
        openAction.setStatusTip('Open Imagen')
        # openAction.triggered.connect(qApp.applicationFilePath) 
        openAction.triggered.connect(self.seleccionar_archivo)
                
        
        exitAction = QAction('&Exit', self)        
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(qApp.quit)

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(exitAction)
        fileMenu.addAction(openAction)

        #---------------------------------------------

        copyAction = QAction('&Copy', self)        
        copyAction.setShortcut('Ctrl+C')
        copyAction.setStatusTip('Copy Imagen')
        copyAction.triggered.connect(qApp.applicationFilePath)           
        
        ROIAction = QAction('&Region of Interest', self)        
        ROIAction.setShortcut('Ctrl+R')
        ROIAction.setStatusTip('Select a ROI in Image')
        ROIAction.triggered.connect(qApp.quit)

        menubar2 = self.menuBar()
        fileMenu2 = menubar2.addMenu('&Edit')
        fileMenu2.addAction(copyAction)
        fileMenu2.addAction(ROIAction)

        #---------------------------------------------

        showAction = QAction('&Show info', self)        
        showAction.setStatusTip('Show info Imagen')
        showAction.triggered.connect(qApp.applicationFilePath)           
        
        brightAction = QAction('&Brightness/Contranst', self)        
        brightAction.triggered.connect(qApp.quit)

        menubar3 = self.menuBar()
        fileMenu3 = menubar3.addMenu('&Image')
        fileMenu3.addAction(showAction)
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
        filename, ok = QFileDialog.getOpenFileName(self, 'Select Image...')
        
        #if filename.lower().endswith((".jpg", ".tif")) :
        #    img_png = Image.open(filename)
        #    img_png.save(filename, format="PNG")
        
        # Abre la imagen
        #im = Image.open(filename)
        #print(im.size, im.mode, im.format)
        #Extraemos el array de la imagen
        #imarray = np.asarray(im)
        #print(imarray.shape)
        # Convertimos array a imagen nuevamente
        #file = Image.fromarray(imarray)

        img = cv2.imread(filename) 
        rgb = np.asarray(img)
        # Mostramos en ventana externa donde permite ver la posición de cada pixel y su valor RGB
        cv2.imshow(filename, rgb)
        


        
# if __name__ == '__main__':
    
#     app = QApplication(sys.argv)
#     ex = basicMenubar()
#     sys.exit(app.exec_())

