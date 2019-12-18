from math import exp

from initialization.encoding import encoding
from simulated_annealing import solution as sol


class Simulated_annealing:

    def __init__(self, temp, decay, max_n_iteration, initial_solution):
        import numpy as np
        self.temp = (
                            initial_solution.get_penalty() - initial_solution.avg_neighbourhood_penalty()) / 0.6931  # calculate the initial temperature
        self.counter = 0
        self.plateau_size = 15 * len(initial_solution.get_neighbours())
        self.plateau_counter = 0
        self.alpha = 0.99
        self.decay_time = max_n_iteration
        self.solution = initial_solution
        self.neigborhood = initial_solution.get_neighbours()

    def solution_update(self):
        import random
        new_solution = self.solution.get_random_neighbour()
        delta = new_solution.get_penalty() - self.solution.get_penalty()
        if random.uniform(-10, 0) < -delta / self.temp:
            self.solution = new_solution

    def solution_update_exp(self):
        import random
        new_solution = self.solution.get_random_neighbour()
        delta = new_solution.get_penalty() - self.solution.get_penalty()
        if random.uniform(-10, 0) < -delta / self.temp:
            self.solution = new_solution

    def run(self):
        self.solution_update()
        while self.counter != self.decay_time:
            print(f"iteration {self.counter} | score {self.solution.get_penalty()}") if i % 10 else False
            if self.plateau_size != self.plateau_counter:
                self.counter += 1
                self.plateau_counter += 1
            else:
                self.plateau_counter = 0
                self.temp = self.temp * self.alpha ** self.counter
        print(f"simulated annealing completed, temperature is {self.temp} and penalty is {self.solution.get_penalty()}")
