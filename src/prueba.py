import PySimpleGUI as sg  
from PIL import Image
import numpy as np
    
sg.SetOptions(element_padding=(0, 0))      

# ------ Menu Definition ------ #      
menu_def = [['File', ['Open', 'Save', 'Exit'  ]],      
            ['Edit', ['Paste', ['Special', 'Normal', ], 'Undo'], ],      
            ['Help', 'About...'], ]      

# ------ GUI Defintion ------ #      
layout = [      
    [sg.Menu(menu_def, )],      
    [sg.Output(size=(60, 20))],
    [sg.Image(key="-IMAGE-")],
          ]      

window = sg.Window("Image viewer VPC", layout, default_element_size=(12, 1), auto_size_text=False, auto_size_buttons=False,      
                    default_button_element_size=(12, 1))      

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
        print(filename)
        if filename.lower().endswith((".png")):
          window["-IMAGE-"].update(filename=filename) 
          im = Image.open(filename)
          imarray = np.array(im)
          print(imarray.shape)
          print(im.size)
          print(imarray)
        else:
          print ('Error: El fichero ' + filename + 'no es una imagen') 
