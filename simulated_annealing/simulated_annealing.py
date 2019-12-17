class Simulated_annealing:

    def __init__(self, temp, decay, max_n_iteration, hood_size, init_sol_val, avg_sol_val ):
        import numpy as np
        self.temp = (avg_sol_val - init_sol_val) / 0.6931  # calculate the initial temperature
        self.counter = 0
        self.plateau_size = 15 * hood_size
        self.plateau_counter = 0
        self.alpha = 0.99
        self.decay_time = max_n_iteration

    def temp_update(self):
        if self.counter != self.decay_time & self.plateau_size != self.plateau_counter:
            self.temp = self.temp * self.alpha ** self.counter
            self.counter += 1
            self.plateau_counter += 1
        else:
            self.plateau_counter = 0

    def solution_update(self, last_solution, new_solution):
        import random
        delta = new_solution.value - last_solution
        if random.uniform() < self.weight ** delta:
            x_new = sol_new
        else:
            x_new = sol_act
        return x_new
