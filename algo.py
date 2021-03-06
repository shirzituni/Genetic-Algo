import random
from pprint import pprint
import numpy as np
from random import randint
import sys
import matplotlib.pyplot as plt
import sys

scores_per_generation = []
dictionary = {}

NUMBER_OF_DIGITS_ROW = 2
number_of_iter = 0
iter_num = 0
iter_score = 0


# get the data from the input file
def get_data(path):
    with open(path) as f:
        lines = f.readlines()
    matrix_size = int(lines[0])
    number_of_digits = int(lines[1])
    coordinates_values = []
    for i in range(NUMBER_OF_DIGITS_ROW, NUMBER_OF_DIGITS_ROW + number_of_digits):
        temp_set = []
        for j in lines[i]:
            if j != ' ' and j != '\n':
                temp_set.append(int(j))
        coordinates_values.append(temp_set)
    inequality_signs_input = []
    number_rows_before_coordinate = 3 + number_of_digits
    for i in range(number_rows_before_coordinate, len(lines)):
        temp_set = []
        for j in lines[i]:
            if j != ' ' and j != '\n':
                temp_set.append(int(j))
        inequality_signs_input.append(temp_set)

    return matrix_size, coordinates_values, inequality_signs_input


# build initial matrix
def build_matrix(matrix_size, coordinates_value):
    matrix = np.zeros(shape=(matrix_size, matrix_size), dtype='int')
    for number_set in coordinates_value:
        matrix[number_set[0] - 1, number_set[1] - 1] = number_set[2]
    return matrix


# generate one row
def generate_row(row, n):
    digits = [i for i in range(1, n + 1)]
    matrix_dim = row.size
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


# sort the list of tuples: matrices and score by theirs score
def sort_list(input_list):
    return sorted(input_list, key=lambda x: x[1])


# calculate number of mismatch between our solution and the desire solution
def calculate_mismatch(matrix_input, inequality_signs_input):
    return calculate_incorrect_inequality_signs(matrix_input, inequality_signs_input) + \
           calculate_duplicates_row_col(matrix_input)


# calculate the number of the mismatch between the matrix and the inequality signs that was in the input file
def calculate_incorrect_inequality_signs(matrix_input, inequality_signs_input):
    incorrect = 0
    for number_set in inequality_signs_input:
        if matrix_input[number_set[0] - 1, number_set[1] - 1] < matrix_input[number_set[2] - 1, number_set[3] - 1]:
            incorrect += 1
    return incorrect


# calculate the number of the duplicates number in each row and each column
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


'''
cross over between two matrices -
by taking one matrix to be the father and the other one to be the mother.
the rows in the new matrix are generate randomaly from each of them. 
'''


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


# solve the problem of convergence
def solve_convergence_problem(curr_generation, coordinates_values_given_numbers, inequality_signs):
    """
    # 30 pick best
    # 20 totally new like first gen
    # =
    # 50 send to hybridization
    """
    matrix_to_hybrid = []
    next_generation = []
    matrix_dim = curr_generation[0][0][0].size
    initial_matrix = build_matrix(matrix_dim, coordinates_values_given_numbers)
    best_30 = curr_generation[:30]
    new_20 = create_first_gen(initial_matrix, inequality_signs)[:20]
    matrix_to_hybrid.extend(best_30)
    matrix_to_hybrid.extend(new_20)
    next_generation.extend(best_30)
    next_generation.extend(new_20)
    next_generation.extend(cross_over(list_of_matrices=matrix_to_hybrid, matrix_size_input=matrix_dim,
                                      inequality_signs_input=inequality_signs))
    return sort_list(next_generation)


# create mutation in order to improve to the next generation
def create_mutation(matrices_to_mutate, matrix_size, coordinates_value):
    for matrix, score in matrices_to_mutate:
        for row_idx in range(matrix_size):
            for col_idx in range(matrix_size):
                random_num = randint(1, 10)
                # probability of a 2/10 to mutation
                if random_num < 2:
                    matrix[row_idx, col_idx] = randint(1, matrix_size)
                for number_set in coordinates_value:
                    matrix[number_set[0] - 1, number_set[1] - 1] = number_set[2]
    return matrices_to_mutate


# create the first generation
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


