import matplotlib.pyplot as plot
from PIL import Image
import numpy as np

def grayConversion(imarray):
    
    height, width, channel = imarray.shape
    
    imarray2 = np.zeros(imarray.shape, np.uint8)

    for i in range(0, height):
        for j in range(0, width):
            r = imarray[i][j][0]
            g = imarray[i][j][1]
            b = imarray[i][j][2]
            grayValue = r * 0.299 + g * 0.587 + b * 0.114
            gris = int(round(grayValue))
            imarray2[i][j][0] = gris
            imarray2[i][j][1] = gris
            imarray2[i][j][2] = gris

    return imarray2
  