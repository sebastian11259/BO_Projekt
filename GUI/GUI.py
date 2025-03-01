#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import PySimpleGUI as sg
import SA_algorithm as alg
import structures as st
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

teachers = ''
classrooms = ''
years = ''
neigh = []
year_list = []
weigh = [100] * 5
initial = 1
temp = 1000000
alpha = 0.8
eps = 0.01
k = 3
Ttable = None
end_result = None
obj_fun_vector = None
obj_fun_current_vec = None
obj_fun_end = None
list_of_tables = []
widget = None
headers = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
char_width = sg.Text.char_width_in_pixels(("Helvetica", 8))
final_value = 0
number_of_lessons = 10


def popup_after_alg(table):
    column = [
        [sg.Text("Algorithm has finished. Do you want to save the result?", background_color='darkgrey')],
        [sg.Input(visible=False, enable_events=True, key="-SAVE-"), sg.FileSaveAs("Save", button_color='grey', size=(5, 1), file_types=(("Excel files", ".xlsx"), )),
         sg.Button("No", enable_events=True, button_color='grey', size=(3, 1))]
    ]

    layout = [
        [sg.VPush(background_color='darkgrey')],
        [sg.Push(background_color='darkgrey'),
         sg.Column(column, element_justification='c', background_color='darkgrey'),
         sg.Push(background_color='darkgrey')],
        [sg.VPush(background_color='darkgrey')]
    ]

    window = sg.Window("Finished", layout=layout, use_default_focus=False, modal=True, background_color='darkgrey')
    event, values = window.read()
    if event == sg.WINDOW_CLOSED or event == "No":
        window.close()
    if event == "-SAVE-":
        table.to_excel(values["-SAVE-"])
    window.close()


def create_plot(obj_fun_current_vec, obj_fun_end):
    # plt.plot(obj_fun_vector)
    plt.plot(obj_fun_current_vec, linewidth=0.5)
    plt.plot(obj_fun_end, linewidth=0.5)
    plt.title("Object function")
    plt.xlabel("Iteration")
    plt.ylabel("Obj fun value")
    plt.legend(["Current", "Best"])
    plt.grid()
    return plt.gcf()


def draw_figure(canvas, figure):
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)
    return figure_canvas_agg


tab1_layout = [
    [
        sg.Text("Choose year to be displayed:", background_color='darkgrey'),
        sg.Combo(year_list, readonly=True, button_background_color='grey', key="-COMBO-", size=(10, 1), enable_events=True)
    ],
    [
        sg.Table(values=[], headings=headers, enable_events=True, key="-TABLE-", vertical_scroll_only=False,\
                 background_color="darkgrey", sbar_background_color='darkgrey', size=(100, 25), row_height=50,\
                 col_widths=[15, 15, 15, 15, 15], auto_size_columns=False, border_width=2, text_color="black")
    ]
]

tab2_layout = [
    [
        sg.Canvas(key="-CANVAS-", background_color="darkgrey", size=(700, 500))
    ]
]

first_column = [
    [
        sg.TabGroup([[sg.Tab("Time Tables", layout=tab1_layout, background_color="darkgrey", key="-TAB1-"),
                      sg.Tab("Graphs", layout=tab2_layout, background_color="darkgrey")]], size=(700, 500),\
                    background_color="darkgrey", tab_background_color="grey", key="-TAB_GROUP-")
    ],
    [
        sg.Text("Final value: ", background_color="darkgrey"),
        sg.Text("", size=(0, 1), key='FINAL_OUTPUT', background_color="darkgrey")
    ]
]

