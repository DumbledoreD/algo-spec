import sys
import threading

sys.setrecursionlimit(10 ** 7)  # max depth of recursion
threading.stack_size(2 ** 27)  # new thread will get stack of such size


def is_bst(node_index, min_key, max_key, tree):
    if not tree or node_index == -1:
        return True

    key, left_child_index, right_child_index = tree[node_index]

    if not (min_key <= key < max_key):
        return False

    # Key same as parent cannot have left child.
    if key == min_key and not left_child_index == -1:
        return False

    return is_bst(left_child_index, min_key, key, tree) and is_bst(
        right_child_index, key, max_key, tree
    )


def main():
    nodes = int(sys.stdin.readline().strip())
    tree = []
    for _ in range(nodes):
        tree.append(list(map(int, sys.stdin.readline().strip().split())))

    print("CORRECT" if is_bst(0, -float("inf"), float("inf"), tree) else "INCORRECT")


if __name__ == "__main__":
    threading.Thread(target=main).start()
