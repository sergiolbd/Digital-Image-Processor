from itertools import accumulate
from PIL import Image
import matplotlib.pyplot as plot

def histogram(imagearray, normalized, cumulative, show, name):
  x, y, z = imagearray.shape

  hist = [0 for i in range(256)]
  histNormalized = [0 for i in range(256)]

  eje_x = range(256)

  i = 0
  while i < x:
      j = 0
      while j < y:
          #Obtenemos el valor RGB de cada pixel
          r = imagearray[i][j][0]
          #Accedemos a la posición r del array hist y aumentamos en 1, realizando un contador del número de pixeles con dicho tono
          hist[r] += 1
          j += 1
      i += 1

  #Normalizar el histograma
  for i in range(256):
    histNormalized[i] = hist[i]/(x*y)
  
  # Añadidos esta opción para mostrarlo solo cuando queramos 
  if show == True:

    if normalized == False and cumulative == False: 

      plot.figure(name + "Normal")
      plot.bar(eje_x, hist)
      plot.xlabel('Vin[0-255]')
      plot.ylabel('h(i)')
      plot.title('Histograma')
      plot.show()
      

    elif normalized == True and cumulative == False: 

      plot.figure(name + "Normalizado")
      plot.bar(eje_x, histNormalized)
      plot.xlabel('Vin[0-255]')
      plot.ylabel('h(i)')
      plot.title('Histograma normalizado')
      plot.show()

    elif normalized == False and cumulative == True: 
  
      for i in range(256):
        if i-1 >= 0:
          hist[i] += hist[i-1]
        else:
          hist[i] = hist[i]

      plot.figure(name + "Acumulado")
      plot.bar(eje_x, hist)
      plot.xlabel('Vin[0-255]')
      plot.ylabel('h(i)')
      plot.title('Histograma acumulado')
      plot.show()

    elif normalized == True and cumulative == True: 
    
      for i in range(256):
        if i - 1 > 0:
          histNormalized[i] += histNormalized[i - 1]
        else:
            histNormalized[i] = histNormalized[i]

      plot.figure(name + "Normalizado & Acumulado")
      plot.bar(eje_x, histNormalized)
      plot.xlabel('Vin[0-255]')
      plot.ylabel('h(i)')
      plot.title('Histograma normalizado acumulado')
      plot.show()

  return hist