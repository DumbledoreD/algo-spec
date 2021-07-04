class SequenceAssembler:
    ALPHABET = "ACGT"

    def __init__(self, reads):
        self._reads = reads

        self._build_prefix_tree()

    def _build_prefix_tree(self):
        self._root = Node(None, 0, 0, 0)

        for read_enum, read in enumerate(self._reads):
            self._add_read_to_tree(read_enum, read)

    def _add_read_to_tree(self, read_enum, read):
        cur_node = self._root
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

            # Advancing to the next node
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


if __name__ == "__main__":
    reads = [
        "AAGGG",
        "ACTTT",
        "AGGCT",
        "GCCAC",
        "TCCGC",
    ]
    a = SequenceAssembler(reads)

    print(a)
