import sys
from collections import Counter, defaultdict, namedtuple


class SequenceAssembler:
    MAX_MISMATCHES = 2
    MIN_CONSENSUS_VOTE = 5

    def __init__(self, reads):
        self._reads = self._preprocess_reads(reads)

        self._prefix_tree = PrefixTree(self._reads)

        self._build_consensus_counter()
        self._assemble_from_consensus_counter()

    def _preprocess_reads(self, reads):
        # Filter out duplicates, note reads are already sorted
        return [r for i, r in enumerate(reads) if r != reads[i - 1] and r]

    def _build_consensus_counter(self):
        self._seen = [False] * len(self._reads)
        self._consensus_counter = defaultdict(Counter)

        read = self._reads[0]
        self._seen[0] = True

        for i, c in enumerate(read):
            self._consensus_counter[i].update(c)

        while True:
            read_enum, concat_pos = self._find_max_overlap(read)

            if read_enum is None:
                break

            read = self._reads[read_enum]
            self._seen[read_enum] = True

            offset = len(self._consensus_counter) - concat_pos
            for i, c in enumerate(read):
                pos = i + offset
                self._consensus_counter[pos].update(c)

    def _find_max_overlap(self, read):
        for i in range(1, len(read)):
            for read_lb, read_ub, concat_pos in self._prefix_tree.find_match(
                read[i:], self.MAX_MISMATCHES
            ):
                for j in range(read_lb, read_ub + 1):
                    if not self._seen[j]:
                        return j, concat_pos
        return None, None

    def _assemble_from_consensus_counter(self):
        result = []

        for i in range(len(self._consensus_counter)):
            counter = self._consensus_counter[i]
            char, count = counter.most_common(1)[0]

            # Ignore start and end positions if min required votes not met
            if count < self.MIN_CONSENSUS_VOTE:
                if result:
                    break
                else:
                    continue

            result.append(char)

        result = "".join(result)

        self._result = self._remove_border(result)

    def _remove_border(self, text):
        prefix_function = compute_prefix_function(text)
        return text[prefix_function[-1] :]

    @property
    def result(self):
        return self._result


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

    def find_match(self, read, max_mismatches):
        OnStackNode = namedtuple("OnStackNode", ["node", "path_length", "mismatches"])

        node_stack = [OnStackNode(self.root, 0, 0)]

        while node_stack:
            cur_node, path_length, mismatches = node_stack.pop()
            local_pos = 0

            while path_length + local_pos < len(read):
                read_pos = path_length + local_pos
                cur_char = read[read_pos]

                # In node comparison
                if cur_node.chain_length and local_pos < cur_node.chain_length:
                    ref_char = self._reads[cur_node.lb][read_pos]

                    # Mismatch
                    if cur_char != ref_char:
                        mismatches += 1

                        if mismatches > max_mismatches:
                            break

                    local_pos += 1

                # Advance to the next node
                else:
                    path_length += cur_node.chain_length + 1

                    # Match
                    if cur_char in cur_node.children:
                        local_pos = 0
                        cur_node = cur_node.children[cur_char]

                    # Mismatch
                    else:
                        mismatches += 1

                        if mismatches <= max_mismatches:
                            for node in cur_node.children.values():
                                node_stack.append(
                                    OnStackNode(node, path_length, mismatches)
                                )

                        break

            # Yield when while condition is false, don't yield on break
            else:
                yield cur_node.lb, cur_node.ub, path_length + local_pos


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


# KMP / Knuth Morris Pratt Algorithm
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
    reads = sys.stdin.read().split("\n")
    print(SequenceAssembler(reads).result)
