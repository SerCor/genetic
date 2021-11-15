import pytest

from genetic.individual import Individual 


@pytest.fixture
def individual():
    return Individual(
        epsilon=10,
        min_samples=100
    )
        

def test_individual_repr(individual: Individual) -> None:
    assert (
        'Individual(epsilon=10,min_samples=100)' == repr(individual)
    )
