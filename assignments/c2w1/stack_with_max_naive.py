import sys


class StackWithMax:
    def __init__(self):
        self.stack = []
        self.max_indices_stack = []

    def Push(self, a):
        if not self.max_indices_stack or a > self.stack[self.max_indices_stack[-1]]:
            self.max_indices_stack.append(len(self.stack))

        self.stack.append(a)

    def Pop(self):
        assert len(self.stack)
        if self.max_indices_stack[-1] == len(self.stack) - 1:
            self.max_indices_stack.pop()

        self.stack.pop()

    def Max(self):
        assert len(self.stack)
        return self.stack[self.max_indices_stack[-1]]


if __name__ == "__main__":
    stack = StackWithMax()

    num_queries = int(sys.stdin.readline())
    for _ in range(num_queries):
        query = sys.stdin.readline().split()

        if query[0] == "push":
            stack.Push(int(query[1]))
        elif query[0] == "pop":
            stack.Pop()
        elif query[0] == "max":
            print(stack.Max())
        else:
            assert 0
