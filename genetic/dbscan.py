'Functions for calcuate a dbscan and the perfomance'
from concurrent.futures import Future
from fractions import Fraction

from sklearn.cluster import DBSCAN
from sklearn import metrics
import pandas as pd


def normalize(min_, max_, value):
    return min(max_, (value - min_) / (max_ - min_))


def compute_perfomance(min_samples: int, epsilon: float) -> float:
    df = pd.read_csv('dataset.csv') 
    points = df.values.tolist()
    clustering = DBSCAN(eps=epsilon, min_samples=min_samples).fit(points)

    X = points
    labels = clustering.labels_

    return (
        Fraction('1/3') * normalize(-1, 1, metrics.silhouette_score(X, labels)) # Best value 1
        + Fraction('1/3') * normalize(0, 1, metrics.calinski_harabasz_score(X, labels)) # 
        + Fraction('1/3') * normalize(0, 1, 1 - metrics.davies_bouldin_score(X, labels)) # Best value 0 
    )


