import pandas as pd
import os
import numpy as np
import SA_algorithm as alg
import matplotlib.pyplot as plt
import time
import structures

# temper = np.linspace(100000, 100000000, 100)
temper = [[1, 2, 3]]
print(temper)

alpha = 0.95
eps = 0.01
k = 10
initial = 3
neigh = [1]
weigh = [100] * 6
weigh[1] = 100
temp = 100000
timer = []
y = []
iter = []
init_value = []
pre_1 = [99999999999]
pre_2 = [99999999999]
for id, diff in enumerate(temper):
    ins_timer = []
    ins_y = []
    ins_iter = []
    ins_init_value = []
    for i in range(2):
        try:
            Ttable = structures.TimeTable(r"C:\Users\Bartosz\Desktop\BO\rb\BO_Projekt\Dane\teachers.xlsx",
                                          r"C:\Users\Bartosz\Desktop\BO\rb\BO_Projekt\Dane\classes.xlsx", 10)
            Ttable.load_years(r"C:\Users\Bartosz\Desktop\BO\rb\BO_Projekt\Dane\Klasy")
            start = time.time()
            z, x, c, v = alg.sa_algorithm(temp, alpha, eps, k, Ttable, initial, diff, weigh)
            print(v[-1], pre_2[-1])
            if v[-1] < pre_2[-1]:
                pre_1 = c
                pre_2 = v
            ins_init_value.append(v[0])
            end = time.time()
            ins_timer.append(end - start)
            ins_y.append(v[-1])
            ins_iter.append(len(v))
            print(end - start)
        except:
            print("failed")
    try:
        print(sum(ins_init_value) / len(ins_init_value))
        print(diff, sum(ins_iter) / len(ins_iter), sum(ins_timer) / len(ins_timer), sum(ins_y) / len(ins_y))
        iter.append(sum(ins_iter) / len(ins_iter))
        timer.append(sum(ins_timer) / len(ins_timer))
        y.append(sum(ins_y) / len(ins_y))
    except:
        None

Ttable.to_excel(r"C:\Users\Bartosz\Desktop\BO\rb\BO_Projekt\plik.xlsx")
def create_plot2(obj_fun_current_vec, obj_fun_end):
    plt.plot(obj_fun_current_vec, linewidth=0.5)
    plt.plot(obj_fun_end, linewidth=0.5)
    plt.title("Object function")
    plt.xlabel("Iteration")
    plt.ylabel("Obj fun value")
    plt.legend(["Current", "Best"])
    plt.grid()
    plt.savefig('example.png')
    plt.show()

create_plot2(pre_1, pre_2)
