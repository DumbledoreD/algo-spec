import pytest

from .change import get_change


@pytest.mark.parametrize(
    "m, expected",
    [
        pytest.param(1, 1, id="only 1s"),
        pytest.param(5, 1, id="only 5s"),
        pytest.param(10, 1, id="only 10s"),
        pytest.param(28, 6, id="general"),
        pytest.param(999, 104, id="large num"),
    ],
)
def test_basic(m, expected):
    assert get_change(m) == expected
