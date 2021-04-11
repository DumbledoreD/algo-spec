def fibonacci_sum_squares(n):
    pisano_period = get_pisano_period(10)

    length = pisano_period[(n + 1) % len(pisano_period)]
    width = pisano_period[n % len(pisano_period)]

    # Key S(n) = F(n + 1) * F(n)
    return (length * width) % 10


def get_pisano_period(m):
    # Key: the period always starts with 0, 1

    n, count = 0, 0
    period = []

    while count <= 1:
        period.append(calc_fib(n) % m)
        n += 1

        if period[-2:] == [0, 1]:
            count += 1

    return period[:-2]


def calc_fib(n):
    if n <= 1:
        return n

    prev_two = [0, 1]

    for i in range(2, n):
        prev_two[i % 2] = sum(prev_two)

    return sum(prev_two)


if __name__ == "__main__":
    n = int(input())
    print(fibonacci_sum_squares(n))
