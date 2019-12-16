class Simulated_annealing:

    def __init__(self, temp, decay, decay_time):
        import numpy as np
        self.temp = temp
        self.counter = 0
        self.decay = decay
        self.weight = np.exp(-(1 / self.temp))
        self.change_counter = 0
        self.decay_time = decay_time

    def temp_update(self):
        if self.counter == decay_time:
            self.temp = self.temp * self.decay
            self.change_counter += 1
            self.counter = 0
            self.weight = self.weight ** (1 / self.decay)

    def solution_update(self, sol_act, sol_new):
        import random
        delta = sol_new.value - sol_act
        if random.uniform() < self.weight ** delta:
            x_new = sol_new
        else:
            x_new = sol_act
        return x_new
