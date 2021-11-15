'function tools'
from itertools import chain, zip_longest
from random import choices


def weighted_sample_without_replacement(population, weights, k=1):
    weights = list(weights)
    positions = range(len(population))
    indices = []

    while True:
        needed = k - len(indices)
        if not needed:
            break
        for i in choices(positions, weights, k=needed):
            if weights[i]:
                weights[i] = 0.0
                indices.append(i)

    return [population[i] for i in indices]


def preprend(value, itr):
    return chain([value], itr)


def grouper(iterable, n, fillvalue=None):
    args = [iter(iterable)] * n
    return zip_longest(*args, fillvalue=fillvalue)
