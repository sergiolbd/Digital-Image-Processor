import matplotlib.pyplot as plot
import numpy as np
from histogram import histogram

def imageDifference(imarray1, imarray2, T, Flag):

  arrayResult = np.zeros([imarray1.shape[0], imarray1.shape[1], 3], np.uint8)

  if (imarray1.shape[0] == imarray2.shape[0] and imarray1.shape[1] == imarray2.shape[1]):

    for x in range(0, imarray1.shape[0]): 
      for y in range(0, imarray1.shape[1]): 
          Vout = abs(imarray1[x][y][0] - imarray2[x][y][0])
          arrayResult[x][y][0] = abs(Vout)
          arrayResult[x][y][1] = abs(Vout)
          arrayResult[x][y][2] = abs(Vout)


  if (Flag == True):
    histresult = histogram(arrayResult, False, False, False, "Distribución de valores")
    printhist(histresult)
  else:
    for x in range(0, imarray1.shape[0]): 
      for y in range(0, imarray1.shape[1]): 
          if (arrayResult[x][y][0] > T):
            imarray1[x][y][0] = 255
            imarray1[x][y][1] = 0
            imarray1[x][y][2] = 0

    return imarray1


# Función para imprimir los dos histogramas que deberían de ser iguales
def printhist(hist1):
  eje_x = range(256)
  plot.bar(eje_x, hist1)
  plot.xlabel('[0-255]')
  plot.ylabel('Frecuencia absoluta')
  plot.title('Histograma')
  plot.show()