import sys
from typing import Dict


class TrieNode:
    def __init__(self, key: int, val: str):
        self.key, self.val = key, val
        self.children: Dict[str, TrieNode] = {}


class Trie:
    def __init__(self):
        self._key_count = -1
        self.root = TrieNode(self._gen_key(), None)

    def _gen_key(self) -> int:
        self._key_count += 1
        return self._key_count

    def add_pattern(self, pattern: str):
        cur_node = self.root

        for letter in pattern:
            if letter in cur_node.children:
                cur_node = cur_node.children[letter]

            else:
                new_node = TrieNode(self._gen_key(), letter)
                cur_node.children[letter] = new_node
                cur_node = new_node


def bfs(root: TrieNode):
    cur_layer = [root]

    while cur_layer:
        next_layer = []

        for parent in cur_layer:
            for letter, child in parent.children.items():
                print(f"{parent.key}->{child.key}:{letter}")
                next_layer.append(child)

        cur_layer = next_layer


if __name__ == "__main__":
    patterns = sys.stdin.read().split()[1:]

    trie = Trie()

    for pattern in patterns:
        trie.add_pattern(pattern)

    bfs(trie.root)
