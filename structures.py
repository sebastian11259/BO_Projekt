from typing import List, Dict

import numpy as np

class Teachers:
    def __init__(self):
        self.list = []
        self.dict = {}

    def add_teacher(self, name, dostepnosc):
        self.dict[len(self.dict)] = name
        self.list.append((name, dostepnosc))


class Classes:
    def __init__(self):
        self.list = []
        self.dict = {}

    def add_class(self, nr):
        self.dict[len(self.dict)] = nr
        self.list.append((nr))


class Subject:
    def __init__(self, name, hours, teachers: List[int], classes: List[int]):
        self.name = name
        self.hours = hours
        self.teachers = teachers
        self.classes = classes


class Year:
    def __init__(self, name):
        self.name = name
        self.subjects = []

    def add_subject(self, name, hours, teachers: List[int], classes: List[int]):
        self.subjects.append(Subject(name, hours, teachers, classes))


class TimeTable:
    def __init__(self, teachers: Teachers, classes: Classes, year: List[Year]):
        self.table: List[np.ndarray] = [np.empty((5, 10, 0)), np.empty((5, 10, len(teachers.list))), np.empty((5, 10, len(classes.list)))]
        self.classes = classes
        self.teachers = teachers

        self.years: List = []
        self.d_years: Dict = {}

    def update_size(self):
        self.table[0] = np.empty((0, 0, len(self.years)))

    def add_year(self, year):
        self.d_years[len(self.d_years)] = year
        self.years.append(year)
        self.update_size()

