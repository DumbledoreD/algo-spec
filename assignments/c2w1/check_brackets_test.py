import pytest

from .check_brackets import find_mismatch


@pytest.mark.parametrize(
    "text, expected",
    [
        ("{}[]()", None),
        ("{[()]}", None),
        ("(())", None),
        ("{", 0),
        ("{[}", 2),
        ("{[(", 0),
        ("[](()", 2),
    ],
)
def test_basic(text, expected):
    assert find_mismatch(text) == expected
