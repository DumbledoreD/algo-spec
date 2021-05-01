from collections import deque


class Query:
    def __init__(self, query):
        self.type = query[0]
        if self.type == "check":
            self.ind = int(query[1])
        else:
            self.s = query[1]


class QueryProcessor:
    _multiplier = 263
    _prime = 1000000007

    def __init__(self, bucket_count):
        self.bucket_count = bucket_count
        self.lists = [deque() for _ in range(self.bucket_count)]

    def _hash_func(self, s):
        h = 0

        for i in range(len(s) - 1, -1, -1):
            h = (h * self._multiplier + ord(s[i])) % self._prime

        return h % self.bucket_count

    def _get_chain(self, s):
        return self.lists[self._hash_func(s)]

    def find(self, s):
        chain = self._get_chain(s)
        has_s = False

        for t in chain:
            if s == t:
                has_s = True
                break

        return has_s, chain

    def add(self, s):
        has_s, chain = self.find(s)

        if not has_s:
            chain.appendleft(s)

    def remove(self, s):
        chain = self._get_chain(s)

        try:
            chain.remove(s)
        except ValueError:
            pass

    def check(self, i):
        return self.lists[i]

    def process_query(self, query):
        if query.type == "check":
            # use reverse order, because we append strings to the end
            self.write_chain(self.check(query.ind))

        elif query.type == "find":
            has_s, _ = self.find(query.s)
            self.write_search_result(has_s)

        elif query.type == "add":
            self.add(query.s)

        elif query.type == "del":
            self.remove(query.s)

    def process_queries(self):
        n = int(input())
        for _ in range(n):
            self.process_query(self.read_query())

    def read_query(self):
        return Query(input().split())

    def write_search_result(self, was_found):
        print("yes" if was_found else "no")

    def write_chain(self, chain):
        print(" ".join(chain))


if __name__ == "__main__":
    bucket_count = int(input())
    proc = QueryProcessor(bucket_count)
    proc.process_queries()
