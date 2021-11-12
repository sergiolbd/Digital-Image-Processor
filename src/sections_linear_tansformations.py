import numpy as np

# Transformación lienal por tramos

def sectionsLinearTrasformations(arrayImage, numofsections, x):
  
  # inicialrange=0
  lut = []
  # Obtener pendiente de las rectas
  for i in range(numofsections): 
    m = (x[i][1][1] - x[i][0][1]) / (x[i][1][0] - x[i][0][0])
    n = x[i][0][1] - m * x[i][0][0]

    # Recorrer también la LUT
    
    if i == numofsections-1:
      inicialrange = x[i][0][0]
      endrange = x[i][1][0] + 1
    else:
      inicialrange = x[i][0][0]
      endrange = x[i][1][0]

  
    # print("-----------------------" + str(i) + "------------------")
    # print(inicialrange)
    # print(endrange)

    
    
    for Vin in range(inicialrange,endrange):
      lut.append(round(m * Vin + n))

    # lut = [round(m * Vin + n) for Vin in range(inicialrange,endrange)]
    # lut = [round(m * Vin + n) for Vin in range(inicialrange, ((x[i][1][0] - x[i][0][0])+1))] # xf - xi
    

  # print(lut)
  # a=0
  # for i in lut:
  #   a += 1
  
  # print("-------------")
  # print(a)
  
  # for i in range(256):
  #   print( str(i)+" --> " + str(lut[i]))

  arrayResult = np.zeros([arrayImage.shape[0], arrayImage.shape[1], 3], np.uint8)

  for x in range(0, arrayImage.shape[0]): 
      for y in range(0, arrayImage.shape[1]): 
          # print(arrayImage[x][y][0])
          Vout = lut[arrayImage[x][y][0]]
          if Vout < 0: Vout = 0
          if Vout > 255: Vout = 255
          arrayResult[x][y][0] = Vout
          arrayResult[x][y][1] = Vout
          arrayResult[x][y][2] = Vout

  return arrayResult