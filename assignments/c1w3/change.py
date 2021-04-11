# python3


def get_change(m):
    coins = [10, 5, 1]
    num_coins = 0
    mod = m

    for c in coins:
        div, mod = divmod(mod, c)
        num_coins += div

    return num_coins


if __name__ == "__main__":
    m = int(input())
    print(get_change(m))
