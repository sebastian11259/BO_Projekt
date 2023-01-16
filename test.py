#!/usr/bin/python
# -*- coding: utf-8 -*-

import structures
import pandas as pd
import os
import numpy as np
from random import sample


Ttable = structures.TimeTable(r"D:\Studia\5 semestr\BO2\BO_Projekt\Dane\teachers.xlsx", r"D:\Studia\5 semestr\BO2\BO_Projekt\Dane\classes.xlsx", 10)
Ttable.load_years(r"D:\Studia\5 semestr\BO2\BO_Projekt\Dane\Klasy")
Ttable.initial_2()
Ttable.to_excel(r"D:\Studia\5 semestr\BO2\BO_Projekt\Dane\plan.xlsx")


# print(Ttable.all_classes())
# print(Ttable.all_teachers())
# print(Ttable.all_years())
# print(Ttable.table[0][0][0][0][1])
# Ttable.table[0][0][0][0][1] = 1
# Ttable.table[0][0][0][1][1] = 2
# Ttable.table[0][0][1][2][1] = 2
#
# print(Ttable)
# print(Ttable.many_teachers())




# print(Ttable.finishing_time())
# Ttable.table[0][0][0]