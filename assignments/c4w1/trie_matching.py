import sys
from typing import Dict, List


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

    def bfs(self):
        cur_layer = [self.root]

        while cur_layer:
            next_layer = []

            for parent in cur_layer:
                for letter, child in parent.children.items():
                    print(f"{parent.key}->{child.key}:{letter}")
                    next_layer.append(child)

            cur_layer = next_layer

    def get_match_indices(self, text: str) -> List[int]:
        result = []

        for i in range(len(text)):
            if self.has_match(i, text):
                result.append(i)

        return result

    def has_match(self, starting_index: int, text: str) -> bool:
        cur_node = self.root

        for i in range(starting_index, len(text)):
            cur_letter = text[i]

            if cur_letter not in cur_node.children:
                return False

            cur_node = cur_node.children[cur_letter]

            if not cur_node.children:  # Reached a leaf
                return True

        # Reached end of text
        return False


if __name__ == "__main__":
    text = sys.stdin.readline().strip()
    n = int(sys.stdin.readline().strip())

    trie = Trie()

    for i in range(n):
        pattern = sys.stdin.readline().strip()
        trie.add_pattern(pattern)

    ans = trie.get_match_indices(text)

    sys.stdout.write(" ".join(map(str, ans)) + "\n")
