import structures
import pandas as pd
import os
import numpy as np

def main():
    Ttable = structures.TimeTable()
    Ttable.load_years()
    Ttable.initial_2()
    print(Ttable.table[0][0][0][0])
    # Ttable.table[0][0][0][0] = (
    # Ttable.table[0][0][0][0][0], None, Ttable.table[0][0][0][0][2], Ttable.table[0][0][0][0][3])
    # print(Ttable.all_classes())
    # print(Ttable.all_teachers())
    # print(Ttable.all_years())
    # print(Ttable.lack_of_teacher())
    for el in (Ttable.years[0].subjects):
        print(el)

    print(Ttable.finishing_time())


if __name__ == '__main__':
    # This code won't run if this file is imported.
    main()