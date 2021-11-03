import sys
from PyQt5.QtWidgets import QApplication
from interface import basicMenubar
from openImage import SelectFileWindow
 

if __name__ == '__main__':
    app = QApplication(sys.argv)
    # a = basicMenubar()
    # b = SelectFileWindow()
    # a
    ex = basicMenubar()
    sys.exit(app.exec_())
