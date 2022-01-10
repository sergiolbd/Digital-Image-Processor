from math import cos, pi, sin, ceil, trunc
import matplotlib.pyplot as plot
from PIL import Image
import numpy as np

def rotation(imarray, angle, flag):
    
  height, width, channel = imarray.shape
  
  # Paso 1: Aplicar transformación directa de coordenadas
  r = R(angle)
 
  E = [0, 0]
  F = [width-1, 0]
  G = [width-1, height-1]
  H = [0, height-1]

  # print(E, F, G, H)

  E0 = np.dot(r, E)
  F0 = np.dot(r, F)
  G0 = np.dot(r, G)
  H0 = np.dot(r, H)

  # print(E0, F0, G0, H0)

  # Determinar dimensiones del rectángulo que circunscribe a la versión rotada
  maxX = max([E0[0], F0[0], G0[0], H0[0]])
  minX = min([E0[0], F0[0], G0[0], H0[0]])
  sizeX = ceil(abs(maxX-minX))
  maxY = max([E0[1], F0[1], G0[1], H0[1]])
  minY = min([E0[1], F0[1], G0[1], H0[1]])
  sizeY = ceil(abs(maxY-minY))

  # print(sizeX, sizeY)

  # Valor de la traslación T(Tx, Ty)
  T = [minX, minY]

  # print(T)

  # Asignar nivel de gris a los indices del array usando interpolacion del vecino más próximo
  imarray2 = np.zeros([sizeY, sizeX, channel], np.uint8)

  # Contador para el número de pixeles que se van fuera
  count = 0

  for indiceX in range(0, sizeX):
    for indiceY in range(0, sizeY):

      x0 = indiceX + T[0]
      y0 = indiceY + T[1]

      P0 = np.array([round(x0, 2), round(y0, 2)])

      # if indiceX == 20 and indiceY == 50: 
      #   print(P0)

      [x, y] = np.dot(R(-angle), P0)
      x = round(x, 2)
      y = round(y, 2)


      # if indiceX == 20 and indiceY == 50: 
      #   print(x, y)

      # HASTA AQUI FUNCIONA TODO IGUAL QUE EN LA ULTIMA TRANSPARENCIA DE LOS APUNTES

      # Contador para los x,y de la imagen original que den x', y' de la imagen rotada, cuyos x,y esten fuera de
      # de la imagen original

      # Si x o y esta fuera de la imagen original => se el asigna color fondo = negro
      if x >= width or x < 0 or y >= height or y < 0:
        imarray2[indiceY][indiceX] = 255
        count += 1
      elif flag == True: 
        # Vecino más próximo
        oldX = round(x)
        oldY = round(y)
        if oldX >= width:
          oldX -= 1
        if oldY >= height:
          oldY -= 1
    
        imarray2[indiceY][indiceX] = imarray[oldY][oldX]
      elif flag == False: 
        # Bilineal
        oldX = trunc(x)
        oldY = trunc(y)

        p = x - oldX
        q = y - oldY

        c = int(imarray[oldY][oldX][0])

        if oldX+1 <= width-1 and oldY+1 <= height-1:
          a = int(imarray[oldY+1][oldX][0])
          b = int(imarray[oldY+1][oldX+1][0])
          d = int(imarray[oldY][oldX+1][0])
        elif oldX+1 > width-1 and oldY+1 > height-1:
          a = 0
          b = 0
          d = 0
        elif oldX+1 > width-1:
          b = 0
          d = 0
          a = int(imarray[oldY+1][oldX][0])
        elif oldY+1 > height-1:
          a = 0
          b = 0
          d = int(imarray[oldY][oldX+1][0])
        
        pp = c + (d - c) * p + (a - c) * q + (b + c - a - d) * p * q
      
        imarray2[indiceY][indiceX] = np.uint8(pp)

      # Para comparar histogramas si pusimos el fondo a negro, este histrograma se obtiene obteniendo el histograma y restando al
      # indice 0 del histograma el valor del contador 

  return imarray2


def R(angle):
  radianes = (angle * pi) / 180
  r = np.array([[cos(radianes), -sin(radianes)],
                [sin(radianes), cos(radianes)]])
  return r