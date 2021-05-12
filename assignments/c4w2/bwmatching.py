import sys
from collections import Counter

ALPHABET = ["A", "C", "G", "T"]


def get_bw_matching(bwt, patterns):
    # preprocess of bwt
    first_counter = Counter(bwt)
    last_tally = get_tally(bwt)

    match_counts = []

    for pattern in patterns:
        match_count = 0
        cur_char = pattern[-1]

        if cur_char in first_counter:
            min_rank = 0
            match_count = first_counter[cur_char]
            max_rank = min_rank + match_count - 1

            for i in range(len(pattern) - 2, -1, -1):
                start_row = get_row_num(cur_char, min_rank, first_counter)
                end_row = get_row_num(cur_char, max_rank, first_counter)

                cur_char = pattern[i]
                min_rank = last_tally[cur_char][start_row - 1]
                match_count = last_tally[cur_char][end_row] - min_rank
                max_rank = min_rank + match_count - 1

                # No matches for cur_char
                if not match_count:
                    break

        match_counts.append(match_count)

    return match_counts


def get_tally(bwt):
    tally = {char: [1 if bwt[0] == char else 0] for char in ALPHABET}

    for i in range(1, len(bwt)):
        for char in ALPHABET:
            if bwt[i] == char:
                tally[char].append(tally[char][-1] + 1)
            else:
                tally[char].append(tally[char][-1])

    return tally


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
    pattern_count = int(sys.stdin.readline().strip())
    patterns = sys.stdin.readline().strip().split()
    print(" ".join(map(str, get_bw_matching(bwt, patterns))))
