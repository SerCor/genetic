from collections import Counter
from typing import List

from .adapters import IndividualAdapter
from .selection import Population


def compute_schema_statistics(population: Population):
    'Compute the number of 0s and 1s in each gen of the population'
    len_population = len(population)
    population_bits = [adapter.get_bits() for adapter in population]
    
    counters: List[Counter] = []
    statistics = []

    for gen_bits in zip(*population_bits):
        counters.append(Counter(gen_bits))

    for contador in counters:
        statistics.append({
            '0': contador['0'] / len_population,
            '1': contador['1'] / len_population
        })

    return statistics


def has_truncated_schema(population: Population, truncated_gen_threshold=0.90,
                         truncated_population_threshold=.90) -> bool:
    schema_statistics = compute_schema_statistics(population)
    len_population = len(population[0])
    truncated_counter = 0

    for gen_statistics in schema_statistics:
        if (gen_statistics['0'] >= truncated_gen_threshold
             or gen_statistics['0'] <= 1 - truncated_gen_threshold):
            truncated_counter += 1

    return (truncated_counter / len_population) >= truncated_population_threshold 
