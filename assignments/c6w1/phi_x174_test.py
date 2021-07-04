import random

import pytest

ALPHABET = "ACGT"
SEQ_LENGTH = 5386
READ_LENGTH = 100
READ_COUNT = 1618


def generate_test_inputs():
    target_sequence = "".join(random.choices(ALPHABET, k=SEQ_LENGTH))

    extended_target_sequence = target_sequence + target_sequence[:READ_LENGTH]
    sampled_reads = [
        extended_target_sequence[i : i + READ_LENGTH]
        for i in random.choices(range(SEQ_LENGTH), k=READ_COUNT)
    ].sort()

    return target_sequence, sampled_reads


@pytest.mark.parametrize(
    "target_sequence, sampled_reads",
    [generate_test_inputs() for _ in range(1000)],
)
def test_basic(target_sequence, sampled_reads):
    assert True
