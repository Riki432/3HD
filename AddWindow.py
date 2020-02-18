import PySimpleGUI as sg
add_layout = [
    [
        sg.Text("Source File(s)", key="Source", size=(15,1), visible=True), 
        sg.InputText(key="src_input", visible=True, disabled=False), 
        sg.FilesBrowse(visible=True,key="src_files", file_types=(("All Files", "*"), ("JPEG", ".jpeg"),("JPG", ".jpg"),("PNG",".png")))
    ],
    [
        sg.Text("Destination Folder",key="Destination", size=(15,1), visible=True), 
        sg.InputText(key="dest_input", visible=True, disabled=False), 
        sg.FolderBrowse(key="dest_folder", visible=True)
    ],
    [
        sg.Button("Copy", button_color=("white", "blue"), visible=True)
    ],
]

add_window = sg.Window("Add Files", resizable=False).Layout(add_layout)
