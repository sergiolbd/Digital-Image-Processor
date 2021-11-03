import matplotlib.pyplot as plot
from PIL import Image
import numpy as np

def grayConversion(imarray):
    
    height, width, channel = imarray.shape

    #Creamos una nueva imagen con las dimensiones de la imagen anterior
    im2 = Image.new('RGB', (height, width))

    for i in range(0, height):
        for j in range(0, width):
            r = imarray[i][j][0]
            g = imarray[i][j][1]
            b = imarray[i][j][2]
            grayValue = r * 0.299 + g * 0.587 + b * 0.114
            gris = int(grayValue)
            imarray[i][j][0] = gris
            imarray[i][j][1] = gris
            imarray[i][j][2] = gris
            #gris = int(grayValue)
            #pixel = tuple([gris, gris, gris])
            #im2.putpixel((i,j), pixel)
    
    #imarray2 = np.asarray(im2)
    # print(imarray.shape)


    return imarray
    # plot.imshow(imarray, cmap='gray')
    # plot.show()