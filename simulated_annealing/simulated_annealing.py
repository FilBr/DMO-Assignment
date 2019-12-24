from math import exp
import numpy as np

from simulated_annealing import solution as sol


class Simulated_annealing:

    def __init__(self, max_n_iteration, initial_solution):
        import numpy as np
        self.temp = abs(initial_solution.get_penalty() - initial_solution.avg_neighbourhood_penalty()) / 0.6931  # calculate the initial temperature
        self.counter = 0
        self.plateau_size = 10 * len(initial_solution.get_neighbours())
        self.plateau_counter = 0
        self.alpha = 0.99
        self.decay_time = max_n_iteration
        self.solution = initial_solution
        self.neigborhood = initial_solution.get_neighbours()
        #self.temp=15000
        print(f"Initial Temperature {self.temp}, plateau size is {self.plateau_size}")

    def solution_update(self,num_mutation):
        import random
        neighbourhood=[]
        delta_neighbourhood=[]
        # create a neighboorhood for local search -> fixed size=5, because otherwise it will take too long time
        for i in range(5):
            new_solution = self.solution.get_random_neighbour(num_mutation)
            neighbourhood.append(new_solution)
            delta = new_solution.get_penalty() - self.solution.get_penalty()
            delta_neighbourhood.append(delta)
        # select the best neighbourhood: the one that mostly improves the objective function
        index=delta_neighbourhood.index(min(delta_neighbourhood))
        new_solution=neighbourhood[index]
        delta=delta_neighbourhood[index]

        if random.uniform(-10, 0) < -delta / self.temp:
            self.solution = new_solution

    def solution_update_exp(self,num_mutation):
        import random
        new_solution = self.solution.get_random_neighbour(num_mutation)
        delta = new_solution.get_penalty() - self.solution.get_penalty()
        if random.uniform(0,1) < np.exp(-delta/self.temp):
            self.solution = new_solution

    def run(self,num_exams):
        # number of mutation for neighbours that scales with number of exams
        num_mutation =round(num_exams/2)
        while self.counter != self.decay_time and self.temp > 0:
            self.solution_update(num_mutation)
            if self.plateau_size != self.plateau_counter:
                self.counter += 1
                self.plateau_counter += 1
            else:
                num_mutation = round(num_mutation / 2)
                print(
                    f"iteration {self.counter} | score {self.solution.get_penalty()} | current temperature {self.temp}")
                self.plateau_counter = 0
                self.temp = self.temp * self.alpha ** self.counter
        print(f"simulated annealing completed, temperature is {self.temp} and penalty is {self.solution.get_penalty()}")
        return self.solution