sec_column = [
    [
        sg.Text("Choose file with teachers:", background_color="darkgrey")
    ],
    [
        sg.Input(key="-TEACHERS-", enable_events=True), sg.FileBrowse("Browse", button_color="grey")
    ],
    [
        sg.Text("Choose file with classrooms:", background_color="darkgrey")
    ],
    [
        sg.Input(key="-CLASSROOMS-", enable_events=True), sg.FileBrowse("Browse", button_color="grey")
    ],
    [
        sg.Text("Choose folder with years:", background_color="darkgrey")
    ],
    [
        sg.Input(key="-YEARS-", enable_events=True), sg.FolderBrowse("Browse", button_color="grey")
    ],
    [
        sg.Text("Choose initial result:", background_color="darkgrey"),
        sg.Text("Number of lessons:", background_color='darkgrey', pad=((130, 0), (0, 0)))
    ],
    [
        sg.Radio('Initial 1', "INITIAL", key="-INIT1-", default=True, background_color="darkgrey", enable_events=True),
        sg.Radio('Initial 2', "INITIAL", key="-INIT2-", background_color="darkgrey", enable_events=True),
        sg.Radio('Initial 3', "INITIAL", key="-INIT3-", background_color="darkgrey", enable_events=True),
        sg.Input(default_text="10", enable_events=True, key="-LESSONS-", size=(7, 1), pad=((60, 0), (0, 0)))
    ],
    [
        sg.Text("Choose neighbourhoods:", background_color="darkgrey")
    ],
    [
        sg.Checkbox("NCL", enable_events=True, key="-NCL-", background_color="darkgrey"),
        sg.Checkbox("NSC", enable_events=True, key="-NSC-", background_color="darkgrey"),
        sg.Checkbox("NST", enable_events=True, key="-NST-", background_color="darkgrey")
    ],
    [
        sg.Text("Initial temperature:", background_color="darkgrey"), sg.Text("Alpha:", background_color="darkgrey"),
        sg.Text("Epsilon:", background_color="darkgrey", pad=((37, 30), (0, 0))), sg.Text("K:", background_color="darkgrey")
    ],
    [
        sg.Input(default_text="1000000", enable_events=True, key="-TEMP-", size=(15, 1)), sg.Input(default_text="0.8", enable_events=True, key="-ALPHA-", size=(10, 1)),
        sg.Input(default_text="0.01", enable_events=True, key="-EPS-", size=(10, 1)), sg.Input(default_text="3", enable_events=True, key="-K-", size=(10, 1))
    ],
    [
        sg.Text("Weights for objective function:", font=("", 12, "bold"), background_color="darkgrey")
    ],
    [
        sg.Text("Beginning time:", background_color="darkgrey"), sg.Input(default_text="100", enable_events=True, key="-BEG_TIME-", size=(10, 1), pad=(73, 0))
    ],
    # [
    #     sg.Text("Finishing time:", background_color="darkgrey"), sg.Input(default_text="100", enable_events=True, key="-FIN_TIME-", size=(10, 1), pad=(78, 0))
    # ],
    [
        sg.Text("Windows:", background_color="darkgrey"), sg.Input(default_text="100", enable_events=True, key="-WINDOWS-", size=(10, 1), pad=(106, 0))
    ],
    [
        sg.Text("Lacking teachers:", background_color="darkgrey"), sg.Input(default_text="100", enable_events=True, key="-LACK_TEACH-", size=(10, 1), pad=(60, 0))
    ],
    [
        sg.Text("Lacking classrooms:", background_color="darkgrey"), sg.Input(default_text="100", enable_events=True, key="-LACK_CLASS-", size=(10, 1), pad=(43, 0))
    ],
    [
        sg.Text("Many teachers per subject:", background_color="darkgrey"), sg.Input(default_text="100", enable_events=True, key="-MANY_TEACHERS-", size=(10, 1))
    ],
    [
        sg.Button("Start", enable_events=True, key="-START-", button_color='grey', size=(12, 2), pad=((140, 0), (20, 0)))
    ],
    # [
    #     sg.Input(), sg.SaveAs("Save as", button_color='darkgrey', file_types=(("Excel files", ".xlsx"),))
    # ]
]

layout = [
    [
        sg.Column(first_column, background_color="darkgrey"),
        sg.VSeparator(),
        sg.Column(sec_column, background_color="darkgrey")
    ]
]

window = sg.Window("Schedule", layout=layout, background_color="darkgrey")

