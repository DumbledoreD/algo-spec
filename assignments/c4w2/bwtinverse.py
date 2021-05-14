import sys
from collections import Counter, defaultdict, deque


def inverse_bwt(bwt):
    first_counter = Counter(bwt)
    last_b_rank = get_b_rank(bwt)

    cur_char, rank = "$", 0
    result = deque()

    while True:
        result.appendleft(cur_char)
        new_row_num = get_row_num(cur_char, rank, first_counter)
        cur_char = bwt[new_row_num]
        rank = last_b_rank[new_row_num]

        if cur_char == "$":
            break

    return "".join(result)


def get_b_rank(bwt):
    counter = defaultdict(int)
    b_rank = []

    for char in bwt:
        b_rank.append(counter[char])
        counter[char] += 1

    return b_rank


def get_row_num(char, rank, first_counter):
    if char == "$":
        return 0

    row_num = rank

    for item, count in first_counter.items():
        # Note, this will evaluate to True at least once for "$"
        # As ord("$") is smaller than ord(char) for char in alphabet
        if ord(item) < ord(char):
            row_num += count

    return row_num


if __name__ == "__main__":
    bwt = sys.stdin.readline().strip()
    print(inverse_bwt(bwt))
