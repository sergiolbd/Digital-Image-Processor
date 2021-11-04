# Cáculo del contraste a partir del histograma de la imagen

import math

def contrast(hist, size, brillo):
    # Contraste = desviación típica
    height = size[0]
    width = size[1]

    sumatoriohist = 0

    for i in range(256):
      sumatoriohist += hist[i] * (i - brillo)**2

    contraste = (1/(height*width)) * sumatoriohist

    contraste = math.sqrt(contraste)

    return round(contraste,3)