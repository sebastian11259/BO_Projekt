#!/usr/bin/python
# -*- coding: utf-8 -*-

import structures
import pandas as pd
import os


Ttable = structures.TimeTable()
Ttable.load_years()

print(Ttable.all_classes())
print(Ttable.all_teachers())
print(Ttable.all_years())