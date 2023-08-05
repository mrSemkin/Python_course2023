# Вариант 11
# Коэффициенты системы линейных уравнений заданы в виде прямоугольной матрицы.
# С помощью допустимых преобразований привести систему к треугольному виду.
# Найти количество строк, среднее арифметическое элементов которых, меньше заданной величины.
import random

ARITHMETIC_MEDIUM = 5


def get_rnd_matrix(min_val, max_val, row, col):
    return [[random.randint(min_val, max_val) for _ in range(col)] for _ in range(row)]


def validate_matrix(matrix):
    col_max = len(matrix[0])

    # verification of data
    if len(matrix) > len(matrix[0]):
        return False

    for row in matrix:
        if col_max != len(row):
            return False
        for col in row:
            if not isinstance(col, (int, float)):
                return False
    return True


def print_matrix(matrix):
    for row in matrix:
        for col in row:
            print(str(col).rjust(8), end='')
        print('')


def get_triangular_matrix(matrix):
    number_of_rows = len(matrix)

    # make a triangular matrix
    col = 0
    for cur_row in range(number_of_rows - 1):
        if not swap_rows_with_zero(cur_row, col, matrix):
            for row in range(cur_row + 1, number_of_rows):
                k = matrix[row][col] / matrix[cur_row][col]
                matrix[row] = sum_row(k, matrix[cur_row], matrix[row])
        col += 1


def get_num_rows_more_than_medium(matrix, average_val):
    count = sum([1 for row in matrix if average_val > (sum(row) / len(matrix[0]))])

    print(f'\nThe number of rows whose arithmetic average is lower than {average_val} = {count}')


def swap_rows_with_zero(row_start, col, matrix):
    for cur_col in range(col, len(matrix)):  # find row value in column "col" not equal zero, if all zero find in next column
        for row in range(row_start, len(matrix)):
            # view the value in the "col" column
            # one found row where value not zero move up in position "row_start"
            if matrix[row][cur_col] != 0:
                matrix[row_start], matrix[row] = matrix[row], matrix[row_start]
                return False
        return True


def sum_row(k, row1, row2):
    return [round(item_2 - k * item_1, 2) for item_1, item_2 in zip(row1, row2)]


def main(matrix, medium):
    if not validate_matrix(matrix):
        print('Bad data')
        return False

    print('\nOrigin matrix')
    print_matrix(matrix)

    get_triangular_matrix(matrix)

    print('\nSimplified triangular matrix')
    print_matrix(matrix)

    get_num_rows_more_than_medium(matrix, medium)

    return True


if __name__ == '__main__':
    rectangle_matrix = get_rnd_matrix(-10, 10, 5, 6)

    main(rectangle_matrix, ARITHMETIC_MEDIUM)
