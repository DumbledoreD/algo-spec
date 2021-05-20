import sys


def naive_gaussian_elimination(augmented_matrix):
    # m equations, n variables
    m, n = len(augmented_matrix), len(augmented_matrix[0]) - 1
    cur_row = cur_col = 0

    while cur_row < m:
        for row in range(cur_row, m):
            if augmented_matrix[row][cur_col] != 0:
                # Swap row with cur_row
                augmented_matrix[cur_row], augmented_matrix[row] = (
                    augmented_matrix[row],
                    augmented_matrix[cur_row],
                )
                break

        # Scale cur_row
        factor = augmented_matrix[cur_row][cur_col]
        for col in range(cur_col, n + 1):
            augmented_matrix[cur_row][col] /= factor

        # Zero out coefficients for the current column in the other rows
        for row in range(m):
            if row == cur_row:
                continue

            factor = augmented_matrix[row][cur_col]
            for col in range(cur_col, n + 1):
                augmented_matrix[row][col] -= factor * augmented_matrix[cur_row][col]

        cur_col += 1
        cur_row += 1

    solution = []

    for i in range(n):
        solution.append(augmented_matrix[i][-1])

    return solution


if __name__ == "__main__":
    data = sys.stdin.read().split("\n")

    augmented_matrix = [list(map(int, row.split())) for row in data[1:] if row]
    solution = naive_gaussian_elimination(augmented_matrix)

    for x in solution:
        print("%.20lf" % x)
