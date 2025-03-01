from typing import List, Dict
import os
import pandas as pd
import numpy as np
import random
from copy import deepcopy
num_of_lessons_pear_day = 10
Days = [i for i in range(5)]
Lesson_hours = [i for i in range(num_of_lessons_pear_day)]


class Teachers:
    def __init__(self):
        self.list = []
        self.dict = {}

    def add_teacher(self, name):
        self.dict[name] = len(self.dict)
        self.list.append(name)

    def get_id(self, name):
        return self.dict[name]

    def __str__(self):
        return str(self.dict)


class Classrooms:
    def __init__(self):
        self.list = []
        self.dict = {}

    def add_class(self, nr):
        self.dict[nr] = len(self.dict)
        self.list.append(nr)

    def get_id(self, nr: str):
        return self.dict[nr]

    def __str__(self):
        return str(self.dict)


class Subject:
    def __init__(self, name, hours, teachers: List[int], classrooms: List[int]):
        self.name = name
        self.hours = hours
        self.hours_left = hours
        self.teachers = teachers
        self.classrooms = classrooms

    def get_t(self):
        return self.teachers

    def get_c(self):
        return self.classrooms

    def __str__(self):
        return str(self.name)

    def __deepcopy__(self, memodict={}):
        new = Subject(self.name, self.hours, self.teachers, self.classrooms)
        return new


class Year:
    def __init__(self, name):
        self.name = name
        self.subjects: List[Subject] = []
        self.hours_left = 0

    def add_subject(self, name, hours, teachers: List[int], classes: List[int]):
        self.subjects.append(Subject(name, hours, teachers, classes))
        self.hours_left += hours

    def __str__(self):
        return str(self.name)

    def __deepcopy__(self, memodict={}):
        new = Year(self.name)
        new.subjects = deepcopy(self.subjects)
        new.hours_left = deepcopy(self.hours_left)
        return new


