import matplotlib.pyplot as plot
from PIL import Image
import numpy as np

def rotate(imarray):
    
  height, width, channel = imarray.shape
  imarray2 = np.zeros([width, height, channel], np.uint8)


  for i in range(0, width):
    for j in range(0, height):
      imarray2[i][j] = imarray[height-1-j][i]

  return imarray2