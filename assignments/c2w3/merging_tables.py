class Database:
    def __init__(self, row_counts):
        self.parents = list(range(len(row_counts)))
        self.rank = [0] * len(row_counts)
        self.row_counts = row_counts
        self.max_row_count = max(row_counts)

    def merge(self, src, dst):
        src_parent = self.get_parent(src)
        dst_parent = self.get_parent(dst)

        if src_parent == dst_parent:
            return

        new_row_count = self.row_counts[src_parent] + self.row_counts[dst_parent]
        self.max_row_count = max(self.max_row_count, new_row_count)

        src_rank, dst_rank = self.rank[src_parent], self.rank[dst_parent]

        if src_rank < dst_rank:
            self.parents[src_parent] = dst_parent
            self.row_counts[src_parent] = 0
            self.row_counts[dst_parent] = new_row_count
        else:
            self.parents[dst_parent] = src_parent
            self.row_counts[dst_parent] = 0
            self.row_counts[src_parent] = new_row_count

            if src_rank == dst_rank:
                self.rank[src_rank] += 1

    def get_parent(self, table):
        children_to_update = []

        root = table

        # Recursive implementation reaches max recursion depth for one of the testcase
        while root != self.parents[root]:
            children_to_update.append(root)
            root = self.parents[root]

        for i in children_to_update:
            self.parents[i] = root

        return root


def main():
    n_tables, n_queries = map(int, input().split())
    counts = list(map(int, input().split()))
    assert len(counts) == n_tables
    db = Database(counts)
    for _ in range(n_queries):
        dst, src = map(int, input().split())
        db.merge(dst - 1, src - 1)
        print(db.max_row_count)


if __name__ == "__main__":
    main()
