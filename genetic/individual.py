'definition of the individual class'
from dataclasses import dataclass


@dataclass
class Individual:
    epsilon: float
    min_samples: int

    def __repr__(self):
        return (
            'Individual('
            f'epsilon={self.epsilon},'
            f'min_samples={self.min_samples}'
            ')'
        )
