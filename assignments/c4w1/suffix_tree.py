# Ref: https://www.youtube.com/watch?v=VA9m_l6LpwI

import sys
from typing import List


class SuffixTreeNode:
    def __init__(self, start_index: int, length: int):
        self.start_index, self.length = start_index, length
        self.children: List[SuffixTreeNode] = []


class SuffixTree:
    def __init__(self, text: str):
        self.text = text
        self.root = SuffixTreeNode(0, 0)
        self.build_suffix_tree()

    def build_suffix_tree(self):
        for i in range(len(self.text) - 1, -1, -1):
            self.add_suffix(i, self.root)

    def add_suffix(self, start_index: int, start_node: SuffixTreeNode):
        suffix_length = len(self.text) - start_index

        cur_node = None

        for node in start_node.children:
            if self.text[node.start_index] == self.text[start_index]:
                cur_node = node
                break

        if cur_node:
            for i in range(1, min(suffix_length, cur_node.length)):
                # Note the last letter for the incoming suffix is "$"
                if self.text[start_index + i] != self.text[cur_node.start_index + i]:
                    # Branch, edit cur_node
                    branched_cur_node = SuffixTreeNode(
                        cur_node.start_index + i, cur_node.length - i
                    )
                    branched_cur_node.children = cur_node.children

                    cur_node.length = i
                    cur_node.children = [branched_cur_node]

                    # Branch, add remaining new suffix as new node
                    self.add_suffix(start_index + i, cur_node)

                    break

            # All letter match in the range
            else:
                # If cur_node length is shorter and cur_node is not a leaf
                if (
                    cur_node.length < suffix_length
                    and self.text[cur_node.start_index + cur_node.length - 1] != "$"
                ):
                    self.add_suffix(start_index + cur_node.length, cur_node)

        # No existing node start with current suffix. Add whole suffix as a new node
        else:
            new_node = SuffixTreeNode(start_index, suffix_length)
            start_node.children.append(new_node)


def dfs(suffix_tree: SuffixTree) -> List[str]:
    edges = []

    stack = [node for node in suffix_tree.root.children]

    while stack:
        cur_node = stack.pop()
        edge = suffix_tree.text[
            cur_node.start_index : cur_node.start_index + cur_node.length
        ]
        edges.append(edge)

        stack.extend(cur_node.children)

    return edges


def bfs(suffix_tree: SuffixTree) -> List[str]:
    edges = []

    cur_layer = [node for node in suffix_tree.root.children]

    while cur_layer:
        next_layer = []

        for node in cur_layer:
            edge = suffix_tree.text[node.start_index : node.start_index + node.length]
            edges.append(edge)

            next_layer.extend(node.children)

        cur_layer = next_layer

    return edges


if __name__ == "__main__":
    text = sys.stdin.readline().strip()
    suffix_tree = SuffixTree(text)
    print("\n".join(bfs(suffix_tree)))
