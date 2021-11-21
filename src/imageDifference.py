import matplotlib.pyplot as plot
import numpy as np
from histogram import histogram


def imageDifference(imarray1, imarray2):

  arrayResult = np.zeros([imarray1.shape[0], imarray1.shape[1], 3], np.uint8)

  if (imarray1.shape[0] == imarray2.shape[0] and imarray1.shape[1] == imarray2.shape[1]):

    for x in range(0, imarray1.shape[0]): 
      for y in range(0, imarray1.shape[1]): 
          Vout = abs(imarray1[x][y][0] - imarray2[x][y][0])
          arrayResult[x][y][0] = abs(Vout)
          arrayResult[x][y][1] = abs(Vout)
          arrayResult[x][y][2] = abs(Vout)

    histresult = histogram(arrayResult, False, False, False)

    printhist(histresult)

  return arrayResult


# Función para imprimir los dos histogramas que deberían de ser iguales
def printhist(hist1):
  eje_x = range(256)
  plot.bar(eje_x, hist1)
  plot.xlabel('[0-255]')
  plot.ylabel('Frecuencia absoluta')
  plot.title('Histograma')
  plot.show()


def normalizar(hist, imarray):
  for i in range(256):
    hist[i] = hist[i]/(imarray.shape[0]*imarray.shape[1])

  return hist

def acumulativo(hist):
  for i in range(256):
    if i-1 >= 0:
      hist[i] += hist[i-1]
    else:
      hist[i] = hist[i]

  return hist