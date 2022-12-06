from typing import List, Dict

import numpy as np

Days = [i for i in range(5)]
Lesson_hours = [i for i in range(10)]


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
        self.list.append(nr)


class Subject:
    def __init__(self, name, hours, teachers: List[int], classes: List[int]):
        self.name = name
        self.hours = hours
        self.hours_left = hours
        self.teachers = teachers
        self.classes = classes

    def get_t(self):
        return self.teachers

    def get_c(self):
        return self.classes


class Year:
    def __init__(self, name):
        self.name = name
        self.subjects = []

    def add_subject(self, name, hours, teachers: List[int], classes: List[int]):
        self.subjects.append(Subject(name, hours, teachers, classes))


class TimeTable:
    def __init__(self, teachers: Teachers, classes: Classes):
        self.table: List[np.ndarray] = [np.zeros((0, 5, 10), dtype=object),
                                        np.zeros((len(teachers.list), 5, 10), dtype=object),
                                        np.zeros((len(classes.list), 5, 10), dtype=object)]
        self.classes = classes
        self.teachers = teachers

        self.years: List = []
        self.d_years: Dict = {}

    def update_size(self):
        self.table[0] = np.empty((len(self.years), 5, 10))

    def add_year(self, year):
        self.d_years[len(self.d_years)] = year
        self.years.append(year)
        self.update_size()

    def choose_teacher(self, sub: Subject, day, time):
        teachers = sub.get_t()
        t = None
        for t_ in teachers:
            if not isinstance(self.table[1][t_, day, time], tuple):
                t = t_
                break
        return t

    def choose_class(self, sub: Subject, day, time):
        classes = sub.get_c()
        c = None
        for c_ in classes:
            if not isinstance(self.table[2][c_, day, time], tuple):
                c = c_
                break
        return c

    def put_sub(self, day, time, y, t, c, sub: Subject):
        self.table[0][y, day, time] = (y, t, c, sub)
        if t is not None:
            self.table[1][t, day, time] = (y, t, c, sub)
        if c is not None:
            self.table[2][c, day, time] = (y, t, c, sub)
        if sub.hours_left > 0:
            sub.hours_left -= 1

# Funkcje do utowrzenia funkcji celu

    def beginning_time(self):
        delay_time_for_classes: List[int] = []
        for year in range(self.table[0].shape[0]):  # dla każdej klasy
            delay = 0  # opóźneinie w rozpoczęciu
            for day in Days:
                for lesson_hour in Lesson_hours:
                    if not self.table[0][year][day][lesson_hour]:
                        break
                    delay += 1  # im wie
            delay_time_for_classes.append(delay)
        return delay_time_for_classes

    def finishing_time(self):  #
        delay_time_for_classes: List[int] = []
        for year in range(self.table[0].shape[0]):  # dla każdej klasy
            delay = 0  # opóźneinie w zakonczeniu
            for day in Days:
                for lesson_hour in reversed(Lesson_hours):
                    if isinstance(self.table[0][year][day][lesson_hour], tuple):
                        break
                    delay -= 1  # im mniejszy bd dealy tym lepiej można ewentualnie zrobić delay_time_for_classes = delay_time_for_classes - [min(delay_time_for_classes) for i in range(len(delay_time_for_classes))]
            delay_time_for_classes.append(delay)
        return delay_time_for_classes

    def windows(self):
        delay_time_for_classes: List[int] = []
        for year in range(self.table[0].shape[0]):  # dla każdej klasy
            windows_counter = 0  # opóźneinie w zakonczeniu
            for day in Days:
                windows_counter += get_number_of_windows(self.table[0][year][day])  # im mniejszy bd dealy tym lepiej
            delay_time_for_classes.append(windows_counter)
        return delay_time_for_classes

    def lack_of_teacher(self):
        number_of: List[int] = []
        for year in range(self.table[0].shape[0]):  # dla każdej klasy
            num = 0  # opóźneinie w rozpoczęciu
            for day in Days:
                for lesson_hour in Lesson_hours:
                    if isinstance(self.table[0][year][day][lesson_hour], tuple) and self.table[0][year][day][lesson_hour][1] is None:
                        num += 1
            number_of.append(num)
        return number_of

    def lack_of_rooms(self):
        number_of: List[int] = []
        for year in range(self.table[0].shape[0]):  # dla każdej klasy
            num = 0  # opóźneinie w rozpoczęciu
            for day in Days:
                for lesson_hour in Lesson_hours:
                    if isinstance(self.table[0][year][day][lesson_hour], tuple) and self.table[0][year][day][lesson_hour][2] is None:
                        num += 1
            number_of.append(num)
        return number_of


def get_number_of_windows(list_of_lesson_hours: List):
    general_windows_counter = 0
    windows_counter = 0
    lessons_started = False
    window_might_happend = False
    for lesson_hours in list_of_lesson_hours:
        if lessons_started and isinstance(lesson_hours, int):
            window_might_happend = True
            windows_counter += 1
        if isinstance(lesson_hours, tuple):
            lessons_started = True
            if window_might_happend:
                general_windows_counter += windows_counter
                windows_counter = 0
    return general_windows_counter