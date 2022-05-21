import random
from pprint import pprint
import numpy as np
from random import randint

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

    return matrix_size, coordinates_values, inequality_signs


def build_matrix(matrix_size, coordinates_value):
    matrix = np.zeros(shape=(matrix_size, matrix_size), dtype='int')
    for number_set in coordinates_value:
        matrix[number_set[0] - 1, number_set[1] - 1] = number_set[2]
    return matrix


def generate_row(row, n):
    digits = [i for i in range(1, n + 1)]
    empty_indexes = [i for i in range(matrix_dim)]
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
    return sorted(input_list, key=lambda x: x[1])


def calculate_mismatch(matrix_input, inequality_signs_input):
    return calculate_incorrect_inequality_signs(matrix_input, inequality_signs_input) + \
           calculate_duplicates_row_col(matrix_input)


def calculate_incorrect_inequality_signs(matrix_input, inequality_signs_input):
    incorrect = 0
    for number_set in inequality_signs_input:
        if matrix_input[number_set[0] - 1, number_set[1] - 1] < matrix_input[number_set[2] - 1, number_set[3] - 1]:
            incorrect += 1
    return incorrect


def calculate_duplicates_row_col(matrix_input):
    duplicates_in_rows = [len(matrix_input[i]) - len(np.unique(matrix_input[i])) for i in range(matrix_input[0].size)]
    matrix_t = matrix_input.transpose()
    duplicates_in_cols = [len(matrix_t[i]) - len(np.unique(matrix_t[i])) for i in range(matrix_t[0].size)]

    total_duplicates = 0
    for duplicate in duplicates_in_rows:
        total_duplicates += duplicate

    for duplicate in duplicates_in_cols:
        total_duplicates += duplicate

    return total_duplicates


def cross_over(list_of_matrices, matrix_size_input, inequality_signs_input):
    result_matrices = []
    for i in range(len(list_of_matrices)):
        father_matrix_index = randint(0, len(list_of_matrices) - 1)
        mother_matrix_index = randint(0, len(list_of_matrices) - 1)
        new_matrix_hybridization_from_top_ten = np.zeros(shape=(matrix_size_input, matrix_size_input), dtype='int')
        for j in range(matrix_size_input):
            random_row_index = randint(0, matrix_size_input - 1)
            random_parent = (randint(0, len(list_of_matrices) - 1)) % 2
            if random_parent == 1:
                new_matrix_hybridization_from_top_ten[j] = \
                    list_of_matrices[mother_matrix_index][0][random_row_index]
            else:
                new_matrix_hybridization_from_top_ten[j] = \
                    list_of_matrices[father_matrix_index][0][random_row_index]
        # calculate the score of the matrix
        score = calculate_mismatch(new_matrix_hybridization_from_top_ten, inequality_signs_input)
        result_matrices.append((new_matrix_hybridization_from_top_ten, score))
    return result_matrices


def solve_problem(curr_generation):
    """
    # 30 pick best
    # 20 totaly new like first gen
    # =
    # 50 send to hybridization
    """
    matrix_to_hyrid = []
    next_generation = []

    base_matrix = build_matrix(matrix_dim, coordinates_values_given_numbers)
    best_30 = curr_generation[:30]
    new_20 = create_first_gen(base_matrix, inequality_signs)[:20]
    matrix_to_hyrid.extend(best_30)
    matrix_to_hyrid.extend(new_20)
    next_generation.extend(best_30)
    next_generation.extend(new_20)
    next_generation.extend(cross_over(list_of_matrices=matrix_to_hyrid, matrix_size_input=matrix_dim,
                                      inequality_signs_input=inequality_signs))
    return sort_list(next_generation)


def create_mutation(matrices_to_mutate, matrix_size, coordinates_value):
    for matrix, score in matrices_to_mutate:
        for row_idx in range(matrix_size):
            for col_idx in range(matrix_size):
                random_num = randint(1, 10)
                # probability of a half to mutation
                if random_num < 2:
                    matrix[row_idx, col_idx] = randint(1, matrix_size)
                for number_set in coordinates_value:
                    matrix[number_set[0] - 1, number_set[1] - 1] = number_set[2]
    return matrices_to_mutate


def create_first_gen(matrix_input, inequality_signs_input):
    matrix_and_score_list = []
    boards = []
    for i in range(100):
        temp_matrix = matrix_input.copy()
        for row in temp_matrix:
            generate_row(row, len(row))
            boards.append(temp_matrix)
        score = calculate_mismatch(temp_matrix, inequality_signs_input)
        matrix_and_score_list.append((temp_matrix, score))

    matrix_and_score_list = sort_list(matrix_and_score_list)
    return matrix_and_score_list


def create_new_generation(list_of_matrices_and_score, matrix_size, inequality_signs_input):
    new_gen_matrices = []

    # append the top-10 from the previous generation to the next
    top_ten_score_matrices = list_of_matrices_and_score[:10]
    new_gen_matrices.extend(top_ten_score_matrices)

    forty_top_score_matrices = list_of_matrices_and_score[:40]

    hybrid_top_ten_matrices = cross_over(top_ten_score_matrices, matrix_size, inequality_signs_input)
    hybrid_top_forty_matrices = cross_over(forty_top_score_matrices, matrix_size, inequality_signs_input)
    hybrid_top_forty_matrices_2 = cross_over(forty_top_score_matrices, matrix_size, inequality_signs_input)

    new_gen_matrices.extend(hybrid_top_ten_matrices)
    new_gen_matrices.extend(hybrid_top_forty_matrices)
    new_gen_matrices.extend(hybrid_top_forty_matrices_2)

    """ Total:
        10 from the generation before
        10 created by cross_over
        40 created by cross_over
        40 created by cross_over
        ---------------------
        100 new matrix for next generation
    """

    result_matrices_with_score = []
    for mutation_matrix, score in new_gen_matrices:
        new_score = calculate_mismatch(mutation_matrix, inequality_signs_input)
        result_matrices_with_score.append((mutation_matrix, new_score))
    result_matrices_with_score = sort_list(result_matrices_with_score)
    return result_matrices_with_score


if __name__ == "__main__":
    matrix_dim, coordinates_values_given_numbers, inequality_signs = get_data('example.txt')
    base_matrix = build_matrix(matrix_dim, coordinates_values_given_numbers)
    first_gen = create_first_gen(base_matrix, inequality_signs)
    new_generation_matrix_score = create_new_generation(first_gen, matrix_dim, inequality_signs)
    main_loops = 5
    loops = 300

    for j in range(main_loops):
        for i in range(loops):
            new_generation_matrix_score = create_new_generation(new_generation_matrix_score, matrix_dim,
                                                                inequality_signs)
        print('-----------after 300th generation----------------')
        pprint(new_generation_matrix_score[0])
        print('-------------------------------------------------')
        print('------------trying to solver problem of convergence---------------')
        new_generation_matrix_score = solve_problem(new_generation_matrix_score)
        print('------------after solver problem of convergence-------------------')
