import sys

ALPHABET = "$ACGT"
ALPHABET_TO_INDEX = {char: i for i, char in enumerate(ALPHABET)}


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


if __name__ == "__main__":
    text = sys.stdin.readline().strip()
    print(" ".join(map(str, build_suffix_array(text))))
