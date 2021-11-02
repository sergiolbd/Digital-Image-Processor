# Cáculo del brillo a partir del histograma de la imagen

from matplotlib.pyplot import hist


def brightness(hist, size):
    # Brillo = media
    
    height = size[0]
    width = size[1]

   
    sumatoriohist = 0

    for i in range(256):
      sumatoriohist += hist[i]

    brillo = (1/(height*width)) * sumatoriohist

    return brillo
