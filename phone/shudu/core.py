import time


def time_cal(fun):
    def function(*args, **kwargs):
        past = time.time()
        result = fun(*args, **kwargs)
        now = time.time()
        print("计算用时{}秒".format(now-past))
        return result
    return function


def print_grid(arr):
    for i in range(9):
        for j in range(9):
            # 注意，在py3.x中，print函数默认都有换行
            print(arr[i][j], end=" ")
        print()


# 找出目前没有被赋值的位置，若全部都被填满，则返回False
def find_empty_location(arr, l):
    for row in range(9):
        for col in range(9):
            if arr[row][col] == 0:
                l[0] = row
                l[1] = col
                # print("empty: row="+str(row)+" col="+str(col))
                return True
    return False


# 找出num在该arr的row行是否出现过
def used_in_row(arr, row, num):
    for i in range(9):
        if arr[row][i] == num:
            return True
    return False


# 找出num在该arr的col列是否出现过
def used_in_col(arr, col, num):
    for i in range(9):
        if arr[i][col] == num:
            return True
    return False


# 找出num在该arr的3x3-box是否出现过，更应注意的是，传参技巧！
def used_in_box(arr, row, col, num):
    for i in range(3):
        for j in range(3):
            if arr[row+i][col+j] == num:
                return True
    return False


def check_location_is_safe(arr, row, col, num):
    return not used_in_row(arr, row, num) and not used_in_col(arr, col, num) and not used_in_box(arr, row - row % 3, col - col % 3, num)


def solve_sudoku(arr):
    # 当前搜索的第几行、第几列
    l = [0, 0]
    # 找出还未被填充的位置
    if not find_empty_location(arr, l):
        return True
    # 未被填充的位置，赋值给row，col
    row = l[0]
    col = l[1]

    for num in range(1, 10):
        if check_location_is_safe(arr, row, col, num):
            arr[row][col] = num
            #print_grid(arr)
            if solve_sudoku(arr):
                return True
            # 若当前num导致未来并没有结果，则当前所填充的数无效，置0后选下一个数测试
            arr[row][col] = 0

    return False


@time_cal
def main(grid):
    if solve_sudoku(grid):
        print_grid(grid)
        # print(grid)
        return grid
    else:
        print("No solution exists\n")


if __name__ == "__main__":
    grid_1 = [[3, 0, 6, 5, 0, 8, 4, 0, 0],
            [5, 2, 0, 0, 0, 0, 0, 0, 0],
            [0, 8, 7, 0, 0, 0, 0, 3, 1],
            [0, 0, 3, 0, 1, 0, 0, 8, 0],
            [9, 0, 0, 8, 6, 3, 0, 0, 5],
            [0, 5, 0, 0, 9, 0, 6, 0, 0],
            [1, 3, 0, 0, 0, 0, 2, 5, 0],
            [0, 0, 0, 0, 0, 0, 0, 7, 4],
            [0, 0, 5, 2, 0, 6, 3, 0, 0]]
    main(grid_1)
