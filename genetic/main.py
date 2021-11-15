import argparse
from concurrent.futures import wait
from itertools import chain
import random
from typing import List

from .adapters import IndividualAdapter
from .dbscan import compute_perfomance
from .state import State, persist_state
from .operators import uniform_crossover, mutate, single_point_crossover
from .selection import generate_couples, get_elites
from .settings import (
    RATE_MUTATION, SIZE_ELITE,
    MAX_EPOCHS, POPULATION_SIZE,
    OUTDIR, INCREMENT_RATE_MUTATION
)
from .utils import preprend


def crossover_stage(state: State) -> List[IndividualAdapter]:    
    # Select the elites
    breakpoint()
    elites = get_elites(state.population, SIZE_ELITE) 

    # Generate rest of the generation
    required_couples = (POPULATION_SIZE - SIZE_ELITE) // 3
    operators = [uniform_crossover, single_point_crossover]
    couples = generate_couples(state.population, required_couples)

    return list(chain.from_iterable([o(*c) for c in couples for o in operators]))
 

def mutate_stage(state: State) -> State:
    new_population: List[IndividualAdapter] = []

    for instance in state.population:
        if(random.uniform(0, 1) <= state.mutation_rate):
            new_population.append(mutate(instance))
        else:
            new_population.append(instance)
    
    state.population = new_population
    return state


def persist_current_state(state: State) -> None:
    out_filename = f'{OUTDIR}/generation_{state.epoch}'
    persist_state(out_filename, state)


def precompute_scores(state: State) -> None:
    for adapter in state.population:
        fitness = compute_perfomance(min_samples=adapter.instance.min_samples,
                                     epsilon=adapter.instance.epsilon)
        adapter.score = fitness


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-r', '--resume', type=str)
    return parser.parse_args()


def main():
    args = get_args()
    state = None

    if(args.resume is None):
        state = State.initial(
            population_size=POPULATION_SIZE,
            max_epoch=MAX_EPOCHS,
            mutation_rate=RATE_MUTATION,
            mutation_rate_increment=INCREMENT_RATE_MUTATION
        )
    else:
        state = read_state(args.resume)

    while not state.is_finished:
        precompute_scores(state)
        persist_current_state(state)
        next_generation = crossover_stage(state)
        state.evolution(next_generation)
        mutation = mutate_stage(state)


if __name__ == '__main__':
    main()
