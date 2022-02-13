import matplotlib.pyplot as plot
from PIL import Image
import numpy as np

def flip(imarray, flag):
    
  height, width, channel = imarray.shape

  # Flip Horizontal
  if flag == 'H':
    imarray2 = np.zeros(imarray.shape, np.uint8)
    for i in range(0, height):
      imarray2[i] = np.flip(imarray[i])
  elif flag == 'V': # Flip vertical 
    imarray2 = np.zeros(imarray.shape, np.uint8)
    for i in range(0, height):
      imarray2[i] = imarray[height-1]
      height -= 1
  elif flag == 'T': # Traspuesta
    shape = [width, height, channel]
    imarray2 = np.zeros(shape, np.uint8)
    for i in range(0, height):
      for j in range(0, width):
        imarray2[j][i] = imarray[i][j][0]
   

  return imarray2
  