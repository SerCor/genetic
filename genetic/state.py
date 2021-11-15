'definition of state class. Define the current state of the genetic algorithm'
from dataclasses import dataclass
from typing import List
import os

from .adapters import IndividualAdapter
from .schemas import has_truncated_schema
from .selection import Population
from .individual import Individual # for parse


@dataclass
class State:
    epoch: int
    population: Population
    max_epoch: int
    mutation_rate: float
    mutation_rate_increment: float

    @classmethod
    def initial(cls, population_size: int, max_epoch: int, mutation_rate: float, mutation_rate_increment: float) -> 'State':
        return cls(
            epoch=0,
            population=[IndividualAdapter.random() for _ in range(population_size)],
            max_epoch=max_epoch,
            mutation_rate=mutation_rate,
            mutation_rate_increment=mutation_rate_increment
        )
    
    def evolution(self, next_generation: Population) -> None:
        self.epoch += 1
        self.population = next_generation
        self.mutation_rate += self.mutation_rate_increment

    @property
    def is_finished(self) -> bool:
        return self.epoch >= self.max_epoch or has_truncated_schema(self.population)

    def __repr__(self) -> str:
        return (
            'State('
            f'epoch={self.epoch!r},'
            f'population={self.population!r},'
            f'max_epoch={self.max_epoch!r},'
            f'mutation_rate={self.mutation_rate!r},'
            f'mutation_rate_increment={self.mutation_rate_increment!r}'
            ')'
        )


def persist_state(filename: str, state: State) -> None:
    os.makedirs(os.path.dirname(filename), exist_ok=True)

    with open(filename, encoding='utf-8', mode='w') as fp:
        fp.write(repr(state))


def parse_state(state_repr: str) -> State:
    return eval(state_repr)


def read_state(filename: str) -> State:
    with open(filename, mode='r', encoding='utf-8') as fp:
        return parse_state(''.join(fp.readlines()))
