#Abrir imagen
from PIL import Image
im = Image.open('../Images/TIFF.jpg')
im.show()

#Transformar imagen en array de puntos RGB
import numpy as np
imarray = np.array(im)

#Imprimir los tamaños tanto del array como de la imagen
print(imarray.shape)
print(im.size)

#Imprimir el array que forma la imagen
print(imarray)

#Una vez modificado el array volver a convertirlo a imagen
Image.fromarray(imarray)

