# Independent set problem

import sys
import threading

# This code is used to avoid stack overflow issues
sys.setrecursionlimit(10 ** 6)  # max depth of recursion
threading.stack_size(2 ** 26)  # new thread will get stack of such size


class Vertex:
    def __init__(self, weight):
        self.weight = weight
        self.children = set()


def build_tree(data):
    tree = [Vertex(w) for w in map(int, data[1].split())]
    for edge in data[2:]:
        if edge.strip():
            a, b = list(map(int, edge.split()))
            tree[a - 1].children.add(b - 1)
            tree[b - 1].children.add(a - 1)
    return tree


class MaxWeightIndependentSetSolver:
    def __init__(self, tree):
        self.tree = tree
        self.on_stack = set()
        self.subtree_max_weight = [None] * len(tree)

    @property
    def result(self):
        if self.tree:
            self.dfs(0)
            return self.dfs(0)
        return 0

    def dfs(self, u):
        if self.subtree_max_weight[u] is not None:
            return self.subtree_max_weight[u]

        is_leaf = all(child in self.on_stack for child in self.tree[u].children)

        if is_leaf:
            self.subtree_max_weight[u] = self.tree[u].weight
            return self.subtree_max_weight[u]

        self.on_stack.add(u)

        # Option 1
        include_u_weight = self.tree[u].weight

        for child in self.tree[u].children:
            if child in self.on_stack:
                continue

            self.on_stack.add(child)

            for grandchild in self.tree[child].children:
                if grandchild not in self.on_stack:
                    include_u_weight += self.dfs(grandchild)

            self.on_stack.remove(child)

        # Option 2
        exclude_u_weight = 0

        for child in self.tree[u].children:
            if child not in self.on_stack:
                exclude_u_weight += self.dfs(child)

        self.on_stack.remove(u)

        self.subtree_max_weight[u] = max(include_u_weight, exclude_u_weight)

        return self.subtree_max_weight[u]


def main():
    data = sys.stdin.read().split("\n")
    tree = build_tree(data)
    weight = MaxWeightIndependentSetSolver(tree).result
    print(weight)


if __name__ == "__main__":
    # This is to avoid stack overflow issues
    threading.Thread(target=main).start()