class TimeTable:
    def __init__(self, teach_dir, class_dir, lessons):
        self.teach_dir = teach_dir
        self.class_dir = class_dir
        self.lessons = lessons

        self.classes = Classrooms()
        self.teachers = Teachers()

        df = pd.read_excel(teach_dir)
        for i, j in df.iterrows():
            self.teachers.add_teacher((j['Imię i nazwisko']))

        df = pd.read_excel(class_dir)
        for i, j in df.iterrows():
            self.classes.add_class(str(j['Nr Sali']))

        self.years: List[Year] = []
        self.d_years: Dict = {}

        self.table: List[np.ndarray] = [np.zeros((0, 5, self.lessons), dtype=object),
                                        np.zeros((len(self.teachers.list), 5, self.lessons), dtype=object),
                                        np.zeros((len(self.classes.list), 5, self.lessons), dtype=object)]

    def __str__(self):
        string = ""
        for el in self.get_tables():
            string += str(el) + "\n"
        return string

    def __deepcopy__(self, memodict={}):
        new = TimeTable(self.teach_dir, self.class_dir, self.lessons)
        new.years = self.years
        new.d_years = self.d_years
        new.table = deepcopy(self.table)
        return new

    def update_size(self):
        self.table[0] = np.zeros((len(self.years), 5, self.lessons), dtype=object)

    def add_year(self, year):
        self.d_years[year] = len(self.d_years)
        self.years.append(year)
        self.update_size()

    def choose_teacher(self, sub: Subject, day, time):
        teachers = sub.get_t()
        t = None
        for t_ in teachers:
            if not isinstance(self.table[1][t_, day, time], list):
                t = t_
                break
        return t

    def choose_class(self, sub: Subject, day, time):
        classes = sub.get_c()
        c = None
        for c_ in classes:
            if not isinstance(self.table[2][c_, day, time], list):
                c = c_
                break
        return c

    def put_sub(self, day, time, y, t, c, sub: Subject):
        if sub.hours_left > 0:
            sub.hours_left -= 1
            self.years[y].hours_left -= 1
            self.table[0][y, day, time] = [y, t, c, sub]
            if t is not None:
                self.table[1][t, day, time] = [y, t, c, sub]
            if c is not None:
                self.table[2][c, day, time] = [y, t, c, sub]

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

    def load_years(self, directory):
        for filename in os.listdir(directory):
            f = os.path.join(directory, filename)
            # checking if it is a xlsx file
            if os.path.isfile(f) and f[-4:] == 'xlsx':
                df = pd.read_excel(f)
                y = Year(filename[:-5])
                for i, j in df.iterrows():
                    t = j['Prowadzący'].split(', ') # lista prowadzących z excela - nazwy
                    t_ = []                         # lista prowadzących z excela - id
                    for i in t:
                        t_.append(self.teachers.get_id(i.strip()))
                    c = str(j['Sala']).split(', ')  # lista s z excela - nr
                    if c[0] == 'nan':
                        c_ = self.classes.dict.values()
                    else:
                        c_ = []                         # lista s z excela - id
                        for i in c:
                            c_.append(self.classes.get_id(i.strip()))
                    y.add_subject(j['Nazwa'], j['Liczba godzin'], t_, c_)
                self.add_year(y)

    def get_tables(self):
        tables = []
        for y in self.years:
            y_idx = self.get_year_id(y)
            tt = np.zeros([self.lessons, 5], dtype=object)
            for day in range(5):
                for time in range(self.lessons):
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

    def to_excel(self, filepath: str):
        writer = pd.ExcelWriter(filepath)
        for i, t in enumerate(self.get_tables()):
            df = pd.DataFrame(t)
            df.to_excel(writer, sheet_name="{}".format(self.years[i].name))
        writer.close()

    # Rozwiązanie startowe
    def initial_1(self):  # rozkłada zajęcia po kolei w wolnych terminach
        for y in self.years:
            y_idx = self.get_year_id(y)
            for day in range(5):
                for time in range(self.lessons):
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
                for time in range(self.lessons):
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
                    for time in range(self.lessons):
                        if self.table[0][y_idx, day, time] == 0:
                            for s in y.subjects:
                                if s.hours_left != 0:
                                    t_idx = self.choose_teacher(s, day, time)
                                    c_idx = self.choose_class(s, day, time)
                                    self.put_sub(day, time, y_idx, t_idx, c_idx, s)
                                    break
                                else:
                                    continue

    def initial_3(self):  # rozkłada zajęcia w po kolei w wolnych terminach
        for y in self.years:
            y_idx = self.get_year_id(y)
            for time in random.sample(range(self.lessons), self.lessons):
                for day in random.sample(range(5),5):
                    for s in y.subjects:
                        if s.hours_left != 0:
                            t_idx = self.choose_teacher(s, day, time)
                            c_idx = self.choose_class(s, day, time)
                            self.put_sub(day, time, y_idx, t_idx, c_idx, s)
                            break
                        else:
                            continue

    # Sąsiedztwo

    def neighbour_change_lesson(self):
        # wyszukuję losową klasę, dzień i godzinę
        ran_year = None
        ran_day = None
        ran_hour = None
        day_empty = None
        lesson_hour_empty = None
        for i in range(50):
            ran_year = random.randint(0, self.table[0].shape[0]-1)
            ran_day = random.randint(0, len(Days)-1)
            ran_hour = random.randint(0, self.lessons-1)
            if isinstance(self.table[0][ran_year, ran_day, ran_hour], list):
                break

        # Znajduję losowo wolny termin dla tej samej klasy
        if isinstance(self.table[0][ran_year, ran_day, ran_hour], list):
            y, t, c, sub = self.table[0][ran_year, ran_day, ran_hour]
            list_of_empty: List[List[int]] = []

            for day in Days:
                for lesson_hour in range(self.lessons):
                    if isinstance(self.table[0][ran_year][day][lesson_hour], int):
                        list_of_empty.append([ran_year, day, lesson_hour])

            # usuwam stary termin i wpisuję w nowy
            if list_of_empty:
                ran_lesson_empty = random.choice(list_of_empty)
                day_empty = ran_lesson_empty[1]
                lesson_hour_empty = ran_lesson_empty[2]
                self.table[0][ran_year, day_empty, lesson_hour_empty] = [y, t, c, sub]
                self.table[0][ran_year, ran_day, ran_hour] = 0
                if t is not None:
                    if isinstance(self.table[1][t, ran_lesson_empty[1], ran_lesson_empty[2]], list):
                        yt = self.table[1][t, ran_lesson_empty[1], ran_lesson_empty[2]][0]
                        self.table[0][yt, ran_lesson_empty[1], ran_lesson_empty[2]][1] = None
                    self.table[1][t, ran_day, ran_hour] = 0
                    self.table[1][t, ran_lesson_empty[1], ran_lesson_empty[2]] = [y, t, c, sub]
                if c is not None:
                    if isinstance(self.table[2][c, ran_lesson_empty[1], ran_lesson_empty[2]], list):
                        yt = self.table[2][c, ran_lesson_empty[1], ran_lesson_empty[2]][0]
                        self.table[0][yt, ran_lesson_empty[1], ran_lesson_empty[2]][2] = None
                    self.table[2][c, ran_day, ran_hour] = 0
                    self.table[2][c, ran_lesson_empty[1], ran_lesson_empty[2]] = [y, t, c, sub]

                for year in range(self.table[0].shape[0]):
                    if year != ran_year:
                        if isinstance(self.table[0][year, ran_day, ran_hour], list):
                            if self.table[0][year, ran_day, ran_hour][1] is None:
                                teach = self.choose_teacher(self.table[0][year, ran_day, ran_hour][3], ran_day, ran_hour)
                                if teach is not None:
                                    y, t, c, sub = self.table[0][year, ran_day, ran_hour]
                                    self.table[0][y, ran_day, ran_hour][1] = teach
                                    self.table[1][teach, ran_day, ran_hour] = [y, teach, c, sub]
                                    if c is not None:
                                        self.table[2][c, ran_day, ran_hour][1] = teach
                                    break
                            if self.table[0][year, ran_day, ran_hour][2] is None:
                                classroom = self.choose_class(self.table[0][year, ran_day, ran_hour][3], ran_day, ran_hour)
                                if classroom is not None:
                                    y, t, c, sub = self.table[0][year, ran_day, ran_hour]
                                    self.table[0][y, ran_day, ran_hour][2] = classroom
                                    self.table[2][classroom, ran_day, ran_hour] = [y, t, classroom, sub]
                                    if c is not None:
                                        self.table[1][t, ran_day, ran_hour][2] = classroom
                                    break
            else:  # jezeli nie ma wolnych terminow mozna zrobic wyszukanie losowe i zamiana miejscami
                pass

        return ran_year, ran_day, ran_hour, day_empty, lesson_hour_empty

    def neighbour_add_teach_class(self):
        for year in range(self.table[0].shape[0]):
            for day in Days:
                for lesson in range(self.lessons):
                    if isinstance(self.table[0][year, day, lesson], list):
                        if self.table[0][year, day, lesson][1] is None:
                            teach = self.choose_teacher(self.table[0][year, day, lesson][3], day, lesson)
                            if teach is not None:
                                y, t, c, sub = self.table[0][year, day, lesson]
                                self.table[0][year, day, lesson][1] = teach
                                self.table[1][teach, day, lesson] = [y, teach, c, sub]
                                if c is not None:
                                    self.table[2][c, day, lesson][1] = teach
                        if self.table[0][year, day, lesson][2] is None:
                            classroom = self.choose_class(self.table[0][year, day, lesson][3], day, lesson)
                            if classroom is not None:
                                y, t, c, sub = self.table[0][year, day, lesson]
                                self.table[0][year, day, lesson][2] = classroom
                                self.table[2][classroom, day, lesson] = [y, t, classroom, sub]
                                if t is not None:
                                    self.table[1][t, day, lesson][2] = classroom

    def neighbour_change_classroom(self):
        list_of_lacking_classroom: List[List[int]] = []

        # znajduje lekcje gdzie nie ma sali
        for year in range(self.table[0].shape[0]):
            for day in Days:
                for lesson_hour in range(self.lessons):
                    if isinstance(self.table[0][year][day][lesson_hour], list) and \
                            self.table[0][year][day][lesson_hour][2] is None:
                        list_of_lacking_classroom.append(
                            [year, day, lesson_hour, self.table[0][year][day][lesson_hour][3]])

        # wybiera losowo lekcje i losowo salę
        if list_of_lacking_classroom:
            ran_lesson_lack = random.choice(list_of_lacking_classroom)
            classroom = random.choice(list(ran_lesson_lack[3].get_c()))

            # wpisanie nowej sali
            y, t, c, sub = self.table[0][ran_lesson_lack[0], ran_lesson_lack[1], ran_lesson_lack[2]]
            if isinstance(self.table[2][classroom, ran_lesson_lack[1], ran_lesson_lack[2]], list):
                y_prev = self.table[2][classroom, ran_lesson_lack[1], ran_lesson_lack[2]][0]
                self.table[0][y_prev, ran_lesson_lack[1], ran_lesson_lack[2]][2] = c
            self.table[0][y, ran_lesson_lack[1], ran_lesson_lack[2]][2] = classroom
            self.table[2][classroom, ran_lesson_lack[1], ran_lesson_lack[2]] = [y, t, classroom, sub]
            if t is not None and isinstance(self.table[1][t, ran_lesson_lack[1], ran_lesson_lack[2]], list):
                self.table[1][t, ran_lesson_lack[1], ran_lesson_lack[2]][2] = classroom
        else:
            ran_year = None
            ran_day = None
            ran_hour = None
            for i in range(50):
                ran_year = random.randint(0, self.table[0].shape[0]-1)
                ran_day = random.randint(0, len(Days)-1)
                ran_hour = random.randint(0, self.lessons-1)
                if isinstance(self.table[0][ran_year, ran_day, ran_hour], list) and ran_year is not None and ran_day is not None and ran_hour is not None:
                    break

            if isinstance(self.table[0][ran_year, ran_day, ran_hour], list) and ran_year is not None and ran_day is not None and ran_hour is not None:
                ran_sub = self.table[0][ran_year][ran_day][ran_hour][3]
                classroom = random.choice(list(ran_sub.get_c()))
                y, t, c, sub = self.table[0][ran_year, ran_day, ran_hour]
                if isinstance(self.table[2][classroom, ran_day, ran_hour], list):
                    if c in self.table[2][classroom, ran_day, ran_hour][3].get_c():
                        y_prev = self.table[2][classroom, ran_day, ran_hour][0]
                        self.table[0][y_prev, ran_day, ran_hour][2] = c
                        self.table[0][y, ran_day, ran_hour][2] = classroom
                        self.table[1][t, ran_day, ran_hour][2] = classroom
                        self.table[2][classroom, ran_day, ran_hour] = [y, t, classroom, sub]
                elif isinstance(self.table[2][classroom, ran_day, ran_hour], int):
                    self.table[0][y, ran_day, ran_hour][2] = classroom
                    self.table[1][t, ran_day, ran_hour][2] = classroom
                    self.table[2][classroom, ran_day, ran_hour] = [y, t, classroom, sub]

    def neighbour_change_teacher(self):
        list_of_lacking_teachers: List[List[int]] = []

        # znajduje lekcje gdzie nie ma nauczyciela
        for year in range(self.table[0].shape[0]):
            for day in Days:
                for lesson_hour in range(self.lessons):
                    if isinstance(self.table[0][year][day][lesson_hour], list) and \
                            self.table[0][year][day][lesson_hour][1] is None:
                        list_of_lacking_teachers.append([year, day, lesson_hour, self.table[0][year][day][lesson_hour][3]])

        # wybiera losowo lekcje i losowo nauczyciela
        if list_of_lacking_teachers:
            ran_lesson_lack = random.choice(list_of_lacking_teachers)
            teach = random.choice(ran_lesson_lack[3].get_t())

            # wpisanie nowego nauczyciela
            y, t, c, sub = self.table[0][ran_lesson_lack[0], ran_lesson_lack[1], ran_lesson_lack[2]]
            if isinstance(self.table[1][teach, ran_lesson_lack[1], ran_lesson_lack[2]], list):
                y_prev = self.table[1][teach, ran_lesson_lack[1], ran_lesson_lack[2]][0]
                self.table[0][y_prev, ran_lesson_lack[1], ran_lesson_lack[2]][1] = t
            self.table[0][y, ran_lesson_lack[1], ran_lesson_lack[2]][1] = teach
            self.table[1][teach, ran_lesson_lack[1], ran_lesson_lack[2]] = [y, teach, c, sub]
            if c is not None and isinstance(self.table[2][c, ran_lesson_lack[1], ran_lesson_lack[2]], list):
                self.table[2][c, ran_lesson_lack[1], ran_lesson_lack[2]][1] = teach
        else:
            ran_year = None
            ran_day = None
            ran_hour = None
            for i in range(50):
                ran_year = random.randint(0, self.table[0].shape[0]-1)
                ran_day = random.randint(0, len(Days)-1)
                ran_hour = random.randint(0, self.lessons-1)
                if isinstance(self.table[0][ran_year, ran_day, ran_hour], list) and ran_year is not None and ran_day is not None and ran_hour is not None:
                    break

            if isinstance(self.table[0][ran_year, ran_day, ran_hour], list) and ran_year is not None and ran_day is not None and ran_hour is not None:
                ran_sub = self.table[0][ran_year][ran_day][ran_hour][3]
                teach = random.choice(list(ran_sub.get_t()))
                y, t, c, sub = self.table[0][ran_year, ran_day, ran_hour]
                if isinstance(self.table[1][teach, ran_day, ran_hour], list):
                    if t in self.table[1][teach, ran_day, ran_hour][3].get_t():
                        y_prev = self.table[1][teach, ran_day, ran_hour][0]
                        self.table[0][y_prev, ran_day, ran_hour][1] = t
                        self.table[0][y, ran_day, ran_hour][1] = teach
                        self.table[1][teach, ran_day, ran_hour] = [y, teach, c, sub]
                        self.table[2][c, ran_day, ran_hour][2] = teach
                elif isinstance(self.table[1][teach, ran_day, ran_hour], int):
                    self.table[0][y, ran_day, ran_hour][1] = teach
                    self.table[1][teach, ran_day, ran_hour] = [y, teach, c, sub]
                    self.table[2][c, ran_day, ran_hour][2] = teach

