# Calcular la entropía de una imagen

import math

def entropy(hist, size):
    # entropia = Representa el nº de bits mínimos para codificar la imagen
    
    height = size[0]
    width = size[1]
   
    sumatoriohist = 0
    entropia = 0

    for i in range(256):
      if hist[i] > 0:
        probabilidad_i = hist[i]/(height*width)
        if (probabilidad_i > 0):
          sumatoriohist +=  probabilidad_i * math.log2(probabilidad_i)

    entropia = -sumatoriohist

    if entropia < 0 or entropia > 8:
      return "Entropia erronea, fuera del rango [0,8]"

    return entropia