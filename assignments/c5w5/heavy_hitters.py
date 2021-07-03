# Count Sketch / Heavy Hitter / Approx Point Query

# TODO: exceeded memory limit.

import math
import statistics
import sys


class ApproxPointQuery:
    # Not sure about what these values should be.
    _bucket_multiplier = 1000
    _estimate_count = 100

    _hash_multiplier = 42
    _hash_prime = 1000000007

    def __init__(self, stream_length):
        logn = math.ceil(math.log2(stream_length))
        self._bucket_count = logn * self._bucket_multiplier

        self._counter = [[0] * self._bucket_count for _ in range(self._estimate_count)]

    def _hash_fcn(self, r, v_id):
        h = (self._hash_multiplier * v_id + r) % self._hash_prime
        return h % self._bucket_count

    def _sign_fcn(self, r, v_id):
        h = (self._hash_multiplier * v_id + r) % self._hash_prime
        return 1 if h % 2 else -1

    def update(self, v_id, count):
        for r in range(self._estimate_count):
            c = self._hash_fcn(r, v_id)
            s = self._sign_fcn(r, v_id)
            self._counter[r][c] += count * s

    def get_estimate(self, v_id):
        return statistics.median(
            self._counter[r][self._hash_fcn(r, v_id)] * self._sign_fcn(r, v_id)
            for r in range(self._estimate_count)
        )


if __name__ == "__main__":
    data = sys.stdin.read().split("\n")
    data = [row for row in data if row]
    id_count, threshold, *stream, _, ids_of_interest = data

    id_count = int(id_count)
    threshold = int(threshold)

    assert len(stream) == id_count * 2

    pq = ApproxPointQuery(len(stream))

    # Update goods
    for i in range(id_count):
        v_id, count = map(int, stream[i].split())
        pq.update(v_id, count)

    # Update bads
    for i in range(id_count, 2 * id_count):
        v_id, count = map(int, stream[i].split())
        pq.update(v_id, -count)

    # Estimate
    ids_of_interest = map(int, ids_of_interest.split())
    result = [int(pq.get_estimate(v_id) >= threshold) for v_id in ids_of_interest]

    print(" ".join(map(str, result)))
