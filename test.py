#!/usr/bin/python
# -*- coding: utf-8 -*-

import structures
import pandas as pd
import os
import numpy as np


Ttable = structures.TimeTable()
Ttable.load_years()
Ttable.initial_2()
print(Ttable.table[0][0][0][0])
Ttable.table[0][0][0][0] = (Ttable.table[0][0][0][0][0], None, Ttable.table[0][0][0][0][2], Ttable.table[0][0][0][0][3])
# print(Ttable.all_classes())
# print(Ttable.all_teachers())
# print(Ttable.all_years())
print(Ttable.lack_of_teacher())
print(Ttable)

print(Ttable.finishing_time())
# Ttable.table[0][0][0]