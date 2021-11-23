from PyQt5.QtGui import QWindow
from PyQt5.QtWidgets import QApplication, QMainWindow, QSlider, QWidget, QLabel, QHBoxLayout
from PyQt5.QtCore import Qt

class Example(QWidget):

    def __init__(self, main):
        super().__init__(main, Qt.WindowType.Window)

        hbox = QHBoxLayout()

        mySlider = QSlider(Qt.Orientation.Horizontal, self)
        mySlider.setRange(0,255)
        mySlider.valueChanged[int].connect(self.changeBright)
        mySlider.value[int].c

        self.label = QLabel('0', self)
        self.label.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
        self.label.setMinimumWidth(80)

        mySlider2 = QSlider(Qt.Orientation.Horizontal, self)
        mySlider2.setRange(0,127)
        mySlider2.valueChanged[int].connect(self.changeContrast)

        self.label2 = QLabel('0', self)
        self.label2.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
        self.label2.setMinimumWidth(80)

        hbox.addWidget(mySlider)
        hbox.addSpacing(10)
        hbox.addWidget(self.label)

        hbox.addWidget(mySlider2)
        hbox.addSpacing(10)
        hbox.addWidget(self.label2)

        self.setLayout(hbox)

        self.setGeometry(50,50,320,200)
        self.setWindowTitle("Brillo & Contraste")
        self.show()

    def changeBright(self, value):
      self.label.setText(str(value))
      # print(value)

    def changeContrast(self, value):
      self.label2.setText(str(value))
      # print(value)
