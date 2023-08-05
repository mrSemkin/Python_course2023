# Вариант 17
# Путем перестановки элементов квадратной вещественной матрицы добиться того,
# чтобы ее максимальный элемент находится в левом верхнем углу,
# следующий по величине — в позиции (2,2),
# следующий по величине — в позиции (3,3) и т. д.,
# заполнив таким образом всю главную диагональ.
# Найти номер первой из строк, не содержащих ни одного положительного элемента.

import random


def print_matrix(matrix):
    for row in matrix:
        for col in row:
            print(str(col).rjust(4), end='')
        print('')


def get_rnd_matrix(min_val, max_val, row, col):
    return [[random.randint(min_val, max_val) for _ in range(col)] for _ in range(row)]


def sort_diagonal(arr):
    diagonal = [item[n] for n, item in enumerate(arr)]
    diagonal.sort(reverse=True)
    for n, val in enumerate(diagonal):
        arr[n][n] = val

    return diagonal[-1]


def restruct_matrix(matrix, min_diagonal_val):
    matrix_size = len(matrix)
    for i in range(matrix_size):
        for j in range(matrix_size):
            if i == j:
                continue
            else:
                if matrix[i][j] > min_diagonal_val:
                    matrix[matrix_size - 1][matrix_size - 1], matrix[i][j] = matrix[i][j], matrix[matrix_size - 1][
                        matrix_size - 1]
                    min_diagonal_val = sort_diagonal(matrix)


def find_negative_row1(matrix):
    line_number = 1
    flag = False
    for row in matrix:
        if flag:
            break
        for item in row:
            if item >= 0:
                line_number += 1
                flag = False
                break
            else:
                flag = True

    return line_number if flag else -1


def find_negative_row(matrix):
    for i, row in enumerate(matrix):

        if all(value < 0 for value in row):
            return i
    return -1


def validate_matrix(matrix):
    for row in matrix:
        if len(row) != len(matrix):
            return False
    return True


def main():
    matrix = get_rnd_matrix(-99, 10, 5, 5)
    if not validate_matrix(matrix):
        print('Bad data')
        return

    print('origin matrix', len(matrix), 'x', len(matrix))
    print_matrix(matrix)

    min_diagonal_val = sort_diagonal(matrix)

    restruct_matrix(matrix, min_diagonal_val)

    print('Restructuring matrix')
    print_matrix(matrix)

    line = find_negative_row(matrix)

    print('Matrix does not have line with only negative values.') if line == -1 else print(f'First Line with only negative values is row {line}')

if __name__ == '__main__':
    main()
