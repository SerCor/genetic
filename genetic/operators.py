'Operators for mutation and crossover'
import random
from typing import Tuple, List

from .adapters import IndividualAdapter


def mutate(instance: IndividualAdapter) -> IndividualAdapter:
    'flip bit mutation'
    bit_index = random.randint(0, len(instance) - 1)
    flipped_bit = '1' if instance[bit_index] == '0' else '0'
    new_bits = instance[:bit_index] + flipped_bit + instance[bit_index+1:]

    return IndividualAdapter.from_bits(new_bits, score=instance.score)


def uniform_crossover(
        instance1: IndividualAdapter,
        instance2: IndividualAdapter) -> List[IndividualAdapter]:
    
    return [IndividualAdapter.from_bits(
        ''.join([random.choice([bit1, bit2]) for bit1, bit2 in zip(instance1, instance2)]))]


def single_point_crossover(instance1: IndividualAdapter, 
        instance2: IndividualAdapter) -> Tuple[IndividualAdapter, IndividualAdapter]:
    cross_point = random.randint(1, len(instance1) - 2)

    return (
            IndividualAdapter.from_bits(instance1[:cross_point] + instance2[cross_point:]),
            IndividualAdapter.from_bits(instance2[:cross_point] + instance1[cross_point:])
    )
