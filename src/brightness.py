# Cáculo del brillo a partir del histograma de la imagen

def brightness(hist, size):
    # Brillo = media
    
    height = size[0]
    width = size[1]
   
    sumatoriohist = 0

    for i in range(256):
      sumatoriohist += hist[i] * i

    brillo = (1/(height*width)) * sumatoriohist

    if brillo < 0 or brillo > 255:
      return "Brillo erroneo, fuera del rango [0,255]"

    return round(brillo,3)
