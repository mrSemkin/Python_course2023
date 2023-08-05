# Вариант 20
# Дана целочисленная прямоугольная матрица. Определить:
# 1) количество отрицательных элементов в тех строках, которые содержат хотя бы один нулевой элемент;
# 2) номера строк и столбцов всех седловых точек матрицы.
# Примечание. Матрица А имеет седловую точку Аij,
# если Аij является минимальным элементом в i-й строке и максимальным в j-м столбце.
import random


def get_rnd_matrix(min_val, max_val, row, col):
    return [[random.randint(min_val, max_val) for _ in range(col)] for _ in range(row)]


def saddle_point(row, col, matrix):
    val = matrix[row][col]
    min_row_val = min(matrix[row])
    max_col_val = max([r[col] for r in matrix])
    if val == min_row_val and val == max_col_val:
        return True
    return False


def find_row_with_zero(matrix):
    list_rows = [[i, row] for i, row in enumerate(matrix) if any(item == 0 for item in row)]
    # list_rows = []
    # for i, row in enumerate(matrix):
    #     if any(item == 0 for item in row):
    #         list_rows.append([i, row])
    # # print(list_rows)
    return list_rows


def calc_count_negative_items(list_rows):
    for row in list_rows:
        count = 0
        for item in row[1]:
            if item < 0:
                count += 1
        row[1] = count

    return list_rows


def print_matrix(matrix):
    for row in matrix:
        for col in row:
            print(str(col).rjust(4), end='')
        print('')


def validate_matrix(matrix):
    for row in matrix:
        if len(row) != len(matrix[0]):
            return False
    return True


def main():
    matrix = get_rnd_matrix(-5, 5, 7, 4)
    # matrix = [[1,1,3],[0,0,8],[0,0,8]]# test

    if not validate_matrix(matrix):
        print('Bad data')
        return

    print_matrix(matrix)
    print('')

    list_row = find_row_with_zero(matrix)

    print('Number of negative elements in rows that have at least one zero element:')
    print('[Row, Column]')
    print_matrix(calc_count_negative_items(list_row))

    print('Saddle point in matrix.')
    saddle_point_table = find_all_saddle_point(matrix)

    if len(saddle_point_table) > 0:
        print('[Row, Column, Value]')
        print_matrix(saddle_point_table)
    else:
        print('Matrix has no saddle points')


def find_all_saddle_point(matrix):
    point_list = []
    for n_row, row in enumerate(matrix):
        for n_col in range(len(row)):
            if saddle_point(n_row, n_col, matrix):
                point_list.append([n_row, n_col, matrix[n_row][n_col]])
    return point_list


if __name__ == '__main__':
    main()
