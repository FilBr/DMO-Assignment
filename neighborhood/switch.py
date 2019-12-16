import numpy as np

def switch_exams(enc, index_pair):
    solution = np.diag(enc)
    feasible_solutions = []
    for pair in list(index_pair):
        if solution[pair[0]] != solution[pair[1]]:
            # print(enc[pair[0], :], d[pair[1]])
            p = (enc[pair[0], :] == solution[pair[1]])
            p1 = (enc[pair[1], :] == solution[pair[0]])
            if any(p) == False and any(p1) == False:
                # list of feasible neighbour solution
                tmp_solution = solution.copy()
                tmp_solution[[pair[0], pair[1]]] = tmp_solution[[pair[1], pair[0]]]
                feasible_solutions.append(tmp_solution)
    return feasible_solutions
