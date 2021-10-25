from itertools import accumulate
from PIL import Image
import matplotlib.pyplot as plot

def histogram(image, normalized, cumulative):
  # #Abrimos la Imagen
  im = Image.open(image)
  rgb_im = im.convert('RGB')

  #Obtenemos sus dimensiones
  x = im.size[0]
  y = im.size[1]

  hist = [0 for i in range(256)]
  histNormalized = [0 for i in range(256)]

  eje_x = range(256)

  i = 0
  while i < x:
      j = 0
      while j < y:
          #Obtenemos el valor RGB de cada pixel
          r, g, b = rgb_im.getpixel((i,j))
          #Accedemos a la posición r del array hist y aumentamos en 1, realizando un contador del número de pixeles con dicho tono
          hist[r] += 1
          j += 1
      i += 1

  #Normalizar el histograma
  for i in range(256):
    histNormalized[i] = hist[i]/(x*y)
  

  if normalized == False and cumulative == False: 

    plot.bar(eje_x, hist)
    plot.xlabel('[0-255]')
    plot.ylabel('Frecuencia absoluta')
    plot.title('Histrograma' + image)
    plot.show()

  elif normalized == True and cumulative == False: 

    plot.bar(eje_x, histNormalized)
    plot.xlabel('[0-255]')
    plot.ylabel('Frecuencia absoluta')
    plot.title('Histrograma normalizado' + image)
    plot.show()

  elif normalized == False and cumulative == True: 
 
    for i in range(256):
      if i-1 >= 0:
        hist[i] += hist[i-1]
      else:
          hist[i] = hist[i]

    plot.bar(eje_x, hist)
    plot.xlabel('[0-255]')
    plot.ylabel('Frecuencia absoluta')
    plot.title('Histrograma acumulado' + image)
    plot.show()

  elif normalized == True and cumulative == True: 
   
    for i in range(256):
      if i-1 > 0:
        histNormalized[i] += histNormalized[i-1]
      else:
          histNormalized[i] = histNormalized[i]


    plot.bar(eje_x, histNormalized)
    plot.xlabel('[0-255]')
    plot.ylabel('Frecuencia absoluta')
    plot.title('Histrograma normalizado acumulado' + image)
    plot.show()