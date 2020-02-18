#GUI related imports
import PySimpleGUI as sg 

#Functionality related imports 
from main import copyFiles, moveFiles, findNamesFromFolder, openFile, isImage
from Cache import storeCacheData, getCacheData, cleanCache, clearCache

import os
from shutil import SameFileError

'''
This file manages all the GUI of the program.

'''
#Layout of the main window
layout = [
        [ sg.Text("Challenge Accepted")],
            [
                sg.Button("Add", button_color=("white", "blue"), size= (6, 1)),
                sg.Button("Search", button_color=("white","green"), size=(6, 1)), 
            ],
            [
                sg.Exit(button_color=("white", "red"), size=(6, 1)),
                sg.Button(button_text="Clear Cache", key="clear_cache", button_color=("white", "blue"), size=(12, 1))
            ]
        ]

window = sg.Window("Challenge", resizable=False, size=(250, 120), element_padding=(15, 5)).Layout(layout)
s_window = False
a_window = False

#Main event loop
while True:
    event, values = window.Read(timeout=100)
    # print(event, values)
    if event in (None, 'Exit') or values == 'Exit':
        window.Close()
        break
    
    if event == 'clear_cache':
        if clearCache():
            sg.Popup("Done!")
        else:
            sg.Popup("Nothing in cache")                

    if event == 'Add':
        a_window = True
        '''
        Every time we create a window we have to use a fresh layout. This is why I have to maintain the layout of 
        the add window in the event loop.
        '''
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
                sg.Button("Copy", button_color=("white", "blue"), visible=True),
                sg.Button("Move", button_color=("white", "green"), visible=True)
            ],
        ]

        add_window = sg.Window("Add Files", resizable=False).Layout(add_layout)
  
    if a_window:
        add_events, add_values = add_window.Read(timeout=100)
        if add_events in (None, 'Exit'):
            a_window = False
            add_window.Close()
            
        if add_events == 'Copy':
            copy_count = 0
            files_list = add_window["src_input"].Get().strip()
            if files_list == '':
                sg.Popup("Error!", "Please select files to copy!")
                continue
            dest_folder = add_window["dest_input"].Get().strip()
            if dest_folder == '':
                sg.Popup("Error!", "Please select a destination folder.")
                continue
            try:
                copy_count = copyFiles(files_list, dest_folder)
            except SameFileError:
                sg.Popup(":(", "File already exists at destination!")
                continue
            except OSError:
                sg.Popup(":(", "Please check the entered paths")
                continue
            except:
                sg.Popup(":(", "Something went wrong")
                continue
            sg.Popup("Done!", "Copied {} files.".format(copy_count))

        if add_events == 'Move':
            copy_count = 0
            files_list = add_window["src_input"].Get().strip()
            if files_list == '':
                sg.Popup("Error!", "Please select files to copy!")
                continue
            dest_folder = add_window["dest_input"].Get().strip()
            if dest_folder == '':
                sg.Popup("Error!", "Please select a destination folder.")
                continue
            try:
                copy_count = moveFiles(files_list, dest_folder)
            except SameFileError:
                sg.Popup(":(", "File already exists at destination!")
                continue
            except OSError:
                sg.Popup(":(", "Please check the entered paths")
                continue
            except:
                sg.Popup(":(", "Something went wrong")
                continue
            sg.Popup("Done!", "Moved {} files.".format(copy_count))

    if event == 'Search':
        s_window = True  
        search_layout = [
            [
                sg.Text("Enter the folder you want to search:", key="search_label", visible=True),
                sg.InputText(key="search_input", disabled=False, visible=True), 
                sg.FolderBrowse(key="search_folder", visible=True)
            ],
            [
                sg.Text("Enter keywords to search", key="keywords", visible=True), 
                sg.InputText(key="keywords_input", visible=True), 
                sg.Checkbox("Match Whole", key="match_whole")
            ],
            [
                sg.Button("Search",key="search_btn" ,button_color=("white", "green")),
                sg.Text("                      ",key="count", visible=False)
            ],
            [
                # sg.Text("File : "), sg.Text(key='found_file'), sg.Button("Open file", button_color=("white", "blue"))
                sg.Listbox(["No Results yet"], key="Files", size=(50, 3), visible=True),
                sg.Button("Open", key="Open", button_color=("white", "green"), visible=False)
            ]
        ]

        search_window = sg.Window("Search Files", resizable = False).Layout(search_layout)
      
    if s_window:
        search_event, search_values = search_window.Read(timeout=100)
        
        if search_event in (None, 'Exit'):
            s_window = False
            search_window.Close()
        
        if search_event == "Open":
            f = search_values["Files"]
            if not len(f) == 0:
                openFile(f[0])

        if search_event == "search_folder":
            search_window["search_folder"].Update(disabled=True)

        if search_event == 'search_btn':
            keywords = search_window["keywords_input"].Get().strip()
            if len(keywords.split()) < 1:
                sg.Popup("Error", "Invalid keywords!")
                continue
            if search_window["match_whole"].Get() == 0:
                match_whole = False
            else:
                match_whole = True
            folder = search_window["search_input"].Get().strip()
            if folder == "":
                sg.Popup("Error", "Please select a folder!")
            try:
                count = len([x for x in os.listdir(folder) if isImage(x)])
            except Exception:
                sg.Popup("Error", "Please select a valid folder!")
                continue
            cache = cleanCache(folder)

            search_window["count"].Update(visible=True)
            f = findNamesFromFolder(keywords, folder, match_whole, cache)
            search_window["count"].Update("Searched {}/{}".format(count,count))
            search_window["Open"].Update(visible=True)
            if f == []:
                sg.Popup("Sorry", "No such file found")
            else:
                search_window["Files"].Update(values = f)