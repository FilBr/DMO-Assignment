import numpy as np


def obj_compare(encoding_matrix, adj_matrix, change_list, obj_matrix):
    # change_list è vettore di due elementi change_list[0] = exam changed, change_list[1] = time slot
    # obj_matrix è matrice con penalità x studenti
    sum_old = 0
    sum_new = 0
    for pair in change_list:
        sum_old += np.sum(obj_matrix[pair[0]])
        row = encoding_matrix[pair[0]]
        row[pair[0]] = pair[1]  # sostituisce sulla diagonale
        row = abs(row - row[pair[0]])
        mask = abs(row - row[pair[0]]) > 5
        row[mask] = 0
        sum_new += np.sum(row * adj_matrix[pair[0]])

    difference = sum_old - sum_new
    if difference > 0:
        accept = True
    else:
        accept = False
    return difference, accept


def overwrite(encoding_matrix, distance_matrix, obj_matrix, change_list, adj_matrix):
    for pair in change_list:
        encoding_matrix[:, pair[0]] = pair[1]
        row = encoding_matrix[pair[0]]
        row[pair[0]] = pair[1]  # sostituisce sulla diagonale
        row = abs(row - row[pair[0]])
        mask = abs(row - row[pair[0]]) > 5
        row[mask] = 0
        distance_matrix[pair[0]] = row
        distance_matrix[:, pair[0]] = row
        obj_matrix[pair[0]] = distance_matrix[pair[0]] * adj_matrix[pair[0]]
        obj_matrix[:, pair[0]] = obj_matrix[pair[0]]
    return encoding_matrix, distance_matrix, obj_matrix

## obj_matrix is a matrix nxn, where n is the number of exams
## each element of the matrix is the penalty calculated between exam i and j, given they have students in common
## The diagonal of the matrix is the penalty contribution of each exam

def obj_matrix(distance_matrix, adj_matrix, tot_students):
    n = len(distance_matrix)
    obj_matrix = np.zeros((n, n))

    ## Each element is the penalty contribution between exam i and j, 
    ## diagonal is the sum of each row -> overall penalty contribution of an exam

    for pos,row in enumerate(distance_matrix):
        for elem in range(pos+1, n):
            if elem != 0:
                obj_matrix[pos][elem] = obj_function_eval(distance_matrix[pos][elem], adj_matrix[pos][elem])
                obj_matrix[elem][pos] = obj_matrix[pos][elem]
        obj_matrix[pos][pos] = np.sum(obj_matrix[pos])

    return obj_matrix/(tot_students*2)

def obj_function_eval(distance, common_students):
    return (2**(5-distance))*common_students
