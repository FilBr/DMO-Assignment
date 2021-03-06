import numpy as np

def encoding(adj_mat, color_dict):
    n = len(adj_mat)
    encoding_matrix = np.zeros((n, n))
    # matrice encoding
    for i, mask in enumerate(adj_mat != 0):
        ts = color_dict[i] + 1
        encoding_matrix[:, i][mask] = ts
        encoding_matrix[i][i] = ts

    distance_matrix = np.zeros((n, n))
    # matrice distanze
    for i, row in enumerate(encoding_matrix):
        x = abs(row - row[i])
        mask = abs(row - row[i]) > 5
        x[mask] = 0
        distance_matrix[i] = x
    return encoding_matrix, distance_matrix
