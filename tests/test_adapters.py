from math import isclose

import pytest 

from genetic.adapters import IndividualAdapter
from genetic.settings import N_BITS_EPSILON, RANGE_EPSILON


def is_close_epsilon(value: float, partition_value: float) -> bool:
    low, high = RANGE_EPSILON
    n_partitions = N_BITS_EPSILON ** 2
    step_per_partition = (high - low) / n_partitions

    return isclose(value, partition_value) or abs(value - partition_value) < step_per_partition


def test_from_bits(bits_10_100: str):
    individual = IndividualAdapter.from_bits(bits_10_100)
    assert is_close_epsilon(individual.instance.epsilon, 10)
    assert individual.instance.min_samples == 100
    assert individual.min_samples == bits_10_100[N_BITS_EPSILON:]
    assert individual.epsilon == bits_10_100[:N_BITS_EPSILON]


def test_binay_fields_access(individual_10_100: IndividualAdapter, bits_10_100):
    bits_epsilon = bits_10_100[:N_BITS_EPSILON]
    bits_min_samples = bits_10_100[N_BITS_EPSILON:]

    assert individual_10_100.epsilon, bits_epsilon
    assert individual_10_100.min_samples ==  bits_min_samples


def test_binay_fields_change(bits_10_100: str):
    individual = IndividualAdapter.random()
    bits_epsilon = bits_10_100[:N_BITS_EPSILON]
    bits_min_samples = bits_10_100[N_BITS_EPSILON:]

    individual.epsilon = bits_epsilon
    individual.min_samples = bits_min_samples
    
    assert individual.epsilon == bits_epsilon
    assert individual.min_samples == bits_min_samples
    assert is_close_epsilon(10, individual.instance.epsilon)
    assert 100 == individual.instance.min_samples
    

def test_set_bits(bits_10_100: str):
    individual = IndividualAdapter.random()
    individual.set_bits(bits_10_100)
    assert is_close_epsilon(individual.instance.epsilon, 10)
    assert individual.instance.min_samples == 100


def test_get_bits(individual_10_100: IndividualAdapter, bits_10_100: str):
    assert individual_10_100.get_bits() == bits_10_100


def test_len(individual_10_100: IndividualAdapter, bits_10_100: str):
    assert len(individual_10_100) == len(bits_10_100)


def test_repr(individual_10_100: IndividualAdapter):
    expected = 'IndividualAdapter(instance=Individual(epsilon=10,min_samples=100),score=None)'
    assert repr(individual_10_100) == expected