# create new generation
def create_new_generation(list_of_matrices_and_score, matrix_size, inequality_signs_input, test_type):
    new_gen_matrices = []
    global number_of_iter
    number_of_iter += 1
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

    """ 
        Total:
        10 from the generation before
        10 created by cross_over
        40 created by cross_over
        40 created by cross_over
        ---------------------
        100 new matrix for next generation
    """
    scores_sum = 0
    if test_type == 'lemarci_genetic':
        after_optimize = optimize_result(new_gen_matrices, inequality_signs_input, matrix_size)
        result_matrices_with_score = []
        for mutation_matrix, score in after_optimize:
            new_score = calculate_mismatch(mutation_matrix, inequality_signs_input)
            result_matrices_with_score.append((mutation_matrix, new_score))
        result_matrices_with_score = sort_list(result_matrices_with_score)

        # for the average score
        for each_tuple in result_matrices_with_score:
            scores_sum += each_tuple[1]

        # print("The average score in this generation", scores_sum / 100)
        return result_matrices_with_score
    else:
        result_matrices_with_score = []
        for mutation_matrix, score in new_gen_matrices:
            new_score = calculate_mismatch(mutation_matrix, inequality_signs_input)
            result_matrices_with_score.append((mutation_matrix, new_score))
        result_matrices_with_score = sort_list(result_matrices_with_score)

        for each_tuple in result_matrices_with_score:
            scores_sum += each_tuple[1]

        # print("The average score in this generation", scores_sum / 100)
    return result_matrices_with_score


# create optimization for the result by swapping the position with the adjacent one
def optimize_result(matrices, inequality_signs, matrix_dim):
    if type(matrices) == tuple:
        matrix_to_fix = matrices[0]
        for rule in inequality_signs:
            row1, col1, row2, col2 = rule
            if matrix_to_fix[row1 - 1][col1 - 1] < matrix_to_fix[row2 - 1][col2 - 1]:
                temp = matrix_to_fix[row1 - 1][col1 - 1]
                matrix_to_fix[row1 - 1][col1 - 1] = matrix_to_fix[row2 - 1][col2 - 1]
                matrix_to_fix[row2 - 1][col2 - 1] = temp
        score = calculate_mismatch(matrix_to_fix, inequality_signs)
        return matrices
    else:
        for curr_round in range(matrix_dim):
            for matrix_score in matrices:
                matrix_to_fix, score = matrix_score
                for rule in inequality_signs:
                    row1, col1, row2, col2 = rule
                    if matrix_to_fix[row1 - 1][col1 - 1] < matrix_to_fix[row2 - 1][col2 - 1]:
                        temp = matrix_to_fix[row1 - 1][col1 - 1]
                        matrix_to_fix[row1 - 1][col1 - 1] = matrix_to_fix[row2 - 1][col2 - 1]
                        matrix_to_fix[row2 - 1][col2 - 1] = temp
                score = calculate_mismatch(matrix_to_fix, inequality_signs)
        return matrices


# question 1.1
def regular_genetic():
    print('Starting regular genetic algorithm!')
    # read the input
    matrix_dim, coordinates_values_given_numbers, inequality_signs = get_data(sys.argv[1])
    # build base matrix and first generation
    base_matrix = build_matrix(matrix_dim, coordinates_values_given_numbers)
    first_gen = create_first_gen(base_matrix, inequality_signs)

    # create 2nd generation
    new_generation_matrix_score = create_new_generation(first_gen, matrix_dim, inequality_signs, 'regular_genetic')

    # run regular genetic algorithm with solving the convergence problem
    num_of_rounds = 200
    num_of_runs = 10
    for loop in range(num_of_rounds):
        for gen in range(num_of_runs):
            new_generation_matrix_score = create_new_generation(new_generation_matrix_score, matrix_dim,
                                                                inequality_signs, 'regular_genetic')
        dictionary[number_of_iter] = new_generation_matrix_score[0][1]
        print('-----------after ', (loop + 1) * num_of_runs, 'th generations----------------')
        # pprint will print the matrix in readable way
        pprint(new_generation_matrix_score[0])
        # if we find a solution, stop
        if new_generation_matrix_score[0][1] == 0:
            global iter_num
            iter_num = dictionary.keys()
            global iter_score
            iter_score = dictionary.values()
            return iter_num, iter_score
        print('-----------------------------------------------------------------')
        print('------------trying to solve problem of convergence---------------')
        new_generation_matrix_score = solve_convergence_problem(new_generation_matrix_score,
                                                                coordinates_values_given_numbers,
                                                                inequality_signs)
        print('------------after solve problem of convergence-------------------')

    iter_num = dictionary.keys()
    iter_score = dictionary.values()
    return iter_num, iter_score



