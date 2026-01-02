#!/usr/bin/env python
# License: GPL v3 Copyright: 2026, Mateusz Jamróz
# pd/core/statistics.py

"""
Docstring for pd.core.statistics
All magic happens here.
"""

from statistics import mean, median
from collections import Counter
from itertools import combinations
from dataclasses import dataclass

from pd.core.repositories import PDRecord

@dataclass
class PDStats:
    avg_lower: float
    avg_upper: float
    avg_spring: float
    avg_total: float
    median_lower: float
    median_upper: float
    common_config: tuple[float, float, float] | None # lower, upper, spring

def compute_stats(records: list[PDRecord]) -> PDStats | None:
    if not records:
        return None

    lowers = [r.washer1 for r in records]
    uppers = [r.washer2 for r in records]
    springs = [r.spring for r in records]
    totals = [r.washer1 + r.washer2 + r.spring for r in records]

    common = most_common_config(records)

    return PDStats(
        avg_lower=mean(lowers),
        avg_upper=mean(uppers),
        avg_spring=mean(springs),
        avg_total=mean(totals),
        median_lower=median(lowers),
        median_upper=median(uppers),
        common_config=common
    )

def most_common_config(
    records: list[PDRecord],
    tolerance: float = 0.03,
    min_count: int = 5,
    ):
    sums = [(r, r.washer1 + r.washer2 + r.spring) for r in records]

    clusters = []

    for rec, total in sums:
        placed = False
        for cluster in clusters:
            if abs(cluster[0][1] - total) <= tolerance:
                cluster.append((rec, total))
                placed = True
                break
        if not placed:
            clusters.append([(rec, total)])

    valid = [c for c in clusters if len(c) >= min_count]
    if not valid:
        return None
    
    # Find the largest cluster
    largest = max(valid, key=len)
    r = largest[0][0]  # Take the first record in the largest cluster

    return (r.washer1, r.washer2, r.spring)

