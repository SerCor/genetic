'Operators for mutation and crossover'
import random
from typing import Tuple, List

from .adapters import IndividualAdapter


def mutate(instance: IndividualAdapter) -> IndividualAdapter:
    'flip bit mutation'
    bit_index = random.randint(0, len(instance) - 1)
    flipped_bit = '1' if instance[bit_index] == '0' else '0'
    new_bits = instance[:bit_index] + flipped_bit + instance[bit_index+1:]

    return IndividualAdapter.from_bits(new_bits, score=instance.score, dataset=instance.dataset)


def uniform_crossover(
        instance1: IndividualAdapter,
        instance2: IndividualAdapter) -> List[IndividualAdapter]:
    
    return [IndividualAdapter.from_bits(
        ''.join([random.choice([bit1, bit2]) for bit1, bit2 in zip(instance1, instance2)]), dataset=instance1.dataset)]


def single_point_crossover(instance1: IndividualAdapter, 
        instance2: IndividualAdapter) -> Tuple[IndividualAdapter, IndividualAdapter]:
    cross_point = random.randint(1, len(instance1) - 2)

    return (
            IndividualAdapter.from_bits(instance1[:cross_point] + instance2[cross_point:], dataset=instance1.dataset),
            IndividualAdapter.from_bits(instance2[:cross_point] + instance1[cross_point:], dataset=instance1.dataset)
    )


def two_point_crossover(instance1: IndividualAdapter, 
        instance2: IndividualAdapter) -> Tuple[IndividualAdapter, IndividualAdapter]:
    p1, p2 = sorted(random.sample(range(1, len(instance1) - 1), 2))
    m1, m2 = instance1.get_bits(), instance2.get_bits()

    return (
        IndividualAdapter.from_bits(m1[:p1] + m2[p1:p2] + m1[p2:], dataset=instance1.dataset),
        IndividualAdapter.from_bits(m2[:p1] + m1[p1:p2] + m2[p2:], dataset=instance1.dataset)
    )