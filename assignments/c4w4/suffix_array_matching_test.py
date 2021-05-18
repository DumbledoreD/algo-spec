import random

import pytest

from .suffix_array_matching import ALPHABET
from .suffix_array_matching import find_matches as fast

TRUE_ALPHABET = ALPHABET[1:]


def slow(text, patterns):
    matches = set()

    for pattern in patterns:
        for i in range(len(text) - len(pattern) + 1):
            if text[i : i + len(pattern)] == pattern:
                matches.add(i)

    return matches


@pytest.mark.parametrize(
    "text, pattern",
    [
        (
            "".join([random.choice(TRUE_ALPHABET) for char in range(50)] + ["$"]),
            "".join(
                [random.choice(TRUE_ALPHABET) for char in range(random.randrange(1, 4))]
            ),
        )
        for trial in range(10000)
    ],
)
def test_stress(text, pattern):
    assert fast(text, [pattern]) == slow(text, [pattern])
