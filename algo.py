import random

import numpy as np


def get_data(path):
    with open(path) as f:
        lines = f.readlines()
    n = int(lines[0])
    digits = int(lines[1])
    cor_values = []
    for i in range(2, 2 + digits):
        temp_set = []
        for j in lines[i]:
            if j != ' ' and j != '\n':
                temp_set.append(int(j))
        cor_values.append(temp_set)
    signs_values = []
    for i in range(3 + digits, len(lines)):
        for j in lines[i]:
            if j != ' ' and j != '\n':
                signs_values.append(int(j))
    return n, cor_values, signs_values


def build_matrix(n, cor_values):
    matrix = np.zeros(shape=(n, n), dtype='int')
    for number_set in cor_values:
        matrix[number_set[0], number_set[1]] = number_set[2]
    return matrix


def generate_row(row, n):
    digits = [i for i in range(1, n+1)]
    empty_indexes = [i for i in range(5)]
    for i in range(n):
        if row[i] != 0:
            digits.remove(row[i])
            empty_indexes.remove(i)
    for i in range(len(digits)):
        index = random.choice(empty_indexes)
        digit = random.choice(digits)
        row[index] = digit
        digits.remove(digit)
        empty_indexes.remove(index)
    return row


def create_first_gen(matrix):
    boards = []
    for i in range(100):
        temp_matrix = matrix.copy()
        for row in temp_matrix:
            generate_row(row, len(row))
            boards.append(temp_matrix)

    return boards


if __name__ == "__main__":
    n, cor_values, signs_values = get_data('example.txt')
    matrix = build_matrix(n, cor_values)
    print(f"original matrix: \n {matrix}")
    boards = create_first_gen(matrix)
