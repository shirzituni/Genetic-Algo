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
    # # Sort the list
    # Len = len(input_list)
    # for i in range(0, Len):
    #     for j in range(0, (Len - i - 1)):
    #         if input_list[j][1] > input_list[j + 1][1]:
    #             temp = input_list[j]
    #             input_list[j] = input_list[j + 1]
    #             input_list[j + 1] = temp
    # return input_list
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
    for dup in duplicates_in_rows:
        total_duplicates += dup

    for dup in duplicates_in_cols:
        total_duplicates += dup

    return total_duplicates


def hybridization(list_of_matrices, matrix_size_input, inequality_signs_input):
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


def disrupt_generation(matrices_to_mutate, matrix_size, coordinates_value):
    knows_indexes = []
    for couple in coordinates_value:
        knows_indexes.append(couple[1])
    for curr_matrix, _ in matrices_to_mutate:
        curr_matrix = curr_matrix.T
        for row in range(matrix_size):
            if row + 1 not in knows_indexes:
                random_num = randint(0, 10)
                # probability of a half to mutation
                if random_num <= 3:
                    pass
                else:
                    curr_matrix[row] = generate_row([0] * matrix_size, matrix_size)
        curr_matrix = curr_matrix.T
    return matrices_to_mutate


# def create_mutation(matrices_to_mutate, matrix_size, coordinates_value):
#     knows_indexes = []
#     for couple in coordinates_value:
#         knows_indexes.append(couple[1])
#     for curr_matrix, _ in matrices_to_mutate:
#         curr_matrix = curr_matrix.T
#         for row in range(matrix_size):
#             if row + 1 not in knows_indexes:
#                 random_num = randint(0, 10)
#                 # probability of a half to mutation
#                 if random_num <= 3:
#                     pass
#                 else:
#                     curr_matrix[row] = generate_row([0] * matrix_size, matrix_size)
#         curr_matrix = curr_matrix.T
#     return matrices_to_mutate


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


def create_new_generation(list_of_matrices_and_score, matrix_size, inequality_signs_input, coordinates_value):
    new_gen_matrices = []

    # append the top-10 from the previous generation to the next
    top_ten_score_matrices = list_of_matrices_and_score[:10]
    new_gen_matrices.extend(top_ten_score_matrices)

    forty_top_score_matrices = list_of_matrices_and_score[:40]

    hybrid_top_ten_matrices = hybridization(top_ten_score_matrices, matrix_size, inequality_signs_input)
    hybrid_top_forty_matrices = hybridization(forty_top_score_matrices, matrix_size, inequality_signs_input)
    hybrid_top_forty_matrices_2 = hybridization(forty_top_score_matrices, matrix_size, inequality_signs_input)

    # create mutation
    new_gen_matrices.extend(create_mutation(hybrid_top_ten_matrices, matrix_size, coordinates_value))
    new_gen_matrices.extend(create_mutation(hybrid_top_forty_matrices, matrix_size, coordinates_value))
    new_gen_matrices.extend(create_mutation(hybrid_top_forty_matrices_2, matrix_size, coordinates_value))

    # total:
    # 10 from the generation before
    # 90 created by hybridization
    # ---------------------
    # 100 new matrix for next generation

    result_matrices_with_score = []
    for mutation_matrix, score in new_gen_matrices:
        new_score = calculate_mismatch(mutation_matrix, inequality_signs_input)
        result_matrices_with_score.append((mutation_matrix, new_score))
    result_matrices_with_score = sort_list(result_matrices_with_score)
    return result_matrices_with_score


def problem_of_convergence(curr_generation):
    for i in range(100):
        curr_generation = create_mutation(matrices_to_mutate=curr_generation, matrix_size=matrix_dim,
                                          coordinates_value=coordinates_values_given_numbers)
    return curr_generation


if __name__ == "__main__":
    matrix_dim, coordinates_values_given_numbers, inequality_signs = get_data('example.txt')
    base_matrix = build_matrix(matrix_dim, coordinates_values_given_numbers)
    first_gen = create_first_gen(base_matrix, inequality_signs)
    new_generation_matrix_score = create_new_generation(first_gen, matrix_dim, inequality_signs,
                                                        coordinates_values_given_numbers)

    for i in range(200):
        new_generation_matrix_score = create_new_generation(new_generation_matrix_score, matrix_dim, inequality_signs,
                                                            coordinates_values_given_numbers)
    print('-----------after 200th generation----------------')
    pprint(new_generation_matrix_score[0])
    print('----------------------------------')
    new_generation_matrix_score = disrupt_generation(matrices_to_mutate=new_generation_matrix_score,
                                                     matrix_size=matrix_dim,
                                                     coordinates_value=coordinates_values_given_numbers)
    print('-----------solve convergence---------------')

    for i in range(200):
        new_generation_matrix_score = create_new_generation(new_generation_matrix_score, matrix_dim, inequality_signs,
                                                            coordinates_values_given_numbers)
    print('-----------after 400th generation----------------')
    pprint(new_generation_matrix_score[0])
    print('----------------------------------')
    new_generation_matrix_score = disrupt_generation(matrices_to_mutate=new_generation_matrix_score,
                                                     matrix_size=matrix_dim,
                                                     coordinates_value=coordinates_values_given_numbers)
    print('-----------solve convergence---------------')

    for i in range(200):
        new_generation_matrix_score = create_new_generation(new_generation_matrix_score, matrix_dim, inequality_signs,
                                                            coordinates_values_given_numbers)
    print('-----------after 600th generation----------------')
    pprint(new_generation_matrix_score[0])
    print('----------------------------------')
    new_generation_matrix_score = disrupt_generation(matrices_to_mutate=new_generation_matrix_score,
                                                     matrix_size=matrix_dim,
                                                     coordinates_value=coordinates_values_given_numbers)
    print('-----------solve convergence---------------')

    for i in range(200):
        new_generation_matrix_score = create_new_generation(new_generation_matrix_score, matrix_dim, inequality_signs,
                                                            coordinates_values_given_numbers)
    print('-----------after 800th generation----------------')
    pprint(new_generation_matrix_score[0])
    print('----------------------------------')
    new_generation_matrix_score = disrupt_generation(matrices_to_mutate=new_generation_matrix_score,
                                                     matrix_size=matrix_dim,
                                                     coordinates_value=coordinates_values_given_numbers)
