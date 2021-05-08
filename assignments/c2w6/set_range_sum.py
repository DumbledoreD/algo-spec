from sys import stdin


# Vertex of a splay tree
class Vertex:
    def __init__(self, key, left, right, parent, subtree_sum):
        self.key, self.left, self.right, self.parent = key, left, right, parent
        self.sum = subtree_sum


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

    update_sum(p)
    update_sum(n)


def update_sum(n):
    if not n:
        return

    n.sum = n.key + (n.left.sum if n.left else 0) + (n.right.sum if n.right else 0)


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


def find(key, root):
    """Searches for key in the tree and splay the deepest visited node.

    Returns (result, new_root).

    If found, result is a pointer to the node with the given key.

    Otherwise, result is a pointer to the node with the smallest bigger key.

    If the key is bigger than all keys in the tree, then result is None.
    """
    prev_node = cur_node = root
    next_node = None

    while cur_node:
        # Note this, nice way to track the next_node
        if cur_node.key >= key and (next_node is None or cur_node.key < next_node.key):
            next_node = cur_node

        prev_node = cur_node

        if cur_node.key == key:
            break

        if cur_node.key < key:
            cur_node = cur_node.right

        else:
            cur_node = cur_node.left

    root = splay(prev_node)

    return (next_node, root)


def split(key, root):
    (result, root) = find(key, root)

    if result is None:  # All values in tree are smaller than key
        return (root, None)

    right = splay(result)

    # Cut left, note right will include the node with "key" if there is one
    left = right.left
    right.left = None
    if left:
        left.parent = None

    update_sum(left)
    update_sum(right)

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

    update_sum(root)

    return root


def insert(key, root):
    (left, right) = split(key, root)

    new_node = None
    if not (right and right.key == key):
        new_node = Vertex(key, None, None, None, key)

    return merge(merge(left, new_node), right)


def delete(key, root):
    (left, right) = split(key, root)

    if right and right.key == key:
        # Remove right root
        right = right.right
        if right:
            right.parent = None

    return merge(left, right)


def range_sum(fr, to, root):
    fr, to = min(fr, to), max(fr, to)

    # left < fr. middle >= fr
    (left, middle) = split(fr, root)
    # middle < to + 1, right >= to + 1
    (middle, right) = split(to + 1, middle)

    return middle.sum if middle else 0, merge(merge(left, middle), right)


if __name__ == "__main__":
    n, *lines = stdin.read().split("\n")

    MODULO = 1000000001
    root = None

    last_sum_result = 0

    for line in lines:
        if not line:
            continue

        line = line.split()

        if line[0] == "+":
            x = int(line[1])
            root = insert((x + last_sum_result) % MODULO, root)

        elif line[0] == "-":
            x = int(line[1])
            root = delete((x + last_sum_result) % MODULO, root)

        elif line[0] == "?":
            x = (int(line[1]) + last_sum_result) % MODULO
            result, root = find(x, root)
            print("Found" if result and result.key == x else "Not found")

        elif line[0] == "s":
            l = int(line[1])
            r = int(line[2])
            result, root = range_sum(
                (l + last_sum_result) % MODULO, (r + last_sum_result) % MODULO, root
            )
            print(result)
            last_sum_result = result % MODULO
