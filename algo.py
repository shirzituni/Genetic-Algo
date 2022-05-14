import random

import numpy as np
from random import randint
from operator import itemgetter

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

    # print(inequality_signs)
    # print(coordinates_values)
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


def sort_list(input_list):
    # Sort the list
    Len = len(input_list)
    for i in range(0, Len):
        for j in range(0, (Len - i - 1)):
            if input_list[j][1] > input_list[j + 1][1]:
                temp = input_list[j]
                input_list[j] = input_list[j + 1]
                input_list[j + 1] = temp
    return input_list


def calculate_mismatch(matrix_input, inequality_signs_input):
    black_points = 0
    # black point for mismatch for the inequality sign
    return calculate_uncorrect_inequality_signs(matrix_input, inequality_signs_input)


def calculate_uncorrect_inequality_signs(matrix_input, inequality_signs_input):
    uncorrect = 0
    for number_set in inequality_signs_input:
        if matrix_input[number_set[0] - 1, number_set[1] - 1] < matrix_input[number_set[2] - 1, number_set[3] - 1]:
            uncorrect += 1
    return uncorrect


def calculate_duplicates_row_col(matrix_input):
    matrix_t = matrix_input.transpose()
    duplicates_in_cols = [len(matrix_t[i]) - len(np.unique(matrix_t[i])) for i in range(matrix_t[0].size)]
    total_dups = sum(duplicates_in_cols)
    return total_dups


def hybridization(list_of_matrices_and_score, matrix_size, inequality_signs_input):
    # list_of_matrixes.reverse()
    result_matrices = []

    list_of_matrices_and_score = list_of_matrices_and_score[0:90]
    top_ten_score_matrices = list_of_matrices_and_score[0:10]
    for i in range(10):
        score = calculate_mismatch(top_ten_score_matrices[i][0], inequality_signs_input)
        result_matrices.append((top_ten_score_matrices[i][0], score))

    # hybridization between the top-10
    for i in range(10):
        new_matrix_hybridization_from_top_ten = np.zeros(shape=(matrix_size, matrix_size), dtype='int')
        for j in range(matrix_size):
            new_matrix_hybridization_from_top_ten[j] = \
                top_ten_score_matrices[randint(0, len(top_ten_score_matrices) - 1)][0][randint(0, matrix_size - 1)]
            # calculate the score of the matrix
        score = calculate_mismatch(new_matrix_hybridization_from_top_ten, inequality_signs_input)
        result_matrices.append((new_matrix_hybridization_from_top_ten, score))

    # hybridization between the top-40
    list_of_matrices_part_1 = list_of_matrices_and_score[0:40]

    for i in range(80):
        new_matrix_hybridization = np.zeros(shape=(matrix_size, matrix_size), dtype='int')
        for j in range(matrix_size):
            new_matrix_hybridization[j] = \
                list_of_matrices_part_1[randint(0, len(list_of_matrices_part_1) - 1)][0][randint(0, matrix_size) - 1]
            # calculate the score of the matrix
        score = calculate_mismatch(new_matrix_hybridization, inequality_signs_input)
        result_matrices.append((new_matrix_hybridization, score))

    sort_list(result_matrices)
    # print("\n")
    # print(result_matrices, "\n", len(result_matrices))
    return result_matrices


def create_first_gen(matrix_input, inequality_signs_input):
    scores_list = []
    boards = []
    for i in range(100):
        temp_matrix = matrix_input.copy()
        for row in temp_matrix:
            generate_row(row, len(row))
            boards.append(temp_matrix)

        # print("matrix", i, "\n", temp_matrix)
        # print(calculate_duplicates_row_col(temp_matrix))
        # print("inequality_signs" , calculate_uncorrect_inequality_signs(temp_matrix, inequality_signs_input))
        score = calculate_mismatch(temp_matrix, inequality_signs_input) + calculate_duplicates_row_col(temp_matrix)
        print(f"{temp_matrix}, duplicates: {score}")

        # print(temp_matrix, score)
        scores_list.append((temp_matrix, score))

    sort_list(scores_list)
    return boards, scores_list


def create_new_generation(list_of_matrixes):
    # take the the best 10 matrix
    best_from_previous_generation = list_of_matrixes[0:10]


if __name__ == "__main__":
    matrix_size, coordinates_values, inequality_signs = get_data('example.txt')
    matrix = build_matrix(matrix_size, coordinates_values)
    # calculate_mismatch(matrix, inequality_signs, coordinates_values)

    # print(f"original matrix: \n {matrix}")
    boards, matrix_scores_list = create_first_gen(matrix, inequality_signs)
    # new_generation = create_new_generation(matrix_scores_list)
    hybridization(matrix_scores_list, matrix_size, inequality_signs)
