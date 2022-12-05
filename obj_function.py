#!/usr/bin/python
# -*- coding: utf-8 -*-
import structures
class TimeTable:
    def beginning_time(self):
        delay_time_for_classes : List[int] = []
        for year in range(self.table[0].shape[0]):# dla każdej klasy 
            delay = 0 #opóźneinie w rozpoczęciu 
            for day in Days:
                for lesson_hour in Lesson_hours:
                    if not self.time[0][year][day][lesson_hour]:
                        break
                    delay += 1# im wie
            delay_time_for_classes.append(delay)
        return delay_time_for_classes
    
    def finishing_time(self):#
        delay_time_for_classes : List[int] = []
        for year in range(self.table[0].shape[0]):# dla każdej klasy 
            delay = 0#opóźneinie w zakonczeniu 
            for day in Days:
                for lesson_hour in reversed(Lesson_hours):
                    if isinstance(self.time[0][year][day][lesson_hour], tuple):
                        break
                    delay -= 1 #im mniejszy bd dealy tym lepiej można ewentualnie zrobić delay_time_for_classes = delay_time_for_classes - [min(delay_time_for_classes) for i in range(len(delay_time_for_classes))]
            delay_time_for_classes.append(delay)
        return delay_time_for_classes
    
    def windows(self):
        delay_time_for_classes : List[int] = []
        for year in range(self.table[0].shape[0]):# dla każdej klasy 
            windows_counter = 0#opóźneinie w zakonczeniu 
            for day in Days:
                windows_counter += get_number_of_windows(self.time[0][year][day]) #im mniejszy bd dealy tym lepiej
            delay_time_for_classes.append(windows_counter)
        return delay_time_for_classes
    
    def lack_of_teacher(self):
        number_of : List[int] = []
        for year in range(self.table[0].shape[0]):# dla każdej klasy 
            num = 0 #opóźneinie w rozpoczęciu 
            for day in Days:
                for lesson_hour in Lesson_hours:
                    if isinstance(self.time[0][year][day][lesson_hour], tuple) and isinstance(self.time[1][year][day][lesson_hour], None):
                        num += 1
            number_of.append(num)
        return number_of
    
    def lack_of_rooms(self):
        number_of : List[int] = []
        for year in range(self.table[0].shape[0]):# dla każdej klasy 
            num = 0 #opóźneinie w rozpoczęciu 
            for day in Days:
                for lesson_hour in Lesson_hours:
                    if isinstance(self.time[0][year][day][lesson_hour], tuple) and isinstance(self.time[2][year][day][lesson_hour], None):
                        num += 1
            number_of.append(num)
        return number_of
        
    
def get_number_of_windows(List_of_lesson_hours: List):
    general_windows_counter = 0
    windows_counter = 0
    lessons_started = False
    window_might_happend = False
    for lesson_hours in List_of_lesson_hours:
        if lessons_started and isinstance(lesson_hours, int):
            window_might_happend = True
            windows_counter += 1
        if isinstance(lesson_hours, tuple):
            lessons_started = True
            if window_might_happend:
                general_windows_counter += windows_counter
                windows_counter = 0
    return general_windows_counter
# sprawdzenie działa jak cos
# print(get_number_of_windows([0, 0, 0, 0,]))
# print(get_number_of_windows([0, (0, 0), (0, 0), 0,]))
# print(get_number_of_windows([0, (0, 0), 0, (0, 0), 0,]))
# print(get_number_of_windows([0, (0, 0), 0, 0, (0, 0), 0,]))
# print(get_number_of_windows([0, (0, 0), 0, (0, 0), 0, (0, 0), 0,]))
# print(get_number_of_windows([0, (0, 0), 0, (0, 0), 0, 0, (0, 0), 0,]))