# Funkcje do utowrzenia funkcji celu

    def beginning_time(self):
        delay_time_for_classes: List[int] = []
        for year in range(self.table[0].shape[0]):  # dla każdej klasy
            delay = 0  # opóźneinie w rozpoczęciu
            for day in Days:
                for lesson_hour in range(self.lessons):
                    if isinstance(self.table[0][year][day][lesson_hour], list):
                        break
                    delay += 1  # im wie
            delay_time_for_classes.append(delay)
        return delay_time_for_classes

    def finishing_time(self):  #
        delay_time_for_classes: List[int] = []
        for year in range(self.table[0].shape[0]):  # dla każdej klasy
            delay = 0  # opóźneinie w zakonczeniu
            for day in Days:
                delay_in_current_day = 0
                for lesson_hour in reversed(range(self.lessons)):
                    if isinstance(self.table[0][year][day][lesson_hour], list):
                        break
                    delay -= 1  # im mniejszy bd dealy tym lepiej można ewentualnie zrobić delay_time_for_classes = delay_time_for_classes - [min(delay_time_for_classes) for i in range(len(delay_time_for_classes))]
                    delay_in_current_day -= 1
                if delay_in_current_day == -6: delay += 6
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
                for lesson_hour in range(self.lessons):
                    if isinstance(self.table[0][year][day][lesson_hour], list) and self.table[0][year][day][lesson_hour][1] is None:
                        num += 1
            number_of.append(num)
        return number_of

    def lack_of_rooms(self):
        number_of: List[int] = []
        for year in range(self.table[0].shape[0]):  # dla każdej klasy
            num = 0  # opóźneinie w rozpoczęciu
            for day in Days:
                for lesson_hour in range(self.lessons):
                    if isinstance(self.table[0][year][day][lesson_hour], list) and self.table[0][year][day][lesson_hour][2] is None:
                        num += 1
            number_of.append(num)
        return number_of

    def many_teachers(self):
        number_of: List[int] = []
        for year in range(self.table[0].shape[0]):  # dla każdej klasy
            num = 0  # ilość różnych nauczycieli prowadzących ten sam przedmiot dal tej samej klasy
            other_teachers = {} #inni naczyciele którzy zostali przypisani do klasy
            for day in Days:
                for lesson_hour in range(self.lessons):
                    if isinstance(self.table[0][year][day][lesson_hour], list) and self.table[0][year][day][lesson_hour][1] is not None:
                        if self.table[0][year, day, lesson_hour][3].name not in other_teachers:
                            other_teachers[self.table[0][year, day, lesson_hour][3].name] = []
                        if self.table[0][year][day][lesson_hour][1] not in other_teachers[self.table[0][year, day, lesson_hour][3].name]:
                            other_teachers[self.table[0][year, day, lesson_hour][3].name].append(self.table[0][year][day][lesson_hour][1])
            for values in other_teachers.values():
                num += len(values)
            num -= len(list(other_teachers.values()))
            number_of.append(num)
        return number_of

    def objective_fun(self, weights: List[int]):
        beginning_time = [i * weights[0] for i in self.beginning_time()]
        # finishing_time = [i * weights[1] for i in self.finishing_time()]
        windows = [i * weights[1] for i in self.windows()]
        lack_of_teachers = [i * weights[2] for i in self.lack_of_teacher()]
        lack_of_classrooms = [i * weights[3] for i in self.lack_of_rooms()]
        many_teachers = [i * weights[4] for i in self.many_teachers()]
        fun_val_for_years = []
        for i in range(self.table[0].shape[0]):
            val = beginning_time[i] + windows[i] + lack_of_teachers[i] + lack_of_classrooms[i] + many_teachers[i]
            fun_val_for_years.append(val)
        mean = sum(fun_val_for_years)/len(fun_val_for_years)
        return mean


def get_number_of_windows(list_of_lesson_hours: List):
    general_windows_counter = 0
    windows_counter = 0
    lessons_started = False
    window_might_happend = False
    for lesson_hours in list_of_lesson_hours:
        if lessons_started and isinstance(lesson_hours, int):
            window_might_happend = True
            windows_counter += 1
        if isinstance(lesson_hours, list):
            lessons_started = True
            if window_might_happend:
                general_windows_counter += windows_counter
                windows_counter = 0
    return general_windows_counter
