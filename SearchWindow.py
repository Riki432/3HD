import PySimpleGUI as sg
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
            sg.Text("Total Files :  ",key="count", visible=False)
        ],
        [
            # sg.Text("File : "), sg.Text(key='found_file'), sg.Button("Open file", button_color=("white", "blue"))
            sg.Listbox("Results", key="Files", size=(50, 3), visible=True),
            sg.Button("Open", key="Open", button_color=("white", "green"))
        ]
]

search_window = sg.Window("Search Files", resizable = False).Layout(search_layout)

