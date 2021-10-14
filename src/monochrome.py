from PIL import Image

def escala_de_grises(imagen):
    #Abrimos la Imagen
    im = Image.open(imagen)
    rgb_im = im.convert('RGB')

    #Obtenemos sus dimensiones
    x = im.size[0]
    y = im.size[1]

    #Creamos una nueva imagen con las dimensiones de la imagen anterior
    im2 = Image.new('RGB', (x, y))
    
    i = 0
    while i < x:
        j = 0
        while j < y:
            #Obtenemos el valor RGB de cada pixel
            r, g, b = rgb_im.getpixel((i,j))
            #Obtenemos su equivalente en la escala de gris
            p = (r * 0.299 + g * 0.587 + b * 0.114)
            #Ese valor lo convertimos a entero
            gris = int(p)
            pixel = tuple([gris, gris, gris])
            #En la nueva imagen en la posición i, j agregamos el nuevo color 
            im2.putpixel((i,j), pixel)
            j += 1
        i += 1
        
    #Guardamos la imagen
    newImageMonochrome = '../Images/Imagen1Monochrome.png'
    im2.save(newImageMonochrome)
    im2.convert('RGB')
    return  newImageMonochrome
    

