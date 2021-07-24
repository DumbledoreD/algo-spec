import sys


class MinMaxOverlap:
    def __init__(self, reads):
        self._reads = self._preprocess_reads(reads)
        self._prefix_tree = PrefixTree(self._reads)
        self._get_min_max_overlap()

    def _preprocess_reads(self, reads):
        # Filter out duplicates, note reads are already sorted
        return [r for i, r in enumerate(reads) if r != reads[i - 1] and r]

    def _get_min_max_overlap(self):
        self._min_max_overlap = float("inf")

        for read in self._reads:
            self._min_max_overlap = min(
                self._min_max_overlap,
                self._get_max_overlap(read),
            )

    def _get_max_overlap(self, read):
        for i in range(1, len(read)):
            read_suffix = read[i:]
            read_lb, read_ub, concat_pos = self._prefix_tree.find_match(read_suffix)

            if read_lb is not None:
                return len(read_suffix)

        return 0

    @property
    def result(self):
        return self._min_max_overlap + 1


class PrefixTree:
    def __init__(self, reads):
        self._reads = reads
        self._build_prefix_tree()

    def _build_prefix_tree(self):
        self.root = Node(None, 0, 0, 0)

        for read_enum, read in enumerate(self._reads):
            self._add_read_to_tree(read_enum, read)

    def _add_read_to_tree(self, read_enum, read):
        cur_node = self.root
        path_length = 0
        local_pos = 0

        while path_length + local_pos < len(read):
            read_pos = path_length + local_pos
            cur_char = read[read_pos]

            # In node comparison
            if cur_node.chain_length and local_pos < cur_node.chain_length:
                ref_char = self._reads[cur_node.lb][read_pos]

                # Match
                if cur_char == ref_char:
                    local_pos += 1

                # Branch
                else:
                    # Split cur node
                    split_cur_node = Node(
                        ref_char,
                        cur_node.lb,
                        cur_node.ub,
                        cur_node.chain_length - local_pos - 1,
                    )
                    split_cur_node.children = cur_node.children

                    # Add new node
                    new_node = Node(
                        cur_char, read_enum, read_enum, len(read) - read_pos - 1
                    )

                    # Update cur node
                    cur_node.chain_length = local_pos
                    cur_node.ub = read_enum
                    cur_node.children = {ref_char: split_cur_node, cur_char: new_node}

                    return

            # Advance to the next node
            else:
                cur_node.ub = read_enum

                # Match
                if cur_char in cur_node.children:
                    local_pos = 0
                    path_length += cur_node.chain_length + 1
                    cur_node = cur_node.children[cur_char]

                # Branch
                else:
                    new_node = Node(
                        cur_char, read_enum, read_enum, len(read) - read_pos - 1
                    )
                    cur_node.children[cur_char] = new_node

                    return

    def find_match(self, read):
        cur_node = self.root
        path_length = 0
        local_pos = 0

        # TODO: Similar to _add_read_to_tree, DRY.
        while path_length + local_pos < len(read):
            read_pos = path_length + local_pos
            cur_char = read[read_pos]

            # In node comparison
            if cur_node.chain_length and local_pos < cur_node.chain_length:
                ref_char = self._reads[cur_node.lb][read_pos]

                # Match
                if cur_char == ref_char:
                    local_pos += 1

                # Mismatch
                else:
                    return None, None, None

            # Advance to the next node
            else:
                # Match
                if cur_char in cur_node.children:
                    local_pos = 0
                    path_length += cur_node.chain_length + 1
                    cur_node = cur_node.children[cur_char]

                # Mismatch
                else:
                    return None, None, None

        return cur_node.lb, cur_node.ub, path_length + local_pos


class Node:
    def __init__(self, char, lb, ub, chain_length):
        self.char = char
        self.children = {}

        # The range [lb, ..., ub]represents all the strings which have a common prefix
        # represented by a path from the root to this node
        self.lb = lb
        self.ub = ub

        # the length of a substring in the node
        self.chain_length = chain_length

    def __repr__(self):
        return "Node(char={}, children={}, lb={}, ub={}, chain_length={})".format(
            self.char, self.children.keys(), self.lb, self.ub, self.chain_length
        )


def main():
    reads = sys.stdin.read().split("\n")
    print(MinMaxOverlap(reads).result)


if __name__ == "__main__":
    main()
