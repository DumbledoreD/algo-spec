def max_pairwise_product(numbers):
    a = b = 0

    for number in numbers:
        if number >= a:
            b, a = a, number
        elif number > b:
            b = number

    return a * b


if __name__ == "__main__":
    input_n = int(input())
    input_numbers = [int(x) for x in input().split()]
    print(max_pairwise_product(input_numbers))
