from typing import List
import numpy as np
from copy import deepcopy

def reduce_and_get_sum(matrix: np.array) -> np.array:
    reduction_sum = 0
    size = len(matrix)
    for row in range(size):
        min_value = min(matrix[row])
        reduction_sum += min_value
        for col in range(size):
            matrix[row][col] -= min_value
    return reduction_sum, matrix

def reduce_matrix(matrix: np.array) -> np.array:
    reduction_sum, matrix = reduce_and_get_sum(matrix)
    matrix = matrix.T
    reduction_sum += reduce_and_get_sum(matrix)[0]
    return matrix.T, reduction_sum

def min_lines(matrix: np.array, size: int) -> (List[int], List[int]):
    independent_row = []
    independent_col = []

    for row in range(size):
        for col in range(size):
            if (matrix[row][col] == 0) and (row not in independent_row) and (col not in independent_col):
                if list(matrix[row]).count(0) > 1:
                    independent_row.append(row)
                    break
                if list(matrix[:, col]).count(0) > 1:
                    independent_col.append(col)
                    break
                independent_row.append(row)
                break

    return independent_row, independent_col

def create_additional_zeros(matrix: np.array, independent_row: List[int], independent_col: List[int]) -> np.array:
    min_element = np.inf
    size = len(matrix)
    
    for row in range(size):
        for col in range(size):
            if (row not in independent_row) and (col not in independent_col):
                if matrix[row, col] < min_element:
                    min_element = matrix[row, col]
    
    for row in range(size):
        for col in range(size):
            if (row not in independent_row) and (col not in independent_col):
                matrix[row, col] -= min_element
            elif (row in independent_row) and (col in independent_col):
                matrix[row, col] += min_element
    
    return matrix

def get_total_cost(matrix: np.array, base_matrix: np.array) -> (List[tuple], int):
    optimal_points = []
    total_cost = 0
    size = len(matrix)
    
    rows = []
    for i in range(size):
        for row in range(size):
            if list(matrix[row]).count(0) == i+1:
                rows.append(row)

    chosen_col = []
    chosen_row = []
    for row in rows:
        minimal_zeros = np.inf
        best_candidate = []
        for col in range(size):
            if (matrix[row, col] == 0) and (col not in chosen_col):
                number_of_zeros = sum(1 for col_row in range(size) if (matrix[col_row, col] == 0) and (col_row not in chosen_row))
                if number_of_zeros < minimal_zeros:
                    minimal_zeros = number_of_zeros
                    best_candidate = [row, col]

        optimal_points.append((best_candidate[0], best_candidate[1]))
        total_cost += base_matrix[best_candidate[0], best_candidate[1]]
        chosen_row.append(best_candidate[0])
        chosen_col.append(best_candidate[1])

    return optimal_points, total_cost

def hungarian_method(matrix: np.array) -> (List[tuple], int):
    base_matrix = deepcopy(matrix)
    matrix, reduction_sum = reduce_matrix(matrix)
    
    independent_row, independent_col = min_lines(matrix, len(matrix))
    
    while True:
        if len(independent_col) + len(independent_row) == len(matrix):
            return get_total_cost(matrix, base_matrix)
        else:
            matrix = create_additional_zeros(matrix, independent_row, independent_col)
            independent_row, independent_col = min_lines(matrix, len(matrix))

# Test
if __name__ == '__main__':
    matrix_example = np.array([[4,  6,  6,  5, 10,  6,  7],
                               [7, 13, 10,  9, 15, 12, 14],
                               [7, 13, 13, 13,  9, 12, 11],
                               [0, 10,  6,  8,  5,  6, 12],
                               [7,  4,  8, 15, 13, 11,  5],
                               [3,  3,  4,  4,  4,  5, 10],
                               [15, 12, 15, 14, 10, 12,  5]])

    print("Macierz początkowa: \n", matrix_example)
    result = hungarian_method(matrix_example)
    print("\n\nMacierz końcowa: \n", matrix_example)
    print("\n\nWynik", result)


    matrix_example = np.array([ [4,  2, 5,  7],
                                [8,  3, 10, 8],
                                [12, 5, 4,  5],
                                [6,  3, 7,  14]])

    print("Macierz początkowa: \n", matrix_example)
    result = hungarian_method(matrix_example)
    print("\n\nMacierz końcowa: \n", matrix_example)
    print("\n\nWynik", result)
