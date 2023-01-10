#!/usr/bin/python
# -*- coding: utf-8 -*-

import structures
import pandas as pd
import os
import numpy as np


Ttable = structures.TimeTable(r"C:\Users\Bartosz\Desktop\BO\BO_Projekt\teachers.xlsx", r"C:\Users\Bartosz\Desktop\BO\BO_Projekt\classes.xlsx")
Ttable.load_years(r"C:\Users\Bartosz\Desktop\BO\BO_Projekt\Klasy")
Ttable.initial_2()
# print(Ttable.all_classes())
# print(Ttable.all_teachers())
# print(Ttable.all_years())
print(Ttable.table[0][0][0][0][1])
Ttable.table[0][0][0][0][1] = 1
Ttable.table[0][0][0][1][1] = 2
Ttable.table[0][0][1][2][1] = 2

print(Ttable)
print(Ttable.many_teachers())


# print(Ttable.finishing_time())
# Ttable.table[0][0][0]