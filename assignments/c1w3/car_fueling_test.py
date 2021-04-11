import pytest

from .car_fueling import compute_min_refills


@pytest.mark.parametrize(
    "distance, tank, stops, expected",
    [
        pytest.param(5, 1, [2, 3, 4], -1, id="impossible first stop"),
        pytest.param(5, 1, [1, 2, 3], -1, id="impossible last stop"),
        pytest.param(5, 2, [1, 2, 3], 2, id="general "),
        pytest.param(5, 3, [1, 2, 3], 1, id="general "),
    ],
)
def test_basic(distance, tank, stops, expected):
    assert compute_min_refills(distance, tank, stops) == expected
