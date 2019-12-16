from __future__ import with_statement
import mmap
import numpy as np
import itertools
import matplotlib.pyplot as plt
import networkx as nx
from networkx.algorithms.coloring import greedy_color
from itertools import combinations


def mapcount(filename):
    f = open(filename, "r+")
    buf = mmap.mmap(f.fileno(), 0)
    lines = 0
    readline = buf.readline
    while readline():
        lines += 1
    f.close()
    return lines


def encoding(adj_mat, color_dict):
    n = len(adj_mat)
    encoding_matrix = np.zeros((n, n))
    # matrice encoding
    for i, mask in enumerate(adj_mat != 0):
        ts = color_dict[i] + 1
        encoding_matrix[:, i][mask] = ts
        encoding_matrix[i][i] = ts

    distance_matrix = np.zeros((n, n))
    # matrice distanze
    for i, row in enumerate(encoding_matrix):
        x = abs(row - row[i])
        mask = abs(row - row[i]) > 5
        x[mask] = 0
        distance_matrix[i] = x
    return encoding_matrix, distance_matrix


def switch_exams(enc, index_pair):
    d = np.diag(enc)
    list_fs = []
    for pair in list(index_pair):
        if d[pair[0]] != d[pair[1]]:
            # print(enc[pair[0], :], d[pair[1]])
            p = (enc[pair[0], :] == d[pair[1]])
            p1 = (enc[pair[1], :] == d[pair[0]])
            if any(p) == False and any(p1) == False:
                # list of feasible neighbour solution
                dd = d.copy()
                dd[[pair[0], pair[1]]] = dd[[pair[1], pair[0]]]
                list_fs.append(dd)
    return list_fs


def mutation_exams(enc, time_slot, n):
    d = np.diag(enc)
    list_fs = []
    for i in range(n):
        diff = np.setdiff1d(range(1, time_slot + 1), enc[i, :])
        if len(diff > 0):
            diff = min(diff)
            dd = d.copy()
            dd[i] = diff
            list_fs.append(dd)
    return list_fs


if __name__ == "__main__":
    for instance_number in ['01', '02', '03', '04', '05', '06', '07', '08']:
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
        print("---Dictionary created---")

        for exam_list in stud_per_exam.values():
            for pair in itertools.combinations(exam_list, 2):
                adj_mat[pair[0] - 1, pair[1] - 1] += 1
        G = nx.from_numpy_matrix(adj_mat)

        with open(f"./instances/instance{instance_number}.slo", "r") as timeslots_file:
            max_col = int(timeslots_file.readline())
        print(f"Maximum number of colors is {max_col}")
        # strategies=[]
        # best_strategy = ""
        # num_col=max_col+1
        # best_col_dict={}
        # best_num_col = max_col
        color_dict = greedy_color(G, strategy='smallest_last', interchange=True)
        num_col = len(set(color_dict.values()))

        if num_col > max_col:
            print("NUMBER OF TIMESLOTS EXCEEDED")
        else:
            print(f"Timeslots used: {num_col}\n")

        # if tmp_num_col <= best_num_col:
        #     best_strategy = strategy
        #     best_num_col = tmp_num_col
        #     best_col_dict = tmp_color_dict
        # if best_num_col > max_col:
        #     print(f"Best strategy is not good enough")
        # else:
        #     print(f"{best_strategy}: {best_num_col}\n\n")

        with open(f"./instances/instance{instance_number}.sol", "w+") as solution_file:
            for exam in color_dict:
                solution_file.write(f"{exam + 1} {color_dict[exam] + 1}\n")

        encoding_matrix, distance_matrix = encoding(adj_mat, color_dict)
        index_pair = combinations(range(n), 2)
        list_fs_sw = switch_exams(encoding_matrix, index_pair)
        # print(list_fs_sw)
        list_fs_mut = mutation_exams(encoding_matrix, max_col, n)
        # print(list_fs_mut)
