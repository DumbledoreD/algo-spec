import sys
from collections import namedtuple

Answer = namedtuple("answer_type", "i j len")


# Max time used: 9.41/15.00, max memory used: 49_246_208/536_870_912
class Solver:
    def __init__(self, s, t, x=31, p1=int(1e9 + 7), p2=int(1e9 + 9)):  # 1e9 is float
        self.s, self.t, self.x, self.p1, self.p2 = s, t, x, p1, p2
        self.s_prefix_hashes = self._get_prefix_hashes(self.s, self.x, self.p1, self.p2)
        self.t_prefix_hashes = self._get_prefix_hashes(self.t, self.x, self.p1, self.p2)

    def longest_common_substring(self):
        left, right = 0, min(len(self.s), len(self.t))

        prev_i_j_length = (0, 0, 0)

        while left <= right:
            m = (left + right) // 2

            i, j, length = self._has_common_substring(m)

            if length:
                prev_i_j_length = i, j, length
                left = m + 1
            else:
                right = m - 1

        return prev_i_j_length

    def _get_prefix_hashes(self, s, x, p1, p2):
        p1_hashes = [None] * len(s)
        p2_hashes = [None] * len(s)

        p1_hashes[-1] = p2_hashes[-1] = 0
        for i, letter in enumerate(s):
            p1_hashes[i] = (x * p1_hashes[i - 1] + ord(letter)) % p1
            p2_hashes[i] = (x * p2_hashes[i - 1] + ord(letter)) % p2

        return p1_hashes, p2_hashes

    def _has_common_substring(self, length):
        hash_to_i = {}

        for i in range(len(self.s) - length + 1):
            hashes = self._get_substring_hashes(i, length, self.s_prefix_hashes)
            hash_to_i[hashes] = i

        for j in range(len(self.t) - length + 1):
            hashes = self._get_substring_hashes(j, length, self.t_prefix_hashes)
            i = hash_to_i.get(hashes)
            if i is not None:
                return i, j, length

        return 0, 0, 0

    def _get_substring_hashes(self, start, length, prefix_hashes):
        end = start + length - 1

        p1_hashes, p2_hashes = prefix_hashes

        if start == 0:
            return p1_hashes[end], p2_hashes[end]

        # Faster than using y = self.x ** length
        y1 = pow(self.x, length, self.p1)
        y2 = pow(self.x, length, self.p2)

        return (
            (p1_hashes[end] - y1 * p1_hashes[start - 1]) % self.p1,
            (p2_hashes[end] - y2 * p2_hashes[start - 1]) % self.p2,
        )


# Max time used: 3.18/15.00, max memory used: 41_218_048/536_870_912
class SolverV2:
    def __init__(self, s, t, x=31, p1=int(1e9 + 7), p2=int(1e9 + 9)):  # 1e9 is float
        self.s, self.t, self.x, self.p1, self.p2 = s, t, x, p1, p2

    def longest_common_substring(self):
        left, right = 0, min(len(self.s), len(self.t))

        prev_i_j_length = (0, 0, 0)

        while left <= right:
            m = (left + right) // 2

            i, j, length = self._has_common_substring(m)

            if length:
                prev_i_j_length = i, j, length
                left = m + 1
            else:
                right = m - 1

        return prev_i_j_length

    def _has_common_substring(self, length):
        p1_rolling_hashes = get_rolling_hashes(self.s, length, self.p1, self.x)
        p2_rolling_hashes = get_rolling_hashes(self.s, length, self.p2, self.x)

        hash_to_i = {
            hashes: i
            for i, hashes in enumerate(zip(p1_rolling_hashes, p2_rolling_hashes))
        }

        p1_hashes = [None] * (len(self.t) - length + 1)
        p2_hashes = [None] * (len(self.t) - length + 1)

        p1_hashes[-1] = poly_hash(self.t[len(self.t) - length :], self.p1, self.x)
        p2_hashes[-1] = poly_hash(self.t[len(self.t) - length :], self.p2, self.x)

        i = hash_to_i.get((p1_hashes[-1], p2_hashes[-1]))
        if i is not None:
            return i, len(self.t) - length, length

        y1 = pow(self.x, length, self.p1)
        y2 = pow(self.x, length, self.p2)

        for j in range(len(p1_hashes) - 2, -1, -1):
            p1_hashes[j] = (
                self.x * p1_hashes[j + 1]
                + ord(self.t[j])
                - ord(self.t[j + length]) * y1
            ) % self.p1
            p2_hashes[j] = (
                self.x * p2_hashes[j + 1]
                + ord(self.t[j])
                - ord(self.t[j + length]) * y2
            ) % self.p2

            i = hash_to_i.get((p1_hashes[j], p2_hashes[j]))
            if i is not None:
                return i, j, length

        return 0, 0, 0


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


if __name__ == "__main__":
    for line in sys.stdin.readlines():
        s, t = line.split()
        ans = Answer(*SolverV2(s, t).longest_common_substring())
        print(ans.i, ans.j, ans.len)
