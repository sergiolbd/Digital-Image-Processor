from math import cos, pi, sin, ceil
import matplotlib.pyplot as plot
from PIL import Image
import numpy as np

def rotation(imarray, angle):
    
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

  for indiceX in range(0, sizeX+1):
    for indiceY in range(0, sizeY+1):

      x0 = indiceX + T[0]
      y0 = indiceY + T[1]

      P0 = np.array([round(x0, 2), round(y0, 2)])

      [x, y] = np.dot(R(-angle), P0)
      x = round(x, 2)
      y = round(y, 2)

      # if indiceX == 20 and indiceY == 50: 
      #   print(x, y)

      # HASTA AQUI FUNCIONA TODO IGUAL QUE EN LA ULTIMA TRANSPARENCIA DE LOS APUNTES
      # Para la imagen 321x201 y angulo 37

      # Si x o y esta fuera de la imagen original => se el asigna color fondo = negro
      if x >= width or x < 0 or y >= height or y < 0:
        imarray2[indiceX][indiceY] = 255
      else: 
        # Vecino más próximo
          cambioX = sizeX / width 
          cambioY = sizeY / height
          oldX = x / cambioX
          oldY = y / cambioY

          oldX = round(oldX)
          oldY = round(oldY)
          if oldX >= width:
            oldX -= 1
          if oldY >= height:
            oldY -= 1
      
          imarray2[indiceX][indiceY] = imarray[oldY][oldX]

  return imarray2


def R(angle):
  radianes = (angle * pi) / 180
  r = np.array([[cos(radianes), -sin(radianes)],
                [sin(radianes), cos(radianes)]])
  return r