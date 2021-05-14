import sys


def bwt(text):
    original_length = len(text)
    text += text
    rotations = [text[i : i + original_length] for i in range(original_length)]
    rotations.sort()
    return "".join(r[-1] for r in rotations)


if __name__ == "__main__":
    text = sys.stdin.readline().strip()
    print(bwt(text))
