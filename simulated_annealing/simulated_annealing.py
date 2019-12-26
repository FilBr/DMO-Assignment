from math import exp
import numpy as np
import random

from simulated_annealing import solution as sol


class Simulated_annealing:

    def __init__(self, max_n_iteration, initial_solution):
        import numpy as np
        self.temp = 0
        #abs(initial_solution.get_penalty() - initial_solution.avg_neighbourhood_penalty()) / 0.6931
        # calculate the initial temperature
        self.counter = 0
        self.plateau_size = 0 #20 * len(initial_solution.get_neighbours())
        self.plateau_counter = 0
        self.alpha = 0.999
        self.decay_time = max_n_iteration
        self.solution = initial_solution
        #self.neighborhood = initial_solution.get_neighbours()
        self.avg_solution_penalty = 0
        self.initial_solution_penalty = initial_solution.get_penalty()

    def solution_update(self,num_mutation,iteration_equal):
        import random
        neighbourhood=[]
        delta_neighbourhood=[]
        # create a neighboorhood for local search -> fixed size=5, because otherwise it will take too long time
        for i in range(10):
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
            iteration_equal=0
        else:
            iteration_equal+=1
        return iteration_equal

    def warming_solution_update(self, max_iterations,num_mutation):
        k = 0
        for i in range(1, max_iterations):
            new_solution = self.solution.get_random_neighbour(num_mutation)
            self.avg_solution_penalty += new_solution.get_penalty()
            if random.uniform(0, 1) > 0.4:
                k += 1
                self.solution = new_solution
        avg = self.avg_solution_penalty / max_iterations
        self.temp = abs(self.initial_solution_penalty - avg) / 0.6931
        self.plateau_size = 10 * k
        print(f"Warming up completed, {k} solutions accepted , initial temperature set as {self.temp}")

    def solution_update_exp(self,num_mutation):
        new_solution = self.solution.get_random_neighbour(num_mutation)
        delta = new_solution.get_penalty() - self.solution.get_penalty()
        if random.uniform(0, 1) < np.exp(-delta / self.temp):
            self.solution = new_solution

    def run(self,num_exams):
        num_mutation = round(num_exams /4)
        self.warming_solution_update(500,num_mutation)
        # count how many times I have mantained the same solution
        iteration_equal=0
        while self.counter != self.decay_time and round(self.temp, 100) > 0:
            iteration_equal=self.solution_update(num_mutation,iteration_equal)
            if iteration_equal>=self.plateau_size*0.01:
                # bang of temperature if I'm stucked in a local minima
                self.temp=2*self.temp
                print(f"temperature bang up to {self.temp}")
                iteration_equal=0
            if self.plateau_size != self.plateau_counter:
                self.counter += 1
                self.plateau_counter += 1

            else:
                num_mutation = round(num_mutation-num_mutation/3)
                if num_mutation==0:
                    num_mutation=1
                    iteration_equal = 0
                print(f"iteration {self.counter} | score {self.solution.get_penalty()} | current temperature {self.temp}, mutation used are {num_mutation}")
                self.plateau_counter = 0
                self.temp = self.temp * self.alpha ** self.counter
        print(f"simulated annealing completed, temperature is {self.temp} and penalty is {self.solution.get_penalty()}")
        return self.solution
