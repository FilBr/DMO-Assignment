import numpy as np
from itertools import combinations
import random


class Solution:

    def __init__(self, adj_matrix, num_timeslots, students, 
                time_array=None, encoding=None, distance=None, objective=None, initial=False):
        if time_array is None and encoding is not None:
            self.time_array = np.diag(encoding)
        else:
            self.time_array = time_array
        self.adj_matrix = adj_matrix
        self.tot_num_students = students
        self.num_timeslots = num_timeslots
        self.n_exams = len(adj_matrix)

        if encoding is None and distance is None:
            self.encoding_matrix, self.distance_matrix = self.encoding(self.adj_matrix, time_array)
        else:
            self.encoding_matrix = encoding
            self.distance_matrix = distance

        if objective is None:
            self.penalty_matrix = self.obj_matrix(self.distance_matrix, self.adj_matrix, self.tot_num_students)
        else:
            self.penalty_matrix = objective

        if initial is True:
            self.neighbours = self.mutation_exams(self.encoding_matrix, num_timeslots, len(adj_matrix))
            self.neighbours += self.switch_exams(self.encoding_matrix, combinations(range(len(adj_matrix)), 2))

    
    # def get_random_neighbour(self):
    #     return Solution(random.sample(self.neighbours, 1)[0], self.adj_matrix, self.num_timeslots,
    #                     self.tot_num_students)

    def get_neighbours(self):
        return self.neighbours

    def get_penalty(self):
        # print(f"Solution penalty is: {sum(np.diag(self.penalty_matrix))}")
        return sum(np.diag(self.penalty_matrix))

    def avg_neighbourhood_penalty(self):
        nbhood_percent = int(1 * (len(self.neighbours)))
        random_neighbours = random.sample(self.neighbours, nbhood_percent)

        avg_penalty = 0
        for sol in random_neighbours:
            diff = np.where(sol != self.time_array)
            change_list = []
            for exam in diff[0]:
                change_list.append([exam, sol[exam]])
            delta = self.obj_compare(self.encoding_matrix, self.adj_matrix, change_list, self.penalty_matrix)
            avg_penalty += self.get_penalty() + delta
        avg_penalty /= nbhood_percent
        print(f"average penalty: {avg_penalty}, initial penalty: {sum(np.diag(self.penalty_matrix))}")
        return avg_penalty

    def get_random_neighbour(self):
        exam_touple = random.sample(range(0, self.n_exams), 2)
        candidate_time_touple = random.sample(range(1, self.num_timeslots + 1), 2)
        while self.time_array[exam_touple[0]] == candidate_time_touple[0]:
            candidate_time_touple[0] = random.randint(1, self.n_exams)
        while self.time_array[exam_touple[1]] == candidate_time_touple[1]:
            candidate_time_touple[1] = random.randint(1, self.n_exams)
        change_list = []
        for i in range(2):
            change_list.append([exam_touple[i], candidate_time_touple[i]])
        
        encoding_matrix, distance_matrix, obj_matrix =  self.overwrite(self.encoding_matrix, self.distance_matrix,
                                                                       self.obj_matrix(self.distance_matrix,self.adj_matrix,self.tot_num_students), change_list, self.adj_matrix)
        return Solution(self.adj_matrix, self.num_timeslots, self.tot_num_students, 
                            encoding = encoding_matrix, distance = distance_matrix, objective = obj_matrix)

    def encoding(self, adj_mat, color_dict):
        n = len(adj_mat)
        encoding_matrix = np.zeros((n, n))
        # matrice encoding
        for i, mask in enumerate(adj_mat != 0):
            ts = color_dict[i]
            encoding_matrix[:, i][mask] = ts
            encoding_matrix[i][i] = ts

        distance_matrix = np.zeros((n, n))
        # matrice distanze
        for i, row in enumerate(encoding_matrix):
            mask0 = row == 0
            x = abs(row - row[i])
            mask = abs(row - row[i]) > 5
            x[mask0] = 0
            x[mask] = 0
            distance_matrix[i] = x
        return encoding_matrix, distance_matrix

    def mutation_exams(self, enc, time_slot, n_exams):
        solution = np.diag(enc)
        feasible_solutions = []
        for i in range(n_exams):
            diff = np.setdiff1d(range(1, time_slot + 1), enc[i, :])
            if len(diff > 0):
                diff = min(diff)
                tmp_solution = solution.copy()
                tmp_solution[i] = diff
                feasible_solutions.append(tmp_solution)
        return feasible_solutions

    def switch_exams(self, enc, index_pair):
        solution = np.diag(enc)
        feasible_solutions = []
        for pair in list(index_pair):
            if solution[pair[0]] != solution[pair[1]]:
                # print(enc[pair[0], :], d[pair[1]])
                p = (np.delete(enc[pair[0], :], pair[1]) == solution[pair[1]])
                p1 = (np.delete(enc[pair[1], :], pair[0]) == solution[pair[0]])
                if any(p) == False and any(p1) == False:
                    # list of feasible neighbour solution
                    tmp_solution = solution.copy()
                    tmp_solution[[pair[0], pair[1]]] = tmp_solution[[pair[1], pair[0]]]
                    feasible_solutions.append(tmp_solution)
        return feasible_solutions

    ## obj_matrix is a matrix nxn, where n is the number of exams
    ## each element of the matrix is the penalty calculated between exam i and j, given they have students in common
    ## The diagonal of the matrix is the penalty contribution of each exam

    def obj_matrix(self, distance_matrix, adj_matrix, tot_students):
        n = len(distance_matrix)
        weight = 2 ** (5 - distance_matrix)
        mask = weight == 32
        weight[mask] = 0
        obj_matrix = weight * adj_matrix
        for pos, row in enumerate(obj_matrix):
            obj_matrix[pos][pos] = np.sum(row)
        return obj_matrix / (tot_students * 2)

    def obj_compare(self, encoding_matrix, adj_matrix, change_list, obj_matrix):
        # change_list è vettore di due elementi change_list[0] = exam changed, change_list[1] = time slot
        # obj_matrix è matrice con penalità x studenti
        sum_old = 0
        sum_new = 0
        for pair in change_list:
            sum_old += obj_matrix[pair[0]][pair[0]]
            row = encoding_matrix[pair[0]]
            row[pair[0]] = pair[1]  # sostituisce sulla diagonale
            mask0 = row == 0
            row = abs(row - row[pair[0]])
            mask = abs(row - row[pair[0]]) > 5
            row[mask0] = 0
            row[mask] = 0
            weight = 2 ** (5 - row)
            mask = weight == 32
            weight[mask] = 0
            sum_new += np.dot(weight, adj_matrix[pair[0]])

        return sum_old - sum_new / (2 * self.tot_num_students)

    def overwrite(self, encoding_matrix, distance_matrix, obj_matrix, change_list, adj_matrix):
        for pair in change_list:
            encoding_matrix[:, pair[0]] = pair[1]
            row = encoding_matrix[pair[0]]
            row[pair[0]] = pair[1]  # sostituisce sulla diagonale
            row = abs(row - row[pair[0]])
            mask = abs(row - row[pair[0]]) > 5
            row[mask] = 0
            distance_matrix[pair[0]] = row
            distance_matrix[:, pair[0]] = row
            obj_matrix[pair[0]] = distance_matrix[pair[0]] * adj_matrix[pair[0]]
            obj_matrix[:, pair[0]] = obj_matrix[pair[0]]
        return encoding_matrix, distance_matrix, obj_matrix

    def get_solution(self):
        return self.time_array
