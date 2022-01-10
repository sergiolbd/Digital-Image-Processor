from math import cos, pi, sin, ceil
import matplotlib.pyplot as plot
from PIL import Image
import numpy as np

def drawRotation(imarray, angle):
    
  height, width, channel = imarray.shape
  
  # Paso 1: Aplicar transformación directa de coordenadas
  r = R(angle)
 
  E = [0, 0]
  F = [width-1, 0]
  G = [width-1, height-1]
  H = [0, height-1]

  E0 = np.dot(r, E)
  F0 = np.dot(r, F)
  G0 = np.dot(r, G)
  H0 = np.dot(r, H)

  # Determinar dimensiones del rectángulo que circunscribe a la versión rotada
  maxX = max([E0[0], F0[0], G0[0], H0[0]])
  minX = min([E0[0], F0[0], G0[0], H0[0]])
  sizeX = ceil(abs(maxX-minX))
  maxY = max([E0[1], F0[1], G0[1], H0[1]])
  minY = min([E0[1], F0[1], G0[1], H0[1]])
  sizeY = ceil(abs(maxY-minY))

  # Valor de la traslación T(Tx, Ty)
  T = [minX, minY]

  # Asignar nivel de gris a los indices del array usando interpolacion del vecino más próximo
  imarray2 = np.zeros([sizeX+1, sizeY+1, channel], np.uint8)

  # Contador para el número de pixeles que se van fuera
  count = 0

  for indiceX in range(0, width):
    for indiceY in range(0, height):
      P0 = np.array([indiceX, indiceY])

      [x, y] = np.dot(R(angle), P0)
      x = round(x)
      y = round(y)

      if x >= width or x < 0 or y >= height or y < 0:
        imarray2[x][y] = 255
        count += 1
      else: 
        imarray2[x][y] = imarray[indiceX][indiceY]

      # Para comparar histogramas si pusimos el fondo a negro, este histrograma se obtiene obteniendo el histograma y restando al
      # indice 0 del histograma el valor del contador 

  return imarray2


def R(angle):
  radianes = (angle * pi) / 180
  r = np.array([[cos(radianes), -sin(radianes)],
                [sin(radianes), cos(radianes)]])
  return r