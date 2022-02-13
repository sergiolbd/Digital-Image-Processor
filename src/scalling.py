from math import trunc
import matplotlib.pyplot as plot
from PIL import Image
import numpy as np

def scallingTransform(imarray, new_height, new_width, flag):
    
  height, width, channel = imarray.shape
  imarray2 = np.zeros([new_height, new_width, 3], np.uint8)
  
  cambioX = new_width / width 
  cambioY = new_height / height

  if flag == True:
    # Vecino más próximo
    for x in range(0, new_width):
      for y in range(0, new_height):
        oldX = x / cambioX
        oldY = y / cambioY

        ## Prueba ---------- repasar porque puede que al redondear se nos salga del limite
        oldX = round(oldX)
        oldY = round(oldY)
        if oldX >= width:
          oldX -= 1
        if oldY >= height:
          oldY -= 1
   
        imarray2[y][x] = imarray[oldY][oldX]
  else:
    # Interpolación bilineal
    for x in range(0, new_width):
      for y in range(0, new_height):
        newX = x / cambioX
        newY = y / cambioY

        oldX = trunc(newX)
        oldY = trunc(newY)

        p = newX - oldX
        q = newY - oldY

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
      
        imarray2[y][x] = np.uint8(pp)

  return imarray2
  