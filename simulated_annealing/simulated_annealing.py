from initialization.encoding import encoding


class Simulated_annealing:

    def __init__(self, temp, decay, max_n_iteration, init_sol_val, avg_sol_val,initial_solution,neighborhood, adj_mat):
        import numpy as np
        self.temp = (avg_sol_val - init_sol_val) / 0.6931  # calculate the initial temperature
        self.counter = 0
        self.plateau_size = 15 * len(neighborhood)
        self.plateau_counter = 0
        self.alpha = 0.99
        self.decay_time = max_n_iteration
        self.solution = initial_solution
        self.neigborhood = neighborhood

    def temp_update(self):
        if self.counter != self.decay_time & self.plateau_size != self.plateau_counter:
            self.counter += 1
            self.plateau_counter += 1
        else:
            self.plateau_counter = 0
            self.temp = self.temp * self.alpha ** self.counter


    def solution_update(self):
        import random
        current_solution = random.sample(self.neigborhood,1)
        encoding()
        if random.uniform(-10, 0) < -delta / self.temp:
            x_new = new_solution
        else:
            x_new = last_solution
        return x_new

    def solution_update_exp(self, last_solution, new_solution):
        import random
        delta = new_solution - last_solution
        if random.uniform(0, 1) < exp(-delta / self.temp):
            x_new = new_solution
        else:
            x_new = last_solution
        return x_new

    def run(self):
        for i in range(0, self.decay_time):