# question 1.2.2
def darvini_genetic():
    print('Starting darvini algorithm!')
    darvini_genetic_dict = {}
    # read the input
    matrix_dim, coordinates_values_given_numbers, inequality_signs = get_data(sys.argv[1])
    # build base matrix and first generation
    base_matrix = build_matrix(matrix_dim, coordinates_values_given_numbers)
    first_gen = create_first_gen(base_matrix, inequality_signs)

    # create 2nd generation
    new_generation_matrix_score = create_new_generation(first_gen, matrix_dim, inequality_signs, 'darvini_genetic')
    # run darvini genetic algorithm
    num_of_rounds = 200
    num_of_runs = 10
    for loop in range(num_of_rounds):
        for gen in range(num_of_runs):
            new_generation_matrix_score = create_new_generation(new_generation_matrix_score, matrix_dim,
                                                                inequality_signs, 'darvini_genetic')
        dictionary[number_of_iter] = new_generation_matrix_score[0][1]
        print('-----------after, ', loop * num_of_runs, 'th generations---------')
        dictionary[number_of_iter] = new_generation_matrix_score[0][1]
        # ===========================================================
        # pprint will print the matrix in readable way
        pprint(new_generation_matrix_score[0])
        if new_generation_matrix_score[0][1] == 0:
            global iter_num
            iter_num = dictionary.keys()
            global iter_score
            iter_score = dictionary.values()
            return iter_num, iter_score
        print('-----------------------------------------------------------------')
        print('------------trying to solve problem of convergence---------------')
        new_generation_matrix_score = solve_convergence_problem(new_generation_matrix_score,
                                                                coordinates_values_given_numbers,
                                                                inequality_signs)
        print('------------after solve problem of convergence-------------------')
        pprint(new_generation_matrix_score[0])
    final_matrix = new_generation_matrix_score[0]
    matrix_after_optimize = optimize_result(final_matrix, inequality_signs, matrix_dim)
    pprint(matrix_after_optimize)

    iter_num = dictionary.keys()
    iter_score = dictionary.values()
    return iter_num, iter_score


# question 1.2.3
def lemarci_genetic():
    print('Starting lemarci algorithm!')
    # read the input
    matrix_dim, coordinates_values_given_numbers, inequality_signs = get_data(sys.argv[1])
    # build base matrix and first generation
    base_matrix = build_matrix(matrix_dim, coordinates_values_given_numbers)
    first_gen = create_first_gen(base_matrix, inequality_signs)

    # create 2nd generation
    new_generation_matrix_score = create_new_generation(first_gen, matrix_dim, inequality_signs, 'lemarci_genetic')

    # run lemarci genetic algorithm
    num_of_rounds = 200
    num_of_runs = 10
    for loop in range(num_of_rounds):
        for gen in range(num_of_runs):
            new_generation_matrix_score = create_new_generation(new_generation_matrix_score, matrix_dim,
                                                                inequality_signs, 'lemarci_genetic')
        dictionary[number_of_iter] = new_generation_matrix_score[0][1]
        print('-----------after, ', loop * num_of_runs, 'th generations----------------')
        # pprint will print the matrix in readable way
        pprint(new_generation_matrix_score[0])
        # if we find a solution, stop
        if new_generation_matrix_score[0][1] == 0:
            global iter_num
            iter_num = dictionary.keys()
            global iter_score
            iter_score = dictionary.values()
            return iter_num, iter_score
        print('------------------------------------------------------------------------')
        print('------------trying to solve problem of convergence----------------------')
        new_generation_matrix_score = solve_convergence_problem(new_generation_matrix_score,
                                                                coordinates_values_given_numbers,
                                                                inequality_signs)
        print('------------after solve problem of convergence--------------------------')
        pprint(new_generation_matrix_score[0])
    final_matrix = new_generation_matrix_score[0]
    matrix_after_optimize = optimize_result(final_matrix, inequality_signs, matrix_dim)
    pprint(matrix_after_optimize)

    iter_num = dictionary.keys()
    iter_score = dictionary.values()
    return iter_num, iter_score


def create_graphs():
    plt.plot(iter_num, iter_score)
    plt.xlabel('x - iter num')
    plt.ylabel('y - iter score')

    plt.title(sys.argv[2] + ' genetic algorithm!')
    plt.show()


if __name__ == "__main__":

    if sys.argv[2] == 'regular':
        iter_num, iter_score = regular_genetic()
    if sys.argv[2] == 'darvini':
        iter_num, iter_score = darvini_genetic()
    if sys.argv[2] == 'lemarci':
        iter_num, iter_score = lemarci_genetic()

    if sys.argv[2] == 'lemarci' or sys.argv[2] == 'darvini' or sys.argv[2] == 'regular':
        create_graphs()
    else:
        print("Invalid algorithm name input, try again")
