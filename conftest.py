import pytest

from genetic.convert import float2bits, int2bits
from genetic.adapters import IndividualAdapter
from genetic.individual import Individual
from genetic.settings import (
    N_BITS_EPSILON, N_BITS_MIN_SAMPLES, RANGE_EPSILON
)


@pytest.fixture
def bits_10_100() -> str:
    low, high = RANGE_EPSILON
    epsilon_bits = float2bits(10, low, high, N_BITS_EPSILON)
    min_samples_bits = int2bits(100, 1, N_BITS_MIN_SAMPLES)

    return epsilon_bits + min_samples_bits


@pytest.fixture
def individual_10_100() -> IndividualAdapter:
    return IndividualAdapter(
        instance=Individual(
            epsilon=10,
            min_samples=100
        )
    )
