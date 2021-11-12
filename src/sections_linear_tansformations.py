import numpy as np

# Transformación lienal por tramos

def sectionsLinearTrasformations(arrayImage, numofsections, x):
  

  lut = []
  # Obtener pendiente de las rectas
  for i in range(numofsections): 
    m = (x[i][1][1] - x[i][0][1]) / (x[i][1][0] - x[i][0][0])
    n = x[i][0][1] - m * x[i][0][0]
    
    # Cuando estemos en el tramo final debemos de sumarle una posición para rellenar la LUT completa
    if i == numofsections-1:
      inicialrange = x[i][0][0]
      endrange = x[i][1][0] + 1
    else:
      inicialrange = x[i][0][0]
      endrange = x[i][1][0]
    
    # Rellenar la LUT por tramos
    for Vin in range(inicialrange,endrange):
      lut.append(round(m * Vin + n))

  arrayResult = np.zeros([arrayImage.shape[0], arrayImage.shape[1], 3], np.uint8)

  for x in range(0, arrayImage.shape[0]): 
      for y in range(0, arrayImage.shape[1]): 
          Vout = lut[arrayImage[x][y][0]]
          if Vout < 0: Vout = 0
          if Vout > 255: Vout = 255
          arrayResult[x][y][0] = Vout
          arrayResult[x][y][1] = Vout
          arrayResult[x][y][2] = Vout

  return arrayResult