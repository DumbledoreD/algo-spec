import sys
import threading

sys.setrecursionlimit(10 ** 6)  # max depth of recursion
threading.stack_size(2 ** 27)  # new thread will get stack of such size


class TreeOrders:
    def read(self):
        self.n = int(sys.stdin.readline())
        self.key = [0 for i in range(self.n)]
        self.left = [0 for i in range(self.n)]
        self.right = [0 for i in range(self.n)]
        for i in range(self.n):
            [a, b, c] = map(int, sys.stdin.readline().split())
            self.key[i] = a
            self.left[i] = b
            self.right[i] = c

    def inOrder(self, node_index):
        if node_index != -1:
            self.inOrder(self.left[node_index])
            print(self.key[node_index], end=" ")
            self.inOrder(self.right[node_index])

    def preOrder(self, node_index):
        if node_index != -1:
            print(self.key[node_index], end=" ")
            self.preOrder(self.left[node_index])
            self.preOrder(self.right[node_index])

    def postOrder(self, node_index):
        if node_index != -1:
            self.postOrder(self.left[node_index])
            self.postOrder(self.right[node_index])
            print(self.key[node_index], end=" ")


def main():
    tree = TreeOrders()
    tree.read()
    tree.inOrder(0)
    print()
    tree.preOrder(0)
    print()
    tree.postOrder(0)


if __name__ == "__main__":
    threading.Thread(target=main).start()
