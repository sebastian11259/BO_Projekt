#!/usr/bin/python
# -*- coding: utf-8 -*-
import structures as st
import copy
import random
import math
from typing import List


def sa_algorithm(temperature: float, alpha: float, eps: float, k: int, time_table: st.TimeTable, initial: int, neighbour: List[int], weights: List[int]):

    """
    :param temperature: initial temperature
    :param alpha: coefficient to decrease temperature
    :param eps: condition for the algorithm to end
    :param k: number of new results i neighbourhood of the current one
    :param time_table: an instance of TimeTable class
    :param initial: 1 or 2
    :param neighbour: a list with id's of different neighbourhoods
    :param weights: a list of weights to calculate the objective function
    :return: instance of TimeTable
    """

    if initial == 1:
        time_table.initial_1()
    elif initial == 2:
        time_table.initial_2()
    else:
        raise ValueError("Wrong initial result ID")

    T = temperature
    current_result = time_table
    current_obj_fun = current_result.objective_fun(weights)
    end_result = copy.deepcopy(current_result)
    end_obj_fun = end_result.objective_fun(weights)
    obj_fun_vector = [current_obj_fun]
    obj_fun_current_vec = [current_obj_fun]
    obj_fun_end = [current_obj_fun]

    while T > eps:
        for i in range(k):
            new_obj_fun, new_result = get_neighbours(neighbour, current_result, weights)
            obj_fun_vector.append(new_obj_fun)
            obj_fun_current_vec.append(current_obj_fun)
            obj_fun_end.append(end_obj_fun)
            delta = new_obj_fun - current_obj_fun
            if delta <= 0:
                current_result = new_result
                current_obj_fun = new_obj_fun
                if current_obj_fun < end_obj_fun:
                    end_result = current_result
                    end_obj_fun = current_obj_fun
            elif delta > 0:
                ran = random.random()
                possibility = math.e ** ((-1) * (new_obj_fun - current_obj_fun)/T)
                if possibility > ran:
                    current_result = new_result
                    current_obj_fun = new_obj_fun
        T = T * alpha

    return end_result, obj_fun_vector, obj_fun_current_vec, obj_fun_end


def get_neighbours(list_of_neigh, time_table: st.TimeTable, weights: List[int]):

    """
    :param list_of_neigh: a list of neighbourhood id's
    :param time_table: instance of TimeTable
    :param weights: a list of weights to calculate the objective function
    :return: objective function value and instance of TimeTable
    """

    obj_fun_list = []
    copy_list = []
    for i in range(len(list_of_neigh)):
        copy_list.append(copy.deepcopy(time_table))

        if list_of_neigh[i] == 1:
            copy_list[i].neighbour_change_lesson()
        # elif list_of_neigh[i] == 2:
        #     copy_list[i].neighbour_add_teach_class()
        elif list_of_neigh[i] == 2:
            copy_list[i].neighbour_change_classroom()
        elif list_of_neigh[i] == 3:
            copy_list[i].neighbour_change_teacher()
        else:
            raise ValueError("One of neighbourhood ID is wrong")

        obj_fun_list.append(copy_list[i].objective_fun(weights))

    # val, idx = min((val, idx) for (idx, val) in enumerate(obj_fun_list))
    val = random.choice(obj_fun_list)
    idx = obj_fun_list.index(val)

    return val, copy_list[idx]
