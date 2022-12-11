from typing import List, Dict
import os
import pandas as pd
import numpy as np

Days = [i for i in range(5)]
Lesson_hours = [i for i in range(10)]


class Teachers:
    def __init__(self):
        self.list = []
        self.dict = {}

    def add_teacher(self, name):
        self.dict[name] = len(self.dict)
        self.list.append(name)

    def get_id(self, name):
        return self.dict[name]



class Classes:
    def __init__(self):
        self.list = []
        self.dict = {}

    def add_class(self, nr):
        self.dict[nr] = len(self.dict)
        self.list.append(nr)

    def get_id(self, nr):
        return self.dict[nr]


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
        self.subjects: List[Subject] = []
        self.hours_left = 0

    def add_subject(self, name, hours, teachers: List[int], classes: List[int]):
        self.subjects.append(Subject(name, hours, teachers, classes))
        self.hours_left += hours


class TimeTable:
    def __init__(self):
        self.classes = Classes()
        self.teachers = Teachers()

        df = pd.read_excel('teachers.xlsx')
        for i, j in df.iterrows():
            self.teachers.add_teacher((j['Imię i nazwisko']))

        df = pd.read_excel('classes.xlsx')
        for i, j in df.iterrows():
            self.classes.add_class(str(j['Nr Sali']))

        self.years: List[Year] = []
        self.d_years: Dict = {}

        self.table: List[np.ndarray] = [np.zeros((0, 5, 6), dtype=object),
                                        np.zeros((len(self.teachers.list), 5, 6), dtype=object),
                                        np.zeros((len(self.classes.list), 5, 6), dtype=object)]

    def update_size(self):
        self.table[0] = np.zeros((len(self.years), 5, 6), dtype=object)

    def add_year(self, year):
        self.d_years[year] = len(self.d_years)
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
        if sub.hours_left > 0:
            sub.hours_left -= 1
            self.years[y].hours_left -= 1
            self.table[0][y, day, time] = (y, t, c, sub)
            if t is not None:
                self.table[1][t, day, time] = (y, t, c, sub)
            if c is not None:
                self.table[2][c, day, time] = (y, t, c, sub)


    def get_year_id(self, year):
        return self.d_years[year]

    def all_years(self):
        y = []
        for y_ in self.years:
            y.append(y_.name)
        return y

    def all_teachers(self):
        return self.teachers.list

    def all_classes(self):
        return self.classes.list

    def load_years(self):
        for filename in os.listdir('Klasy'):
            f = os.path.join('Klasy', filename)
            # checking if it is a xlsx file
            if os.path.isfile(f) and f[-4:] == 'xlsx':
                df = pd.read_excel(f)
                y = Year(filename[:-5])
                for i, j in df.iterrows():
                    t = j['Prowadzący'].split(', ') # lista prowadzących z excela - nazwy
                    t_ = []                         # lista prowadzących z excela - id
                    for i in t:
                        t_.append(self.teachers.get_id(i))
                    c = str(j['Sala']).split(', ')  # lista s z excela - nr
                    c_ = []                         # lista s z excela - id
                    for i in c:
                        c_.append(self.classes.get_id(i))
                    y.add_subject(j['Nazwa'], j['Liczba godzin'], t_, c_)
                self.add_year(y)

    def get_tables(self):
        tables = []
        for y in self.years:
            y_idx = self.get_year_id(y)
            tt = np.zeros([6,5], dtype=object)
            for day in range(5):
                for time in range(6):
                    if self.table[0][y_idx, day, time] == 0:
                        tt[time][day] = None
                    else:
                        if self.table[0][y_idx, day, time][1] is None:
                            t = None
                        else:
                            t = self.teachers.list[self.table[0][y_idx, day, time][1]]

                        if self.table[0][y_idx, day, time][2] is None:
                            c = None
                        else:
                            c = self.classes.list[self.table[0][y_idx, day, time][2]]
                        s = self.table[0][y_idx, day, time][3].name
                        str = '{}, {}, Sala nr {}'.format(s, t, c)
                        tt[time][day] = str
            tables.append(pd.DataFrame(tt, columns=['Day 1','Day 2','Day 3', 'Day 4', 'Day 5']))

        return tables

# Rozwiązanie startowe
    def initial_1(self): # rozkłada zajęcia po kolei w wolnych terminach
        for y in self.years:
            y_idx = self.get_year_id(y)
            for day in range(5):
                for time in range(6):
                    for s in y.subjects:
                        if s.hours_left != 0:
                            t_idx = self.choose_teacher(s, day, time)
                            c_idx = self.choose_class(s, day, time)
                            self.put_sub(day, time, y_idx, t_idx, c_idx, s)
                            break
                        else:
                            continue

    def initial_2(self): # rozkłada zajęcia po kolei w wolnych terminach tylko gdy jest wolny nauczyciel i sala, dopiero potem jak sie nie udało rozdzielić wszystkich to reszte rozklada w pierwszysch wolnych terminach
        for y in self.years:
            y_idx = self.get_year_id(y)
            for day in range(5):
                for time in range(6):
                    for s in y.subjects:
                        if s.hours_left != 0:
                            t_idx = self.choose_teacher(s, day, time)
                            c_idx = self.choose_class(s, day, time)
                            if t_idx is None or c_idx is None:
                                continue
                            else:
                                self.put_sub(day, time, y_idx, t_idx, c_idx, s)
                            break
                        else:
                            continue
            if y.hours_left > 0:
                for day in range(5):
                    for time in range(6):
                        if self.table[0][y_idx, day, time] == 0:
                            for s in y.subjects:
                                if s.hours_left != 0:
                                    t_idx = self.choose_teacher(s, day, time)
                                    c_idx = self.choose_class(s, day, time)
                                    self.put_sub(day, time, y_idx, t_idx, c_idx, s)
                                    break
                                else:
                                    continue


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