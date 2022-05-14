import random

import numpy as np

NUMBER_OF_DIGITS_ROW = 2

def get_data(path):
    with open(path) as f:
        lines = f.readlines()
    matrix_size = int(lines[0])
    number_of_digits = int(lines[1])
    coordinates_value = []
    for i in range(NUMBER_OF_DIGITS_ROW, NUMBER_OF_DIGITS_ROW + number_of_digits):
        temp_set = []
        for j in lines[i]:
            if j != ' ' and j != '\n':
                temp_set.append(int(j))
        coordinates_value.append(temp_set)
    inequality_signs = []

    for i in range(3 + number_of_digits, len(lines)):
        temp_set = []
        for j in lines[i]:
            if j != ' ' and j != '\n':
                temp_set.append(int(j))
        inequality_signs.append(temp_set)

    print(inequality_signs)
    print(coordinates_value)
    return matrix_size, coordinates_value, inequality_signs


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
