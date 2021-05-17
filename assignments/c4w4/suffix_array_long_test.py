import random

import pytest

from .suffix_array_long import ALPHABET
from .suffix_array_long import build_suffix_array as fast

TRUE_ALPHABET = ALPHABET[1:]


def slow(text):
    suffixes = [(text[i:], i) for i in range(len(text))]
    suffixes.sort()
    return [start for _, start in suffixes]


@pytest.mark.parametrize(
    "text",
    [
        "".join([random.choice(TRUE_ALPHABET) for char in range(50)] + ["$"])
        for trial in range(10000)
    ],
)
def test_stress(text):
    assert fast(text) == slow(text)
