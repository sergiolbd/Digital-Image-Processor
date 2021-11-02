from traceback import print_tb
import PySimpleGUI as sg  
from PIL import Image
import numpy as np 
import matplotlib.pyplot as plot

from monochrome import escala_de_grises
from newmonochrome import grayConversion
from histogram import histogram
from brightness import brightness

sg.SetOptions(element_padding=(0, 0))  

# ------ Menu Definition ------ #      
menu_def = [['File', ['Open', 'Save', 'Exit'  ]],      
            ['Edit', ['Paste', ['Special', 'Normal', ], 'Undo', 'Monochrome'], ],
            ['Tools', ['Histogram', 'Normalized Histogram', 'Cumulative Histogram', 'Cumulative Normalized Histogram', 'Brightness']],      
            ['Help', 'About...'], ]      

# ------ GUI Defintion ------ #      
layout = [      
    [sg.Menu(menu_def)],      
    [sg.Output(size=(60, 20))],
    [sg.Image(key="-IMAGE-"), sg.Image(key="-BW-")],
          ]      

window = sg.Window("Image viewer VPC", layout, resizable=True)
# ------ Loop & Process button menu choices ------ #      
while True:      
    event, values = window.read()      
    if event == sg.WIN_CLOSED or event == 'Exit':      
        break      
    print('Button = ', event)      
    # ------ Process menu choices ------ #      
    if event == 'About...':      
        sg.popup('About this program', 'Version 1.0', 'PySimpleGUI rocks...')      
    elif event == 'Open':     # Abrir imagen 
        filename = sg.popup_get_file('file to open', no_window=True) 

        if filename.lower().endswith((".jpg", ".tif")) :
            img_png = Image.open(filename)
            img_png.save(filename, format="PNG")

        # window["-IMAGE-"].update(filename=filename)  
        sg.popup_no_buttons('Text', title="Über uns", text_color=('#F7F6F2'), keep_on_top=True, image=filename)


        # Convertimos imagen en una matriz
        im = Image.open(filename)
        print(im.size, im.mode, im.format)
        imarray = np.asarray(im)
        print(imarray.shape)
        # Convertimos array a imagen nuevamente
        file = Image.fromarray(imarray)
    
        # Mostramos en ventana externa donde permite ver la posición de cada pixel y su valor RGB
        # plot.imshow(imarray)
        # plot.show()
       
    elif event == 'Monochrome': # Convertir en blanco y negro
        # filename2 = escala_de_grises(filename)
        # window["-BW-"].update(filename=filename2)
        newBlack = grayConversion(imarray)
        plot.axis('off')
        # plot.imshow(newBlack, origin="lower")
        plot.imshow(newBlack, interpolation='nearest')
        plot.show()

    elif event == 'Histogram': 
        hist = histogram(filename, False, False)

    elif event == 'Normalized Histogram': 
        histogram(filename, True, False)

    elif event == 'Cumulative Histogram': 
        histogram(filename, False, True)

    elif event == 'Cumulative Normalized Histogram': 
        histogram(filename, True, True)

    elif event == 'Brightness':
        brillo = brightness(hist, imarray.shape)
        print(brillo)
