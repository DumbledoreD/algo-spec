# python3


def calc_fib(n):
    if n <= 1:
        return n

    prev_two = [0, 1]

    for i in range(2, n):
        prev_two[i % 2] = sum(prev_two)

    return sum(prev_two)


if __name__ == "__main__":
    n = int(input())
    print(calc_fib(n))
