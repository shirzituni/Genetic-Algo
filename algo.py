import random

import numpy as np

NUMBER_OF_DIGITS_ROW = 2


def get_data(path):
    with open(path) as f:
        lines = f.readlines()
    matrix_size = int(lines[0])
    number_of_digits = int(lines[1])
    coordinates_values = []
    for i in range(NUMBER_OF_DIGITS_ROW, NUMBER_OF_DIGITS_ROW + number_of_digits):
        temp_set = []
        number_of_lines = len(lines) + 1
        for j in lines[i]:
            if j != ' ' and j != '\n':
                temp_set.append(int(j))
        coordinates_values.append(temp_set)
    inequality_signs = []
    number_rows_before_coordinate = 3 + number_of_digits
    for i in range(number_rows_before_coordinate, len(lines)):
        temp_set = []
        for j in lines[i]:
            if j != ' ' and j != '\n':
                temp_set.append(int(j))
        inequality_signs.append(temp_set)

    print(inequality_signs)
    print(coordinates_values)
    return matrix_size, coordinates_values, inequality_signs


def build_matrix(matrix_size, coordinates_value):
    matrix = np.zeros(shape=(matrix_size, matrix_size), dtype='int')
    for number_set in coordinates_value:
        matrix[number_set[0] - 1, number_set[1] - 1] = number_set[2]
    return matrix


def generate_row(row, n):
    digits = [i for i in range(1, n + 1)]
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


def create_first_gen(matrix_input):
    boards = []
    for i in range(100):
        temp_matrix = matrix_input.copy()
        for row in temp_matrix:
            generate_row(row, len(row))
            boards.append(temp_matrix)

        print("matrix", i, "\n", temp_matrix)
        print(calculate_duplicates_row_col(temp_matrix))

    return boards


def calculate_mismatch(matrix_input, inequality_signs_input):
    black_points = 0
    # black point for mismatch for the inequality sign
    return calculate_uncorrect_inequality_signs(matrix_input) + \
           calculate_uncorrect_inequality_signs(matrix_input, inequality_signs_input)


def calculate_uncorrect_inequality_signs(matrix_input, inequality_signs_input):
    uncorrect = 0
    for number_set in inequality_signs_input:
        if matrix_input[number_set[0] - 1, number_set[1] - 1] < matrix_input[number_set[2] - 1, number_set[3] - 1]:
            uncorrect += 1
    return uncorrect


def calculate_duplicates_row_col(matrix):
    duplicates_in_rows = [len(matrix[i]) - len(np.unique(matrix[i])) for i in range(matrix[0].size)]
    matrix_t = matrix.transpose()
    duplicates_in_cols = [len(matrix_t[i]) - len(np.unique(matrix_t[i])) for i in range(matrix_t[0].size)]

    total_dups = 0
    for dup in duplicates_in_rows:
        total_dups += dup

    for dup in duplicates_in_cols:
        total_dups += dup

    if total_dups == 0:
        print("No\n")
    else:
        print("Yes\n", total_dups)

    return total_dups


if __name__ == "__main__":
    matrix_size, coordinates_values, inequality_signs = get_data('example.txt')
    matrix = build_matrix(matrix_size, coordinates_values)
    # calculate_mismatch(matrix, inequality_signs, coordinates_values)

    print(f"original matrix: \n {matrix}")
    boards = create_first_gen(matrix)
