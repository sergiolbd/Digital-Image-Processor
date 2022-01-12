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
  imarray2 = np.zeros([sizeY, sizeX, channel], np.uint8)

  # Contador para el número de pixeles que se van fuera
  count = 0

  print(E0, F0, G0, H0)
  print(T)

  # for indiceX in range(0, sizeX):
  #   for indiceY in range(0, sizeY):

  #     x0 = indiceX + T[0]
  #     y0 = indiceY + T[1]

  #     P0 = np.array([round(x0, 2), round(y0, 2)])

  #     [x, y] = np.dot(R(-angle), P0)
  #     x = round(x, 2)
  #     y = round(y, 2)

  #     if x >= width or x < 0 or y >= height or y < 0:
  #       imarray2[indiceY][indiceX] = 255
  #       count += 1
  #     else:
  #       imarray2[indiceY][indiceX] = 0

  for indiceX in range(0, width):
    for indiceY in range(0, height):

      P0 = np.array([indiceX, indiceY])

      [x0, y0] = np.dot(R(angle), P0)
      x0 = x0 - T[0]
      y0 = y0 - T[1]
      x0 = round(x0)
      y0 = round(y0)

      # if imarray2[y0][x0][0] == 255:
      if x0 >= width or x0 < 0 or y0 >= height or y0 < 0:
        imarray2[y0][x0] = 255
        count += 1
      else: 
        imarray2[y0][x0] = imarray[indiceY][indiceX]

      # Para comparar histogramas si pusimos el fondo a negro, este histrograma se obtiene obteniendo el histograma y restando al
      # indice 0 del histograma el valor del contador Z

  return imarray2


def R(angle):
  radianes = (angle * pi) / 180
  r = np.array([[cos(radianes), -sin(radianes)],
                [sin(radianes), cos(radianes)]])
  return r