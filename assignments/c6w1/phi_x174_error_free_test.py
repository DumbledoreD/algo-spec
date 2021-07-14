import random

import pytest

from .phi_x174_error_free import SequenceAssembler

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
    ]
    sampled_reads.sort()

    return target_sequence, sampled_reads


def are_rotations(text_1, text_2):
    if len(text_1) != len(text_2):
        return False

    extended_text_1 = text_1 * 2

    return text_2 in extended_text_1


@pytest.mark.parametrize(
    "target_sequence, sampled_reads",
    [generate_test_inputs() for _ in range(1000)],
)
def test_basic(target_sequence, sampled_reads):
    assert are_rotations(SequenceAssembler(sampled_reads).result, target_sequence)
