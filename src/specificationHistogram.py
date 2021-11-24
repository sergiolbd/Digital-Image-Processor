# Especificación del histograma
# Obtener histograma de la imagen abierta
# Abrir otra imagen cualquiera
# Obtener histograma de la nueva imagen
# Obtener la nueva imagen de referencia cuyo histograma debe ser similar a la imagen de referencia
 
import matplotlib.pyplot as plot
import numpy as np
from histogram import histogram


def histogramSpecification(hist1, histR, imarray1, imarrayR, name):
  # Normalizar los histogramas
  hist1 = normalizar(hist1, imarray1)
  histR = normalizar(histR, imarrayR)

  # Obtenemos los histogramas acumulativos
  hist1 = acumulativo(hist1)
  histR = acumulativo(histR)
  
  m = 256
  # Creamos la LUT
  lut = []
  for i in range(m):
    lut.append(i)

  # Igualamos histogramas
  for a in range(m-1):
    j = m-1
    while True:
      lut[a] = j
      j -= 1
      if (hist1[a] >= histR[j]) or (j <= 0):
        break
    
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

  # histresult = histogram(arrayResult, False, False, False, name)
  # histresult = acumulativo(histresult)
  # histresult = normalizar(histresult, imarray1)

  return arrayResult

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