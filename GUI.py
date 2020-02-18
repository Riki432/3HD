import PySimpleGUI as sg
from main import copyFiles, findNamesFromFolder, openFile
from SearchWindow import search_window
from AddWindow import add_window
from Cache import storeCacheData, getCacheData, cleanCache, clearCache
import os
from shutil import SameFileError

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


    if event == 'Search':
        s_window = True    
    if s_window:
        search_event, search_values = search_window.Read(timeout=100)
        # print(search_event, search_values)
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
                count = len(os.listdir(folder))
            except Exception:
                sg.Popup("Error", "Please select a valid folder!")
                continue
            cache = cleanCache(folder)
            # sg.ProgressBar(100)
            # try:
            search_window["count"].Update(visible=True)
            search_window["count"].Update("Total Files : {}".format(count))
            f = findNamesFromFolder(keywords, folder, match_whole, cache)
            print(f)
            if f == []:
                sg.Popup("Sorry", "No such file found")
                # break
            else:
                search_window["Files"].Update(values = f)
                # break
                # if sg.PopupYesNo("File found: {} \n Do you want to open it?".format(f)) == 'Yes':
                #     print("{}\{}".format(folder.replace("/", "\\"), f))
                #     openFile("{}\{}".format(folder.replace("/", "\\"), f))
                #     break
