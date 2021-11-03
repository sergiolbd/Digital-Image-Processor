import sys
from PyQt5.QtWidgets import QApplication, QFileDialog, QLabel, QMainWindow, QPushButton
from PyQt5.QtGui import QPixmap

class SelectFileWindow(QMainWindow):
  def __init__(self):
    super().__init__()

    self.inicializarGui()

  def inicializarGui(self):
    self.setWindowTitle('Select File')
    self.setFixedSize(400, 500)

    btn_seleccionar_archivo = QPushButton('Select File...', self) # Crear un boton para buscar
    btn_seleccionar_archivo.move(30, 20) # Posición del botón
    btn_seleccionar_archivo.setFixedWidth(340)
    btn_seleccionar_archivo.clicked.connect(self.seleccionar_archivo)

    self.lbl_imagen = QLabel('', self)
    self.lbl_imagen.move(30, 40)
    self.lbl_imagen.setFixedWidth(340)
    self.lbl_imagen.setFixedHeight(340)

    self.lbl_imagen = QLabel('', self)
    self.lbl_imagen.move(30, 40)
    self.lbl_imagen.setFixedWidth(340)
    self.lbl_imagen.setFixedHeight(340)

  def seleccionar_archivo(self):
        archivo, ok = QFileDialog.getOpenFileName(self, 'Select Image...')
        if ok:
            self.lbl_imagen.setPixmap(QPixmap(archivo))



def main():
    app = QApplication(sys.argv)
    ventana = SelectFileWindow()
    ventana.show()

    sys.exit(app.exec_())

if __name__ == "__main__":
    main()