import pytest

from .process_packages import Buffer, Request, Response, process_requests


@pytest.mark.parametrize(
    "buffer, requests, expected",
    [
        (
            Buffer(1),
            [Request(0, 0)],
            [Response(False, 0)],
        ),
        (
            Buffer(1),
            [Request(0, 1), Request(0, 1)],
            [Response(False, 0), Response(True, -1)],
        ),
        (
            Buffer(1),
            [Request(0, 1), Request(1, 1)],
            [Response(False, 0), Response(False, 1)],
        ),
        (
            Buffer(2),
            [Request(0, 2), Request(1, 1)],
            [Response(False, 0), Response(False, 2)],
        ),
    ],
)
def test_basic(buffer, requests, expected):
    assert process_requests(requests, buffer) == expected
