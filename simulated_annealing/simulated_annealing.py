from initialization.encoding import encoding
from simulated_annealing import solution as sol

class Simulated_annealing:

    def __init__(self, temp, decay, max_n_iteration, initial_solution):
        import numpy as np
        self.temp = ( initial_solution.get_penalty()-initial_solution.avg_neighbourhood_penalty()) / 0.6931  # calculate the initial temperature
        self.counter = 0
        self.plateau_size = 15 * len(initial_solution.get_neighbours())
        self.plateau_counter = 0
        self.alpha = 0.99
        self.decay_time = max_n_iteration
        self.solution = initial_solution
        self.neigborhood = initial_solution.get_neighbours()

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

        if random.uniform(-10, 0) < -delta / self.temp:
            x_new = 0
        else:
            x_new = 0
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


