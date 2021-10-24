from PIL import Image
import matplotlib.pyplot as plot

def histogram(image, normalized):
  # #Abrimos la Imagen
  im = Image.open(image)
  rgb_im = im.convert('RGB')

  #Obtenemos sus dimensiones
  x = im.size[0]
  y = im.size[1]

  hist = [0 for i in range(256)]
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

  if normalized == False: 
     # print(hist)
    plot.bar(eje_x, hist)
    plot.xlabel('[0-255]')
    plot.ylabel('Frecuencia absoluta')
    plot.title('Histrograma' + image)
    plot.show()

  else: 
    #Normalizar el histograma
    for i in range(256):
      hist[i] = hist[i]/(x*y)

    # print(hist)

    # A partir de aquí preguntar como construir el histograma usando el array hist[] que contiene las frecuencias relativas

    plot.bar(eje_x, hist)
    plot.xlabel('[0-255]')
    plot.ylabel('Frecuencia absoluta')
    plot.title('Histrograma normalizado' + image)
    plot.show()
