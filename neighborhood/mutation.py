import numpy as np

def mutation_exams(enc, time_slot, n_exams):
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