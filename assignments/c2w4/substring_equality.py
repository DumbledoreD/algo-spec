import sys


class Solver:
    def __init__(self, s, x=31, p1=10 ** 9 + 7, p2=10 ** 9 + 9):
        self.s, self.x, self.p1, self.p2 = s, x, p1, p2
        self.prefix_hashes = self._get_prefix_hashes(self.s, self.x, self.p1, self.p2)

    def ask(self, a, b, l):
        hashes_a_l = self._get_substring_hashes(a, l)
        hashes_b_l = self._get_substring_hashes(b, l)

        return hashes_a_l == hashes_b_l

    def _get_prefix_hashes(self, s, x, p1, p2):
        p1_hashes = [None] * len(s)
        p2_hashes = [None] * len(s)

        p1_hashes[-1] = p2_hashes[-1] = 0
        for i, letter in enumerate(s):
            p1_hashes[i] = (x * p1_hashes[i - 1] + ord(letter)) % p1
            p2_hashes[i] = (x * p2_hashes[i - 1] + ord(letter)) % p2

        return p1_hashes, p2_hashes

    def _get_substring_hashes(self, start, length):
        end = start + length - 1

        p1_hashes, p2_hashes = self.prefix_hashes

        if start == 0:
            return p1_hashes[end], p2_hashes[end]

        y = self.x ** length

        return (
            (p1_hashes[end] - y * p1_hashes[start - 1]) % self.p1,
            (p2_hashes[end] - y * p2_hashes[start - 1]) % self.p2,
        )


if __name__ == "__main__":
    s = sys.stdin.readline()
    q = int(sys.stdin.readline())
    solver = Solver(s)
    for i in range(q):
        a, b, l = map(int, sys.stdin.readline().split())
        print("Yes" if solver.ask(a, b, l) else "No")
