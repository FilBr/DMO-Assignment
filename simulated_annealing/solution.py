import numpy as np
from itertools import combinations
import random

class Solution:

    def __init__(self, time_array, adj_matrix, num_timeslots, students):
        self.time_array = time_array
        self.adj_matrix = adj_matrix
        self.tot_num_students = students
        self.num_timeslots = num_timeslots
        self.encoding_matrix, self.distance_matrix = self.encoding(self.adj_matrix, time_array)
        self.neighbours = self.mutation_exams(self.encoding_matrix, num_timeslots, len(adj_matrix))
        self.neighbours += self.switch_exams(self.encoding_matrix, combinations(range(len(adj_matrix)), 2))
        self.penalty_matrix = self.obj_matrix(self.distance_matrix, self.adj_matrix, self.tot_num_students)
    
    
    # def evaluate_yourself_alone(self, ):
    #      self.value = 3
    #      # to do,


    # def evaluate_yourself_delta(self, other):
    #     if other.value == -1:
    #         self.value = self.evaluate_yourself_alone()
    #     else:
    #         self.value = 4
    #         # to do


    def get_neighbours(self):
        return self.neighbours


    def get_penalty(self):
        #print(f"Solution penalty is: {sum(np.diag(self.penalty_matrix))}")
        return sum(np.diag(self.penalty_matrix))


    def avg_neighbourhood_penalty(self):
        nbhood_percent = int(1 * (len(self.neighbours)))
        random_neighbours = random.sample(self.neighbours, nbhood_percent)

        avg_penalty = 0
        for sol in random_neighbours:
            self.encoding_matrix, self.distance_matrix = self.encoding(self.adj_matrix, sol)
            self.penalty_matrix = self.obj_matrix(self.distance_matrix, self.adj_matrix, self.tot_num_students)
            curr_sol_penalty = sum(np.diag(self.penalty_matrix))
            # print(f"penalty: {curr_sol_penalty}")
            avg_penalty += curr_sol_penalty
        avg_penalty /= len(random_neighbours)
        print(f"average penalty: {avg_penalty}")
        return  avg_penalty

    def encoding(self,adj_mat, color_dict):
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
                p = (np.delete(enc[pair[0], :],pair[1]) == solution[pair[1]])
                p1 = (np.delete(enc[pair[1], :],pair[0]) == solution[pair[0]])
                if any(p) == False and any(p1) == False:
                    # list of feasible neighbour solution
                    tmp_solution = solution.copy()
                    tmp_solution[[pair[0], pair[1]]] = tmp_solution[[pair[1], pair[0]]]
                    feasible_solutions.append(tmp_solution)
        return feasible_solutions


    def obj_matrix(self, distance_matrix, adj_matrix, tot_students):
        n = len(distance_matrix)
        obj_matrix = 2**(5-distance_matrix)*adj_matrix

        ## Each element is the penalty contribution between exam i and j, 
        ## diagonal is the sum of each row -> overall penalty contribution of an exam

        for pos,row in enumerate(distance_matrix):
            obj_matrix[pos][pos] = np.sum(obj_matrix[pos])

        return obj_matrix/(tot_students*2)


    def obj_function_eval(self, distance, common_students):
        return (2**(5-distance))*common_students


    def get_random_neighbour(self):
        return Solution(random.sample(self.neighbours, 1)[0], self.adj_matrix, self.num_timeslots, self.tot_num_students)