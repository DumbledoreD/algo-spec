import sys


def merge_sort(a):
    if len(a) == 1:
        return a

    m = len(a) // 2
    left = a[:m]
    right = a[m:]

    sorted_left = merge_sort(left)
    sorted_right = merge_sort(right)

    return merge(sorted_left, sorted_right)


def merge(left, right):
    i = j = 0
    merged_array = []

    while i < len(left) and j < len(right):
        if left[i] < right[j]:
            merged_array.append(left[i])
            i += 1
        else:
            merged_array.append(right[j])
            j += 1

    merged_array += left[i:] + right[j:]

    return merged_array


def merge_sort_plus(a):
    if len(a) == 1:
        return a, 0

    m = len(a) // 2
    left = a[:m]
    right = a[m:]

    sorted_left, inversion_count_left = merge_sort_plus(left)
    sorted_right, inversion_count_right = merge_sort_plus(right)

    merged_array, inversion_count_merged = merge_plus(sorted_left, sorted_right)

    return merged_array, (
        inversion_count_left + inversion_count_right + inversion_count_merged
    )


def merge_plus(left, right):
    i = j = inversion_count = 0
    merged_array = []

    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            merged_array.append(left[i])
            i += 1
        else:
            merged_array.append(right[j])
            j += 1
            # Plus the num of the elements on the left that are larger
            inversion_count += len(left) - i

    merged_array += left[i:] + right[j:]

    return merged_array, inversion_count


def get_number_of_inversions(a):
    _, inversion_count = merge_sort_plus(a)
    return inversion_count


if __name__ == "__main__":
    n, *a = list(map(int, sys.stdin.read().split()))
    print(get_number_of_inversions(a))
