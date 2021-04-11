def get_fibonacci_last_digit(n):
    if n <= 1:
        return n

    if n <= 1:
        return n

    prev_two = [0, 1]

    for i in range(2, n):
        prev_two[i % 2] = sum(prev_two) % 10

    return sum(prev_two) % 10


if __name__ == "__main__":
    n = int(input())
    print(get_fibonacci_last_digit(n))
