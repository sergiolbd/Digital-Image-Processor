import matplotlib.pyplot as plot
import numpy as np
from histogram import histogram


def histogramEqualize(hist1, imarray1):
  # Obtenemos los histogramas acumulativos
  hist1 = acumulativo(hist1)
  
  m = 256
  # Creamos la LUT
  lut = []
  for i in range(m):
    cociente = hist1[i]/(imarray1.shape[0]*imarray1.shape[1])
    redondeo = round(cociente * m)
    result = max(0, redondeo-1)
    
    lut.append(result)
  
  # Convertimos la imagen 1 a la imagen 1 pero con histograma similar a la imagen de referencia
  arrayResult = np.zeros([imarray1.shape[0], imarray1.shape[1], 3], np.uint8)

  for x in range(0, imarray1.shape[0]): 
      for y in range(0, imarray1.shape[1]): 
          Vout = lut[imarray1[x][y][0]]
          if Vout < 0: Vout = 0
          if Vout > 255: Vout = 255
          arrayResult[x][y][0] = Vout
          arrayResult[x][y][1] = Vout
          arrayResult[x][y][2] = Vout

  return arrayResult


def acumulativo(hist):
  for i in range(256):
    if i-1 >= 0:
      hist[i] += hist[i-1]
    else:
      hist[i] = hist[i]

  return hist