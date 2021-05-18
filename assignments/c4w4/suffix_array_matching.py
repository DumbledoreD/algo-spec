import sys
from collections import Counter

ALPHABET = "$ACGT"
ALPHABET_TO_INDEX = {char: i for i, char in enumerate(ALPHABET)}


def find_matches(text, patterns):
    suffix_array = build_suffix_array(text)
    bwt = "".join([text[(index - 1) % len(text)] for index in suffix_array])
    return get_bw_matching_with_sa(bwt, patterns, suffix_array)


def build_suffix_array(text):
    order_to_start_index = sort_char(text)
    start_index_to_eq_class = compute_class(text, order_to_start_index)
    length = 1

    while length < len(text):
        order_to_start_index = sort_doubled(
            text, length, order_to_start_index, start_index_to_eq_class
        )
        start_index_to_eq_class = update_class(
            text, length, order_to_start_index, start_index_to_eq_class
        )
        length += length

    return order_to_start_index


def sort_char(text):
    count = [0] * len(ALPHABET)

    # Count chars
    for char in text:
        count[ALPHABET_TO_INDEX[char]] += 1

    # Make accumulative count
    for i in range(1, len(count)):
        count[i] += count[i - 1]

    order_to_start_index = [0] * len(text)

    # Iter through text backwards to keep stabe
    for i in range(len(text) - 1, -1, -1):
        char = text[i]
        count[ALPHABET_TO_INDEX[char]] -= 1
        order_to_start_index[count[ALPHABET_TO_INDEX[char]]] = i

    return order_to_start_index


def compute_class(text, order_to_start_index):
    start_index_to_eq_class = [0] * len(text)
    start_index_to_eq_class[order_to_start_index[0]] = 0

    # Iterate through order
    for order in range(1, len(order_to_start_index)):
        cur_start_index = order_to_start_index[order]
        prev_start_index = order_to_start_index[order - 1]

        if text[cur_start_index] == text[prev_start_index]:
            start_index_to_eq_class[cur_start_index] = start_index_to_eq_class[
                prev_start_index
            ]
        else:
            start_index_to_eq_class[cur_start_index] = (
                start_index_to_eq_class[prev_start_index] + 1
            )

    return start_index_to_eq_class


def sort_doubled(text, length, order_to_start_index, start_index_to_eq_class):
    eq_class_count = [0] * len(text)

    # Count equivalence classes
    for eq_class in start_index_to_eq_class:
        eq_class_count[eq_class] += 1

    # Make accumulative count
    for i in range(1, len(eq_class_count)):
        eq_class_count[i] += eq_class_count[i - 1]

    new_order_to_start_index = [0] * len(order_to_start_index)

    # Iter through order backwards to keep stabe
    for order in range(len(order_to_start_index) - 1, -1, -1):
        start_index = (order_to_start_index[order] - length) % len(text)
        eq_class = start_index_to_eq_class[start_index]
        eq_class_count[eq_class] -= 1
        new_order_to_start_index[eq_class_count[eq_class]] = start_index

    return new_order_to_start_index


def update_class(text, length, order_to_start_index, start_index_to_eq_class):
    new_start_index_to_eq_class = [0] * len(start_index_to_eq_class)

    cur_start_index = order_to_start_index[0]
    cur_mid_index = (cur_start_index + length) % len(text)
    cur_eq_class_tuple = (
        start_index_to_eq_class[cur_start_index],
        start_index_to_eq_class[cur_mid_index],
    )
    cur_eq_class = 0

    new_start_index_to_eq_class[cur_start_index] = cur_eq_class

    for order in range(1, len(order_to_start_index)):
        prev_eq_class_tuple, prev_eq_class = cur_eq_class_tuple, cur_eq_class

        cur_start_index = order_to_start_index[order]
        cur_mid_index = (cur_start_index + length) % len(text)
        cur_eq_class_tuple = (
            start_index_to_eq_class[cur_start_index],
            start_index_to_eq_class[cur_mid_index],
        )

        cur_eq_class = (
            prev_eq_class
            if cur_eq_class_tuple == prev_eq_class_tuple
            else prev_eq_class + 1
        )

        new_start_index_to_eq_class[cur_start_index] = cur_eq_class

    return new_start_index_to_eq_class


def find_matches_with_sa(text, pattern, suffix_array):
    min_rank, max_rank = 0, len(text)

    while min_rank < max_rank:
        mid_rank = (min_rank + max_rank) // 2

        # Slow
        if (
            pattern
            > text[suffix_array[mid_rank] : suffix_array[mid_rank] + len(pattern)]
        ):
            min_rank = mid_rank + 1
        else:
            max_rank = mid_rank

    start_rank = min_rank

    max_rank = len(text)

    while min_rank < max_rank:
        mid_rank = (min_rank + max_rank) // 2

        # Slow
        if (
            pattern
            < text[suffix_array[mid_rank] : suffix_array[mid_rank] + len(pattern)]
        ):
            max_rank = mid_rank
        else:
            min_rank = mid_rank + 1  # Note the + 1

    end_rank = max_rank

    results = []

    for rank in range(start_rank, end_rank):
        start_index = suffix_array[rank]
        suffix = text[start_index:]
        if suffix.startswith(pattern):
            results.append(start_index)

    return results


def get_bw_matching_with_sa(bwt, patterns, suffix_array):
    # preprocess of bwt
    first_counter = Counter(bwt)
    last_tally = get_tally(bwt)

    matches = set()

    for pattern in patterns:
        match_count = 0
        cur_char = pattern[-1]

        if cur_char not in first_counter:
            continue

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

        else:
            # Found matches
            start_row = get_row_num(cur_char, min_rank, first_counter)
            end_row = get_row_num(cur_char, max_rank, first_counter)

            for row in range(start_row, end_row + 1):
                matches.add(suffix_array[row])

    return matches


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
    text = sys.stdin.readline().strip() + "$"
    pattern_count = int(sys.stdin.readline().strip())
    patterns = sys.stdin.readline().strip().split()
    matches = find_matches(text, patterns)
    print(" ".join(map(str, matches)))
