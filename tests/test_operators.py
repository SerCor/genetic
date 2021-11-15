import pytest

from genetic.adapters import IndividualAdapter
from genetic.operators import mutate


def test_mutate(individual_10_100: IndividualAdapter, bits_10_100: str) -> None:
    mutated_instance = mutate(individual_10_100)
    assert sum(map(lambda bits: 0 if bits[0] == bits[1] else 1,
            zip(mutated_instance.get_bits(), bits_10_100))) == 1

