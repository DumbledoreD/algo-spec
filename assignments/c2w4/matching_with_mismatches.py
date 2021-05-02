import sys


class Solver:
    def __init__(self, k, t, p, x=31, p1=int(1e9 + 7), p2=int(1e9 + 9)):
        self.k, self.t, self.p = k, t, p

        self.x, self.p1, self.p2 = x, p1, p2

        self.t_prefix_hashes = self._get_prefix_hashes(self.t)
        self.p_prefix_hashes = self._get_prefix_hashes(self.p)

        # Precompute powers of x to save time. Time: TLE -> 23.52/40.00
        self.y1 = [None] * len(self.p)
        self.y2 = [None] * len(self.p)

        self.y1[0] = self.y2[0] = 1

        for i in range(1, len(self.p)):
            self.y1[i] = (self.x * self.y1[i - 1]) % self.p1
            self.y2[i] = (self.x * self.y2[i - 1]) % self.p2

    def matches(self):
        results = []
        for i in range(len(self.t) - len(self.p) + 1):
            if self._count_mismatches(i, i, i + len(self.p) - 1, 0) <= self.k:
                results.append(i)
        return results

    # TODO: Can do better?
    def _count_mismatches(self, start, left, right, count):
        m = (left + right) // 2

        count += int(self.t[m] != self.p[m - start])

        if left <= m - 1 and not self._are_substrings_equal(start, left, m - 1):
            # At least 1 mismatch in the left part
            # No need to find where exactly the mismatch is
            # Time: 23.52/40.00 -> 22.22/40.00
            if count == self.k:
                return float("inf")

            count = self._count_mismatches(start, left, m - 1, count)

        if m + 1 <= right and not self._are_substrings_equal(start, m + 1, right):
            # At least 1 mismatch in the right part
            # No need to find where exactly the mismatch is
            # Time: 23.52/40.00 -> 22.22/40.00
            if count == self.k:
                return float("inf")

            count = self._count_mismatches(start, m + 1, right, count)

        return count

    def _are_substrings_equal(self, start_of_t, t_left, t_right):
        p_left = t_left - start_of_t
        p_right = t_right - start_of_t

        t_seg_hashes = self._get_substring_hashes(t_left, t_right, self.t_prefix_hashes)
        p_seg_hashes = self._get_substring_hashes(p_left, p_right, self.p_prefix_hashes)

        return t_seg_hashes == p_seg_hashes

    def _get_substring_hashes(self, start, end, prefix_hashes):
        p1_hashes, p2_hashes = prefix_hashes

        if start == 0:
            return p1_hashes[end], p2_hashes[end]

        length = end - start + 1

        return (
            (p1_hashes[end] - self.y1[length] * p1_hashes[start - 1]) % self.p1,
            (p2_hashes[end] - self.y2[length] * p2_hashes[start - 1]) % self.p2,
        )

    def _get_prefix_hashes(self, s):
        p1_hashes = [None] * len(s)
        p2_hashes = [None] * len(s)

        p1_hashes[-1] = p2_hashes[-1] = 0
        for i, letter in enumerate(s):
            p1_hashes[i] = (self.x * p1_hashes[i - 1] + ord(letter)) % self.p1
            p2_hashes[i] = (self.x * p2_hashes[i - 1] + ord(letter)) % self.p2

        return p1_hashes, p2_hashes


if __name__ == "__main__":
    for line in sys.stdin.readlines():
        k, t, p = line.split()
        ans = Solver(int(k), t, p).matches()
        print(len(ans), *ans)
