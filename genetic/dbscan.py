'Functions for calcuate a dbscan and the perfomance'
from concurrent.futures import Future
from fractions import Fraction

from sklearn.cluster import DBSCAN
from sklearn import metrics
import pandas as pd
import numpy as np

def normalize(min_, max_, value):
    return max(min_, min(max_, (value - min_) / (max_ - min_)))


def compute_perfomance(dataset: str, min_samples: int, epsilon: float) -> float:
    df = pd.read_csv(dataset) 
    points = df.values.tolist()
    clustering = DBSCAN(eps=epsilon, min_samples=min_samples).fit(points)
    X = points
    labels = clustering.labels_
    n_labels = len(np.unique(labels))

    return (
        Fraction('2/5') * normalize(-1, 1, metrics.silhouette_score(X, labels)) # Best value 1
        + Fraction('2/5') * normalize(0, 1, 1 - metrics.davies_bouldin_score(X, labels)) # Best value 0 
        + Fraction('1/5') * 1 if n_labels > 3 else 0
    )


