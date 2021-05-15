import sys


def find_pattern(pattern, text):
    """
    Find all the occurrences of the pattern in the text
    and return a list of all positions in the text
    where the pattern starts in the text.
    """
    prefix_function = compute_prefix_function("".join([pattern, "$", text]))

    result = []
    offset = len(pattern) * 2

    for i in range(len(pattern) + 1, len(prefix_function)):
        border_length = prefix_function[i]
        if border_length == len(pattern):
            result.append(i - offset)

    return result


def compute_prefix_function(text):
    prefix_function = [0] * len(text)
    border_length = 0

    # Iter through prefixes
    for i in range(1, len(text)):
        # border_length is also the index of the char next to the current border
        while border_length > 0 and text[i] != text[border_length]:
            # Retract to the longest border of the current border
            border_length = prefix_function[border_length - 1]

        if text[i] == text[border_length]:
            border_length += 1

        else:
            border_length = 0

        prefix_function[i] = border_length

    return prefix_function


if __name__ == "__main__":
    pattern = sys.stdin.readline().strip()
    text = sys.stdin.readline().strip()
    result = find_pattern(pattern, text)
    print(" ".join(map(str, result)))
