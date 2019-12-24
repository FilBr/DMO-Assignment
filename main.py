from __future__ import with_statement
import mmap
import numpy as np
import itertools
import matplotlib.pyplot as plt
import networkx as nx
from networkx.algorithms.coloring import greedy_color
from itertools import combinations
import random

from initialization.mapcount import mapcount
from initialization.encoding import encoding
from neighborhood.mutation import mutation_exams
from neighborhood.switch import switch_exams
from neighborhood.mutation import mutation_exams
from neighborhood.switch import switch_exams
from simulated_annealing.solution import Solution
from simulated_annealing.simulated_annealing import Simulated_annealing

if __name__ == "__main__":
    for instance_number in ['01']:
        print(f"Instance {instance_number}")
        n = mapcount(f"./instances/instance{instance_number}.exm")
        adj_mat = np.zeros(shape=(n, n), dtype=np.int16)
        with open(f"./instances/instance{instance_number}.stu", "r") as enrollments_file:
            enrollments_file.readline()
            dataset = np.loadtxt(enrollments_file, delimiter=" ", dtype=str)
        print("---Dataset created---")

        stud_per_exam = {}
        for line in dataset:
            if line[0] not in stud_per_exam:
                stud_per_exam[line[0]] = []
            stud_per_exam[line[0]].append(int(line[1]))
        num_students = len(stud_per_exam)
        print("---Dictionary created---")

        for exam_list in stud_per_exam.values():
            for pair in itertools.combinations(exam_list, 2):
                adj_mat[pair[0] - 1, pair[1] - 1] += 1
                adj_mat[pair[1] - 1, pair[0] - 1] += 1
        G = nx.from_numpy_matrix(adj_mat)

    # adj_mat=np.array([[0,1,0,2,6],[1,0,5,2,0],[0,5,0,10,0],[2,2,10,0,7],[6,0,0,7,0]])
    #
    # num_students=70
    G = nx.from_numpy_matrix(adj_mat)
    with open(f"./instances/instance{instance_number}.slo", "r") as timeslots_file:
        max_col = int(timeslots_file.readline())
    print(f"Number of colors used: {max_col}")

    color_dict = greedy_color(G, strategy='smallest_last', interchange=True)
    num_col = len(set(color_dict.values()))
    first_sol = np.zeros(len(color_dict))
    for exam in color_dict:
        first_sol[int(exam)] = color_dict[exam] +1

    # Write initial solution
    with open(f"./instances/instance{instance_number}.sol", "w+") as solution_file:
        for exam in color_dict:
            solution_file.write(f"{exam + 1} {color_dict[exam] + 1}\n")

    initial_solution = Solution(adj_mat, max_col, num_students, time_array = first_sol, initial=True)

    simulated_annealing = Simulated_annealing(10000, initial_solution)
    #simulated_annealing = Simulated_annealing(100, initial_solution)
    solution = simulated_annealing.run(n)
    timeslots = solution.get_solution()
    # prova commit
    with open(f"./instances/instance{instance_number}.sol", "w+") as solution_file:
        for exam, timeslot in enumerate(timeslots):
            solution_file.write(f"{exam+1} {int(timeslot)}\n")
