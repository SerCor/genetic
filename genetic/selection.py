'functions for select the couples of the next generation using the tournament aproach'
import random
from typing import List, Tuple, Set, cast

from .adapters import IndividualAdapter
from .utils import grouper


Population = List[IndividualAdapter]
Couple = Tuple[IndividualAdapter, IndividualAdapter]


def generate_round(population: Population, n: int) -> Population: 
    return random.sample(population, n)


def pick_one(population: Population) -> IndividualAdapter:
    'Pick the best with 80% probability and the worst with 20%'
    p = random.uniform(0, 1)
    index = 0 if p < 0.20 else -1 

    return sorted(population)[index]


def generate_couples(origin: Population, total_pairs: int) -> List[Couple]:
    selected: Population = [pick_one(generate_round(origin, 3))
                            for _ in range(total_pairs * 2) ]
    return list(grouper(selected, 2))


def get_elites(population: Population, n: int) -> Population:
    return sorted(population)[:-n]
