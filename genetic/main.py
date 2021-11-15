import argparse
from concurrent.futures import wait
from itertools import chain
import random
from typing import List

from .adapters import IndividualAdapter
from .state import State, persist_state, read_state
from .operators import uniform_crossover, mutate, single_point_crossover, two_point_crossover
from .selection import generate_couples, get_elites
from .settings import (
    RATE_MUTATION, SIZE_ELITE,
    MAX_EPOCHS, POPULATION_SIZE,
    OUTDIR, INCREMENT_RATE_MUTATION
)
from .utils import preprend


def crossover_stage(state: State) -> List[IndividualAdapter]:    
    # Generate couples
    required_couples = (POPULATION_SIZE - SIZE_ELITE) // 3
    operators = [uniform_crossover, two_point_crossover]
    couples = generate_couples(state.population, required_couples)

    # Select the elites
    elites = get_elites(state.population, SIZE_ELITE) 
    return [*elites, *chain.from_iterable([o(*c) for c in couples for o in operators])]
 

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


def get_args():
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-r', '--resume', type=str, help='output file from resume')
    group.add_argument('-d', '--dataset', type=str, help='path to dataset')

    return parser.parse_args()


def main():
    args = get_args()
    state = None

    if(args.resume is None):
        state = State.initial(
            population_size=POPULATION_SIZE,
            max_epoch=MAX_EPOCHS,
            mutation_rate=RATE_MUTATION,
            mutation_rate_increment=INCREMENT_RATE_MUTATION,
            dataset=args.dataset
        )
    else:
        state = read_state(args.resume)

    while not state.is_finished:
        print(f'Generation #{state.epoch}')
        next_generation = crossover_stage(state)
        persist_current_state(state)
        state.evolution(next_generation)
        mutation = mutate_stage(state)


if __name__ == '__main__':
    main()
