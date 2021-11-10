import numpy as np


# Transformación lienal por tramos

def sectionsLinearTrasformations(arrayImage, xi, yi, xf, yf):
  
  # Obtener pendiente de las rectas
  m = (yf - yi) / (xf - xi)
  n = yi - m * xi

  lut = [round(m * Vin + n) for Vin in range(256)]

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