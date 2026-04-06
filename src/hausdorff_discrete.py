import heapq
import itertools
from typing import List, Tuple
from geometry import (
    Point, Polygon, 
    EdgeSample, Interval,
    point_to_centers_distance
    )


def normalize_sample(sample: EdgeSample, size: int, eps: float = 1e-10) -> EdgeSample:
    if abs(sample.edge_position - 1.0) < eps:
        return EdgeSample((sample.edge_idx + 1) % size, 0.0)
    return sample


def generate_samples(polygon: Polygon, total_samples: int = 50) -> List[EdgeSample]:
    edges = list(polygon.edges())
    lengths = [(b - a).norm() for a, b in edges] 
    total_length = sum(lengths)

    samples = []

    for i in range(total_samples):
        target = i / total_samples * total_length
        accumulator  = 0.0
        for edge_idx, length in enumerate(lengths):
            if accumulator  + length >= target:
                t = (target - accumulator ) / length
                edge_sample = EdgeSample(edge_idx, t)
                samples.append(edge_sample)
                break
            accumulator  += length

    return samples


def hausdorff_per_edge(
    polygon: Polygon,
    edge_idx: int,
    centers: List[Point],
    eps: float = 1e-3
) -> Tuple[float, EdgeSample]:
    a, b = polygon.get_edge(edge_idx)
    L = (b - a).norm()

    t0, t1 = 0.0, 1.0
    f0 = point_to_centers_distance(polygon, edge_idx, t0, centers)
    f1 = point_to_centers_distance(polygon, edge_idx, t1, centers)

    interval_queue = []
    counter = itertools.count()

    max_dist = -float("inf")
    worst_point = None

    if f1 > f0:
        max_dist = f1
        worst_point = EdgeSample(edge_idx, t1)
    else:
        max_dist = f0
        worst_point = EdgeSample(edge_idx, t0)

    interval = Interval(edge_idx, t0, t1, f0, f1, L)
    heapq.heappush(interval_queue, (-interval.upper_bound, next(counter), interval))

    samples = [
        EdgeSample(edge_idx, t0),
        EdgeSample(edge_idx, t1),
    ]

    while interval_queue:
        _, _, interval = heapq.heappop(interval_queue)

        if interval.upper_bound <= max_dist + eps:
            continue
        
        if interval.upper_bound - max_dist < eps:
            continue

        if interval.t2 - interval.t1 < eps:
            continue

        mid = 0.5 * (interval.t1 + interval.t2)
 
        function_value  = point_to_centers_distance(polygon, edge_idx, mid, centers)

        samples.append(EdgeSample(edge_idx, mid))

        if function_value > max_dist:
            max_dist = function_value
            worst_point = EdgeSample(edge_idx, mid)

        left_interval = Interval(edge_idx, interval.t1, mid, interval.f1, function_value, L)
        right_interval = Interval(edge_idx, mid, interval.t2, function_value, interval.f2, L)
        
        heapq.heappush(interval_queue, (-left_interval.upper_bound, next(counter), left_interval))
        heapq.heappush(interval_queue, (-right_interval.upper_bound, next(counter), right_interval))

    return max_dist, worst_point


def hausdorff_with_witness(
    polygon: Polygon,  
    centers: List[Point] 
) -> Tuple[float, EdgeSample]:
    
    if not centers:
        raise ValueError("centers must not be empty")

    edges_amount = polygon.get_amount_vertices()

    max_dist = -float("inf")
    worst_point = None

    for idx in range(edges_amount):
        local_hausdorff, local_worst_point = hausdorff_per_edge(polygon, idx, centers)

        if local_hausdorff > max_dist:
            max_dist = local_hausdorff
            worst_point = local_worst_point

    return max_dist, worst_point
