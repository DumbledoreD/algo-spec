# python3

from collections import namedtuple

Bracket = namedtuple("Bracket", ["char", "position"])


def are_matching(left, right):
    return (left + right) in ["()", "[]", "{}"]


def find_mismatch(text):
    opening_brackets_stack = []
    for i, char in enumerate(text):
        if char in "([{":
            # Process opening bracket, write your code here
            opening_brackets_stack.append(Bracket(char, i))

        if char in ")]}":
            # Process closing bracket, write your code here
            if opening_brackets_stack and are_matching(
                opening_brackets_stack[-1].char, char
            ):
                opening_brackets_stack.pop()
            else:
                return i

    return opening_brackets_stack[0].position if opening_brackets_stack else None


def main():
    text = input()
    mismatch = find_mismatch(text)
    # Printing answer, write your code here
    print(mismatch + 1 if mismatch is not None else "Success")


if __name__ == "__main__":
    main()
