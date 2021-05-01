def get_occurrences(pattern, text):
    occurrences = []

    p, x = 10 ** 6 + 3, 31

    pattern_hash = poly_hash(pattern, p, x)
    hashes = get_rolling_hashes(text, len(pattern), p, x)

    for i, h in enumerate(hashes):
        if h == pattern_hash and text[i : i + len(pattern)] == pattern:
            occurrences.append(i)

    return occurrences


def get_rolling_hashes(text, seg_len, p, x):
    hashes = [None] * (len(text) - seg_len + 1)

    hashes[-1] = poly_hash(text[len(text) - seg_len :], p, x)

    y = (x ** seg_len) % p

    for i in range(len(hashes) - 2, -1, -1):
        hashes[i] = (x * hashes[i + 1] + ord(text[i]) - ord(text[i + seg_len]) * y) % p

    return hashes


def poly_hash(s, p, x):
    h = 0

    for i in range(len(s) - 1, -1, -1):
        h = (h * x + ord(s[i])) % p

    return h


def read_input():
    return (input().rstrip(), input().rstrip())


def print_occurrences(output):
    print(" ".join(map(str, output)))


if __name__ == "__main__":
    print_occurrences(get_occurrences(*read_input()))
