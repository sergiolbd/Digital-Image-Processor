from PyQt5.QtGui import QWindow
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QSlider, QWidget, QLabel, QVBoxLayout, qApp
from PyQt5.QtCore import Qt
from window import Window

class Slider(QWidget):

    def __init__(self, main):
        super().__init__(main, Qt.WindowType.Window)

        hbox = QVBoxLayout()

        self.main = main

        self.labelBright = QLabel('Brillo', self)
        self.labelBright.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
        self.labelBright.setMinimumWidth(80)

        self.mySlider = QSlider(Qt.Orientation.Horizontal, self)
        self.mySlider.setRange(0,255)
        self.mySlider.valueChanged[int].connect(self.changeBright)

        self.label = QLabel('0', self)
        self.label.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
        self.label.setMinimumWidth(80)

        self.labelContrast = QLabel('Contraste', self)
        self.labelContrast.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
        self.labelContrast.setMinimumWidth(80)

        self.mySlider2 = QSlider(Qt.Orientation.Horizontal, self)
        self.mySlider2.setRange(0,127)
        self.mySlider2.valueChanged[int].connect(self.changeContrast)

        self.label2 = QLabel('0', self)
        self.label2.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
        self.label2.setMinimumWidth(80)

        hbox.addWidget(self.labelBright)
        hbox.addWidget(self.mySlider)
        hbox.addSpacing(10)
        hbox.addWidget(self.label)

        hbox.addWidget(self.labelContrast)
        hbox.addWidget(self.mySlider2)
        hbox.addSpacing(10)
        hbox.addWidget(self.label2)

        # Crear botón
        self.pushButton = QPushButton("Aceptar")
        self.pushButtonExit = QPushButton("Salir")

        self.pushButton.clicked.connect(self.calculate) #Añadir un evento de clic para el botón
        self.pushButtonExit.clicked.connect(self.exit)

        hbox.addWidget(self.pushButton)
        hbox.addWidget(self.pushButtonExit)

        self.setLayout(hbox)

        self.setGeometry(50,50,320,200)
        self.setWindowTitle("Brillo & Contraste")
        self.show()

    def changeBright(self, value):
      self.label.setText(str(value))

    def changeContrast(self, value):
      self.label2.setText(str(value))

    def exit(self):
      self.close()

    def calculate(self):
      indice = self.main.windowsStatus.index(True)
      newBrightness = self.mySlider.value()
      newContrast = self.mySlider2.value()
      newArray = self.main.windows[indice].change(newBrightness, newContrast)
      
      newRoi = Window(self.main.windows[indice].getName() + '_new')
      newRoi.setArray(newArray)
      self.main.windows.append(newRoi)
      self.main.windows[-1].showImage(self.main, newArray)
      self.main.windows[-1].setValues(newArray)