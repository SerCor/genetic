import pytest
from math import isclose
from typing import Dict, List

from genetic.state import State, parse_state


@pytest.fixture
def initial_data() -> Dict:
    return {
        'population_size': 66,
        'max_epoch': 44,
        'mutation_rate': 0.3,
        'mutation_rate_increment': 0.1
    }


@pytest.fixture
def initial_state(initial_data: Dict) -> State:
    return State.initial(
            population_size=initial_data['population_size'],
            max_epoch=initial_data['max_epoch'],
            mutation_rate=initial_data['mutation_rate'],
            mutation_rate_increment=initial_data['mutation_rate_increment']
    )


def test_state_initial_named_constructor(initial_state: State, initial_data: Dict) -> None:
    assert len(initial_state.population) == initial_data['population_size'] 
    assert initial_state.max_epoch == initial_data['max_epoch'] 
    assert isclose(initial_state.mutation_rate, initial_data['mutation_rate'])
    assert isclose(initial_state.mutation_rate_increment, initial_data['mutation_rate_increment'])


def test_state_evolution_method(initial_state: State) -> None:
    new_generation: List = []
    old_epoch = initial_state.epoch
    old_mutation_rate = initial_state.mutation_rate
    mutation_rate_increment = initial_state.mutation_rate_increment
    initial_state.evolution(new_generation)

    assert initial_state.epoch == old_epoch + 1
    assert initial_state.population == new_generation
    assert isclose(initial_state.mutation_rate, old_mutation_rate + mutation_rate_increment)
    assert isclose(initial_state.mutation_rate_increment, mutation_rate_increment)


def test_state_is_not_finished(initial_state: State) -> None:
    assert initial_state.is_finished == False


def test_state_is_finisihed_true_by_max_epoch(initial_state: State):
    initial_state.epoch = initial_state.max_epoch
    assert initial_state.is_finished == True


def test_state_is_finished_by_truncated_population(individual_10_100, initial_state: State):
    initial_state.population = [individual_10_100] * 10
    assert initial_state.is_finished == True


def test_state_repr(initial_state: State, initial_data: Dict) -> None:
    assert repr(initial_state) == (
            f'State('
            'epoch=0,'
            f'population={initial_state.population!r},'
            f'max_epoch={initial_data["max_epoch"]!r},'
            f'mutation_rate={initial_data["mutation_rate"]!r},'
            f'mutation_rate_increment={initial_data["mutation_rate_increment"]!r}'
            ')'
        )


def test_success_parse_state(initial_state: State) -> None:
    assert isinstance(parse_state(repr(initial_state)), State)
