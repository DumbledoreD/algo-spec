import sys


def max_dot_product(a, b):
    return sum(a_i * b_i for a_i, b_i in zip(sorted(a), sorted(b)))


if __name__ == "__main__":
    data = list(map(int, sys.stdin.read().split()))
    n = data[0]
    a = data[1 : (n + 1)]
    b = data[(n + 1) :]
    print(max_dot_product(a, b))
