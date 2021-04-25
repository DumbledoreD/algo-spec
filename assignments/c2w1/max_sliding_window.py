from collections import deque


def max_sliding_window(sequence, m):
    maximums = []
    index_queue = deque()

    for i in range(len(sequence)):
        cur_num = sequence[i]

        # Remove out of window indices
        while index_queue and i - index_queue[0] >= m:
            index_queue.popleft()

        # Remove smaller elements
        while index_queue and sequence[index_queue[-1]] <= cur_num:
            index_queue.pop()

        index_queue.append(i)

        if i >= m - 1:
            maximums.append(sequence[index_queue[0]])

    return maximums


def max_sliding_window_naive(sequence, m):
    maximums = []
    for i in range(len(sequence) - m + 1):
        maximums.append(max(sequence[i : i + m]))

    return maximums


if __name__ == "__main__":
    n = int(input())
    input_sequence = [int(i) for i in input().split()]
    assert len(input_sequence) == n
    window_size = int(input())

    print(*max_sliding_window(input_sequence, window_size))
