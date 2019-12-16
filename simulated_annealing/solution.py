class Solution:
    def __init__(self, time_array):
        self.time_array = time_array
        self.value = -1
        self.neighbors = []

    def evaluate_yourself_alone(self, ):
         self.value = 3
         # to do,

    def evaluate_yourself_delta(self, other):
        if other.value == -1:
            self.value = self.evaluate_yourself_alone()
        else:
            self.value = 4
            # to do
