import PySimpleGUI as sg
import os.path


# ---------------Menu ----------------------------

menu_def = [
            ['&File', ['&Open', '&Save', 'E&xit', 'Properties']],
            ['&Edit', ['Paste', 'Copy', 'Undo'], ],
            ['&Help', '&About...'], 
           ]

file_list_column = [
  [
    sg.Text("Image Folder"),
    sg.In(size=(25,1), enable_events=True, key="-FOLDER-"),
    sg.FolderBrowse(),
  ],
  [
    sg.Listbox(
      values=[], enable_events=True, size=(40,20),
      key="-FILE LIST-"
    )
  ],
]

image_viewer_column = [
  [sg.Text("Choose an image from the list ont the left:")],
  [sg.Text(size=(40,1), key="-TOUT-")],
  [sg.Image(key="-IMAGE-")],
]

# Full layout

layout = [
  [sg.Menu(menu_def, tearoff=True)],
  [
    sg.Column(file_list_column),
    sg.VSeparator(),
    sg.Column(image_viewer_column),
  ]
]

window = sg.Window("Image Viewer", layout)

# event loop 
while True:
  event, values = window.read()
  if event == "Exit" or event == sg.WIN_CLOSED:
    break
  if event == "-FOLDER-":
    folder = values["-FOLDER-"]
    try:
      file_list = os.listdir(folder)
    except:
      file_list = []

    fnames = [
      f
      for f in file_list
      if os.path.isfile(os.path.join(folder, f))
      and f.lower().endswith((".png"))
    ]
    window["-FILE LIST-"].update(fnames)
  elif event =="-FILE LIST-":
      try:
        filename = os.path.join(
          values["-FOLDER-"], values["-FILE LIST-"][0]
        )
        window["-TOUT-"].update(filename)
        window["-IMAGE-"].update(filename=filename)
      except:
        pass

window.close()

# layout = [
#   [sg.Text('Your Folder', size=(15, 1), auto_size_text=False, justification='right'),
#      sg.InputText('Default Folder'), sg.FolderBrowse()]
# ]

# window = sg.Window('ImageSergio', layout, default_element_size=(40, 1), grab_anywhere=False)
# event, values = window.read()