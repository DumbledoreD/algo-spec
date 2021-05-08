import sys


class Rope:
    def __init__(self, s):
        self.tree = self.build_tree(s)

    def build_tree(self, s):
        root = None

        for letter in s:
            v = Vertex(letter)
            root = merge(root, v)

        return root

    def process(self, i, j, k):
        le_j, g_j = split(j + 2, self.tree)

        l_i, ge_i_le_j = split(i + 1, le_j)

        remaining_string = merge(l_i, g_j)

        le_k, g_k = split(k + 1, remaining_string)

        self.tree = merge(merge(le_k, ge_i_le_j), g_k)

    def __str__(self):
        return str(self.tree)


class Vertex:
    def __init__(self, key, left=None, right=None, parent=None, size=1):
        self.key, self.left, self.right, self.parent = key, left, right, parent
        self.size = size

    def __repr__(self):
        return f"Vertex({self.key}, {self.size})"

    def __str__(self):
        cur_node = self
        stack = []
        result = []

        while cur_node or stack:
            if cur_node:
                stack.append(cur_node)
                cur_node = cur_node.left

            else:
                cur_node = stack.pop()
                result.append(cur_node.key)
                cur_node = cur_node.right

        return "".join(result)


# Splay tree implementation


# Makes splay of the given vertex till it the new root.
def splay(n):
    while n and n.parent:
        if n.parent.parent:
            bigRotation(n)
        else:
            smallRotation(n)
    return n


def smallRotation(n):
    p = n.parent
    q = p and p.parent

    if p is None:
        return

    if p.left == n:  # n is the left child
        #   p        n
        #  /          \
        # n    --->    p
        #  \          /
        #   nr       nr
        nr = n.right

        n.right = p
        p.left = nr

        p.parent = n
        if nr:
            nr.parent = p

    else:  # n is the right child
        # p              n
        #  \            /
        #   n   --->   p
        #  /            \
        # nl             nl
        nl = n.left

        n.left = p
        p.right = nl

        p.parent = n
        if nl:
            nl.parent = p

    # Update n <---> q
    n.parent = q
    if q:
        if q.left == p:
            q.left = n
        else:
            q.right = n

    update_size(p)
    update_size(n)


def update_size(n):
    if not n:
        return

    n.size = 1 + (n.left.size if n.left else 0) + (n.right.size if n.right else 0)


def bigRotation(n):
    if (n.parent.left == n and n.parent.parent.left == n.parent) or (
        n.parent.right == n and n.parent.parent.right == n.parent
    ):
        # Left zig-zig
        #     q             p            n
        #    /           /     \          \
        #   p           n       q          p
        #  / \           \     /          / \
        # n   pr          nr  pr         nr  q
        #  \                                /
        #   nr                             pr
        # Right zig-zig
        # q                 p                  n
        #  \             /     \              /
        #   p           q       n            p
        #  / \           \     /            / \
        # pl  n           pl  nl           q   nl
        #    /                              \
        #   nl                               pl
        smallRotation(n.parent)
        smallRotation(n)
    else:
        # Left zig-zag
        #   q               q               n
        #  /               /             /     \
        # p               n             p       q
        #  \             / \             \     /
        #   n           p   nr            nl  nr
        #  / \           \
        # nl  nr          nl
        # Right zig-zag
        #   q             q                 n
        #    \             \             /     \
        #     p             n           q       p
        #    /             / \           \     /
        #   n             nl  p           nl  nr
        #  / \               /
        # nl  nr            nr
        smallRotation(n)
        smallRotation(n)


def find(k, root):
    """Find the k-th smallest element in the tree and splay the deepest visited node.

    Return (result, new_root).

    If k is greater than the number of elements, then result is None
    """
    prev_node = cur_node = root

    while cur_node:

        cur_node_rank = cur_node.left.size + 1 if cur_node.left else 1

        if k == cur_node_rank:
            break

        prev_node = cur_node

        if k < cur_node_rank:
            cur_node = cur_node.left

        else:
            cur_node = cur_node.right
            k -= cur_node_rank

    root = splay(prev_node)

    return (cur_node, root)


def split(key, root):
    """Split by the k-th smallest element in the tree.

    Return (left, right).

    The k-th smallest element is the root of the right tree.
    """
    (result, root) = find(key, root)

    if result is None:  # All values in tree are smaller than key
        return (root, None)

    right = splay(result)

    # Cut left, note right includes the node with "key" if there is one
    left = right.left
    right.left = None
    if left:
        left.parent = None

    update_size(left)
    update_size(right)

    return (left, right)


def merge(left, right):
    if not (left and right):
        return left or right

    while right.left:
        right = right.left

    # Move the smallest node on the right to the right's root
    # Then add left to the right's root
    root = splay(right)
    root.left = left
    left.parent = root

    update_size(root)

    return root


if __name__ == "__main__":
    s, n, *queries = sys.stdin.read().split("\n")

    rope = Rope(s.strip())

    for q in queries:
        q = q.strip()
        if q:
            i, j, k = map(int, q.split())
            rope.process(i, j, k)

    print(rope)
