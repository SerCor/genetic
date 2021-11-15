'''Adapter for the individual object. The adapter support the binary representation of the the properties of the original individual object'''
from typing import Optional
import random


from .convert import (
    bits2float, bits2int,
    float2bits, int2bits
)
from .dbscan import compute_perfomance
from .settings import (
    N_BITS_EPSILON, N_BITS_MIN_SAMPLES,
    RANGE_EPSILON,
)
from .individual import Individual


class IndividualAdapter:
    def __init__(self, instance: Individual, dataset, score=None):
        self.instance = instance
        self.dataset = dataset
        self._score: Optional[float] = score

    @classmethod
    def from_bits(cls, bits: str, dataset, score=None) -> 'IndividualAdapter':
        len_input_bits = len(bits)
        expected_len = N_BITS_EPSILON + N_BITS_MIN_SAMPLES
        if len_input_bits != expected_len:
            raise ValueError(f'the assgiend bits must to be of length {expected_len} but is {len_input_bits}')

        epsilon_bits, min_samples_bits = bits[:N_BITS_EPSILON], bits[N_BITS_EPSILON:]

        return cls(
                instance=Individual(
                    epsilon=bits2float(epsilon_bits, *RANGE_EPSILON),
                    min_samples=bits2int(min_samples_bits, 1),
                ),
                score=score,
                dataset=dataset
            )
    
    @classmethod
    def random(cls, dataset) -> 'IndividualAdapter':
        low_epsilon, high_epsilon = RANGE_EPSILON

        return cls(
            instance=Individual(
                epsilon=random.uniform(low_epsilon, high_epsilon),
                min_samples=random.randint(1, 2 ** N_BITS_MIN_SAMPLES)
            ),
            dataset=dataset
        )

    @property
    def epsilon(self) -> str:
        low, high = RANGE_EPSILON
        return float2bits(self.instance.epsilon, low=low, high=high, n_bits=N_BITS_EPSILON)

    @epsilon.setter
    def epsilon(self, epsilon: str) -> None:
        low, high = RANGE_EPSILON
        self.instance.epsilon = bits2float(epsilon, low, high)

    @property
    def min_samples(self) -> str:
        return int2bits(self.instance.min_samples, 1, N_BITS_MIN_SAMPLES)

    @min_samples.setter
    def min_samples(self, min_samples: str) -> None:
        self.instance.min_samples = bits2int(min_samples, 1)

    @property
    def score(self):
        if self._score is None:
            self._score = compute_perfomance(dataset=self.dataset, min_samples=self.instance.min_samples,
                                epsilon=self.instance.epsilon)

        return self._score

    def set_bits(self, bits: str) -> None:
        len_input_bits = len(bits)
        expected_len = N_BITS_EPSILON + N_BITS_MIN_SAMPLES
        if len_input_bits != expected_len:
            raise ValueError(f'the assgiend bits must to be of length {expected_len} but is {len_input_bits}')
        
        epsilon_bits, min_samples_bits = bits[:N_BITS_EPSILON], bits[N_BITS_EPSILON:]
        self.epsilon = epsilon_bits
        self.min_samples = min_samples_bits

    def get_bits(self) -> str:
        return self._instance_to_bits()

    def _instance_to_bits(self) -> str:
        return self.epsilon + self.min_samples

    def __getitem__(self, index) -> str:
        return self._instance_to_bits()[index]

    def __iter__(self):
        return  iter(self._instance_to_bits())
    
    def __len__(self) -> int:
        return len(self._instance_to_bits())

    def __lt__(self, other: 'IndividualAdapter') -> bool:
        s1 = self._score or 0 # Dont force to evaluate
        s2 = other._score or 0 # Dont force to evaluate

        return s1 < s2
    
    def __hash__(self) -> int:
        return hash(self.epsilon + self.min_samples)

    def __eq__(self, other) -> bool:
        if not isinstance(other, IndividualAdapter):
            return False

        return (self.epsilon, self.min_samples) == (other.epsilon, other.min_samples)

    def __repr__(self) -> str:
        return (
            'IndividualAdapter('
            f'instance={self.instance!r},'
            f'score={self._score!r},'
            f'dataset={self.dataset!r}'
            ')'
        )
