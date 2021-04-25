import sys
import threading
from collections import defaultdict


def compute_height(parents):
    root, graph = build_graph(parents)

    stack = [root]
    next_stack = []
    level = 0

    while stack:
        level += 1

        next_stack = []
        for node in stack:
            next_stack.extend(graph[node])

        stack = next_stack

    return level


def build_graph(parents):
    root = None
    graph = defaultdict(list)

    for child, parent in enumerate(parents):
        if parent == -1:
            root = child
        else:
            graph[parent].append(child)

    return root, graph


def main():
    n = int(input())  # noqa: F841
    parents = list(map(int, input().split()))
    print(compute_height(parents))


# In Python, the default limit on recursion depth is rather low,
# so raise it here for this problem. Note that to take advantage
# of bigger stack, we have to launch the computation in a new thread.
if __name__ == "__main__":
    sys.setrecursionlimit(10 ** 7)  # max depth of recursion
    threading.stack_size(2 ** 27)  # new thread will get stack of such size
    threading.Thread(target=main).start()