while 1:
    event, values = window.read()
    if event == sg.WINDOW_CLOSED:
        break
    if event == "-TEACHERS-":
        teachers = values["-TEACHERS-"]
    if event == "-CLASSROOMS-":
        classrooms = values['-CLASSROOMS-']
    if event == "-YEARS-":
        years = values["-YEARS-"]
        year_list = []
        for filename in os.listdir(years):
            f = os.path.join(years, filename)
            if os.path.isfile(f) and f[-4:] == 'xlsx':
                year_list.append(filename[:-5])
        window['-COMBO-'].update(value='', values=year_list)
    if event == "-INIT1-" or event == "-INIT2-" or event == "-INIT3-":
        if values["-INIT1-"]:
            initial = 1
        elif values["-INIT2-"]:
            initial = 2
        elif values["-INIT3-"]:
            initial = 3
    if event == "-LESSONS-" and values["-LESSONS-"]:
        number_of_lessons = int(values["-LESSONS-"])
    if event == '-NCL-' or event == "-NSC-" or event == "-NST-":
        if values["-NCL-"] and 1 not in neigh:
            neigh.append(1)
        if not values["-NCL-"] and 1 in neigh:
            neigh.remove(1)
        if values["-NSC-"] and 2 not in neigh:
            neigh.append(2)
        if not values["-NSC-"] and 2 in neigh:
            neigh.remove(2)
        if values["-NST-"] and 3 not in neigh:
            neigh.append(3)
        if not values["-NST-"] and 3 in neigh:
            neigh.remove(3)
    if event == "-TEMP-" and values["-TEMP-"]:
        temp = float(values["-TEMP-"])
    if event == "-ALPHA-" and values["-ALPHA-"]:
        alpha = float(values["-ALPHA-"])
    if event == "-EPS-" and values["-EPS-"]:
        eps = float(values["-EPS-"])
    if event == "-K-" and values["-K-"]:
        k = int(values["-K-"])
    if event == "-BEG_TIME-" and values["-BEG_TIME-"]:
        weigh[0] = int(values["-BEG_TIME-"])
    # if event == "-FIN_TIME-" and values["-FIN_TIME-"]:
    #     weigh[1] = int(values["-FIN_TIME-"])
    if event == "-WINDOWS-" and values["-WINDOWS-"]:
        weigh[1] = int(values["-WINDOWS-"])
    if event == "-LACK_TEACH-" and values["-LACK_TEACH-"]:
        weigh[2] = int(values["-LACK_TEACH-"])
    if event == "-LACK_CLASS-" and values["-LACK_CLASS-"]:
        weigh[3] = int(values["-LACK_CLASS-"])
    if event == "-MANY_TEACHERS-" and values["-MANY_TEACHERS-"]:
        weigh[4] = int(values["-MANY_TEACHERS-"])
    if event == "-START-" and neigh and teachers and classrooms and years:
        list_of_tables = []
        if widget:
            widget.get_tk_widget().forget()
            plt.close('all')
        Ttable = st.TimeTable(teachers, classrooms, number_of_lessons)
        Ttable.load_years(years)
        end_result, obj_fun_vector, obj_fun_current_vec, obj_fun_end = alg.sa_algorithm(temp, alpha, eps, k, Ttable,\
                                                                                        initial, neigh, weigh)
        widget = draw_figure(window["-CANVAS-"].TKCanvas, create_plot(obj_fun_current_vec, obj_fun_end))
        window['FINAL_OUTPUT'].update(value=obj_fun_end[-1])
        for el in end_result.get_tables():
            list_of_tables.append(el)
        popup_after_alg(end_result)
    if event == "-COMBO-":
        if values["-COMBO-"] in year_list:
            table_widget = window["-TABLE-"].Widget
            idx = year_list.index(values["-COMBO-"])
            days = [0, 0, 0, 0, 0]
            for row in list_of_tables[idx].values.tolist():
                for i in range(len(row)):
                    if row[i]:
                        if len(row[i]) > days[i]:
                            days[i] = len(row[i]) * char_width
            window["-TABLE-"].update(values=list_of_tables[idx].values.tolist())
            for head, width in zip(headers, days):
                table_widget.column(head, width=width)
            table_widget.pack(side='left', fill='both', expand=True)

window.close()
