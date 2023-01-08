#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import PySimpleGUI as sg
import pandas as pd
import structures as st
import SA_algorithm as alg
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

teachers = ''
classrooms = ''
years = ''
initial = 1
neigh = []
weigh = [100] * 5
year_list = []
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


def create_plot(obj_fun_current_vec, obj_fun_end):
    # plt.plot(obj_fun_vector)
    plt.plot(obj_fun_current_vec)
    plt.plot(obj_fun_end)
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
        sg.Table(values=[], headings=["Mon", "Tue", "Wed", "Thu", "Fri"], enable_events=True, key="-TABLE-",\
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
        sg.Text("Choose initial result:", background_color="darkgrey")
    ],
    [
        sg.Radio('Initial 1', "INITIAL", key="-INIT1-", default=True, background_color="darkgrey", enable_events=True),
        sg.Radio('Initial 2', "INITIAL", key="-INIT2-", background_color="darkgrey", enable_events=True)
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
        sg.Text("Beginning time:", background_color="darkgrey"), sg.Input(default_text="100", enable_events=True, key="-BEG_TIME-", size=(10, 1), pad=(35, 0))
    ],
    [
        sg.Text("Finishing time:", background_color="darkgrey"), sg.Input(default_text="100", enable_events=True, key="-FIN_TIME-", size=(10, 1), pad=(40, 0))
    ],
    [
        sg.Text("Windows:", background_color="darkgrey"), sg.Input(default_text="100", enable_events=True, key="-WINDOWS-", size=(10, 1), pad=(68, 0))
    ],
    [
        sg.Text("Lacking teachers:", background_color="darkgrey"), sg.Input(default_text="100", enable_events=True, key="-LACK_TEACH-", size=(10, 1), pad=(22, 0))
    ],
    [
        sg.Text("Lacking classrooms:", background_color="darkgrey"), sg.Input(default_text="100", enable_events=True, key="-LACK_CLASS-", size=(10, 1))
    ],
    [
        sg.Button("Start", enable_events=True, key="-START-", button_color='grey', size=(12, 2), pad=((140, 0), (20, 0)))
    ]
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
    if event == "-INIT1-" or event == "-INIT2-":
        if values["-INIT1-"]:
            initial = 1
        if not values["-INIT1-"]:
            initial = 2
    if event == '-NCL-' or event == "-NSC-" or event == "-NST-":
        if values["-NCL-"]:
            if 1 not in neigh:
                neigh.append(1)
        if not values["-NCL-"]:
            if 1 in neigh:
                neigh.remove(1)
        if values["-NSC-"]:
            if 2 not in neigh:
                neigh.append(2)
        if not values["-NSC-"]:
            if 2 in neigh:
                neigh.remove(2)
        if values["-NST-"]:
            if 3 not in neigh:
                neigh.append(3)
        if not values["-NST-"]:
            if 3 in neigh:
                neigh.remove(3)
    if event == "-TEMP-":
        temp = float(values["-TEMP-"])
    if event == "-ALPHA-":
        alpha = float(values["-ALPHA-"])
    if event == "-EPS-":
        eps = float(values["-EPS-"])
    if event == "-K-":
        k = int(values["-K-"])
    if event == "-BEG_TIME-":
        weigh[0] = int(values["-BEG_TIME-"])
    if event == "-FIN_TIME-":
        weigh[1] = int(values["-FIN_TIME-"])
    if event == "-WINDOWS-":
        weigh[2] = int(values["-WINDOWS-"])
    if event == "-LACK_TEACH-":
        weigh[3] = int(values["-LACK_TEACH-"])
    if event == "-LACK_CLASS-":
        weigh[4] = int(values["-LACK_CLASS-"])
    if event == "-START-":
        if widget:
            widget.get_tk_widget().forget()
            plt.close('all')
        Ttable = st.TimeTable(teachers, classrooms)
        Ttable.load_years(years)
        end_result, obj_fun_vector, obj_fun_current_vec, obj_fun_end = alg.sa_algorithm(temp, alpha, eps, k, Ttable,\
                                                                                        initial, neigh, weigh)
        widget = draw_figure(window["-CANVAS-"].TKCanvas, create_plot(obj_fun_current_vec, obj_fun_end))
        for el in end_result.get_tables():
            list_of_tables.append(el)
    if event == "-COMBO-":
        if values["-COMBO-"] in year_list:
            idx = year_list.index(values["-COMBO-"])
            window["-TABLE-"].update(values=list_of_tables[idx].values.tolist())

window.close()
