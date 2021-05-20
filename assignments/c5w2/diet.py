import sys
from itertools import combinations

INFINITY_BOUND = 1e9
ALMOST_ZERO = 1e-3


def naive_lin_prog(A, b, obj_coefficients):
    best_obj, best_solution = -float("inf"), None
    # m - num of inequilities, n - num of variables
    m, n = len(b), len(obj_coefficients)

    # Add x_i >= 0, and sum(x_i) <= INFINITY_BOUND as constraints
    A, b = add_constraints(A, b)

    # Pick n inequalities
    for indices in combinations(range(n + m + 1), n):
        # Solve the system of linear equations
        augmented_matrix = get_augmented_matrix(A, b, indices)
        solution = naive_gaussian_elimination(augmented_matrix)

        # Check the solution satisfies all other inequalities
        if solution and check_solution(solution, A, b):
            obj = calculate_objective(solution, obj_coefficients)
            if obj > best_obj:
                best_obj = obj
                best_solution = solution

    return float("inf") if best_obj == float("inf") else best_solution


def add_constraints(A, b):
    n = len(A[0])

    # Add x_i >= 0
    for i in range(n):
        constr = [0] * n
        constr[i] = -1
        A.append(constr)
        b.append(0)

    # Add sum(x_i) <= INFINITY_BOUND
    constr = [1] * n
    A.append(constr)
    b.append(INFINITY_BOUND)

    return A, b


def get_augmented_matrix(A, b, indices):
    return [A[i] + [b[i]] for i in indices]


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
        else:
            # No solution or multiple solutions
            return None

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


def check_solution(solution, A, b):
    for coefficients, rhs in zip(A, b):
        lhs = sum(c * x for c, x in zip(coefficients, solution))
        # Note the usage of ALMOST_ZERO
        if lhs - rhs > ALMOST_ZERO:
            return False

    return True


def calculate_objective(solution, obj_coefficients):
    obj = sum(c * x for c, x in zip(obj_coefficients, solution))
    return float("inf") if obj >= INFINITY_BOUND else obj


if __name__ == "__main__":
    data = sys.stdin.read().split("\n")
    data = [row for row in data if row]
    m, n = map(int, data[0].split())
    A = [list(map(int, row.split())) for row in data[1:-2]]
    b = list(map(int, data[-2].split()))
    obj = list(map(int, data[-1].split()))

    solution = naive_lin_prog(A, b, obj)

    if solution is None:
        print("No solution")
    elif solution == float("inf"):
        print("Infinity")
    else:
        print("Bounded solution")
        print(" ".join(["%.18f" % x for x in solution]))
