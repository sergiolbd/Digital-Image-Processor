import matplotlib.pyplot as plot
import numpy as np
from histogram import histogram


def correctionGamma(hist1, imarray1, gammaValue):

  m = 256
  a = []
  # Escalado lineal de Vin en el intervalo [0,1]
  for i in range(m):
    a.append(i/255)

  b = []
  # Aplicación de la función gamma al valor a para obtener b en [0,1]
  for i in range(m):
    b.append(a[i]**gammaValue)

  lut = []
  # Escalado de los valores de b a Vout en el intervalo permitido [0,255]
  for i in range(m):
    lut.append(round(b[i] * 255))
  
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