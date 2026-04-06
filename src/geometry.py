import math
from typing import List, Tuple
from dataclasses import dataclass


class Point:
    def __init__(self, x: float = 0.0, y: float = 0.0):
        self.x = x
        self.y = y

    def copy(self) -> 'Point':          
        return Point(self.x, self.y)

    def __eq__(self, other) -> bool:
        if not isinstance(other, Point):
            return False
        
        eps = 1e-10
        return (abs(self.x - other.x) < eps and
                abs(self.y - other.y) < eps)

    def __add__(self, other: 'Point') -> 'Point':
        return Point(self.x + other.x, self.y + other.y)
    
    def __sub__(self, other: 'Point') -> 'Point':
        return Point(self.x - other.x, self.y - other.y)
    
    def __mul__(self, scalar: float) -> 'Point':
        return Point(self.x * scalar, self.y * scalar)
    
    def __rmul__(self, scalar: float) -> 'Point':
        return self.__mul__(scalar)
    
    def dot(self, other: 'Point') -> float:
        return self.x * other.x + self.y * other.y
    
    def norm(self) -> float:
        return math.sqrt(self.x * self.x + self.y * self.y)
    
    def dist(self, other: "Point") -> float:
        return (self - other).norm()
    
    def __repr__(self) -> str:
        return f"Point({self.x}, {self.y})"
    

class Polygon:
    def __init__(self, vertices: List[Point]):
        self.vertices = vertices

    def get_amount_vertices(self):
        return len(self.vertices)

    def get_edge(self, idx):
        n = self.get_amount_vertices()
        return (
            self.vertices[idx],
            self.vertices[(idx + 1) % n]
        )

    def edges(self):
        n = len(self.vertices)
        for i in range(n):
            yield self.vertices[i], self.vertices[(i + 1) % n]

    def perimeter(self) -> float:
        return sum(a.dist(b) for a, b in self.edges())
    
    def compute_bounging_box(self) -> Tuple[float, float, float, float]:
        xs = [point.x for point in self.vertices]
        ys = [point.y for point in self.vertices]

        return min(xs), max(xs), min(ys), max(ys)


@dataclass
class EdgeSample:
    edge_idx: int
    edge_position: float #t (0=start, 1=end): p = a + t(b - a)


class Interval:
    def __init__(
        self, 
        edge_idx: int, 
        t1: float, 
        t2: float, 
        f1: float, 
        f2: float, 
        L: float
    ):  
        self.edge_idx = edge_idx
        self.t1 = t1
        self.t2 = t2
        self.f1 = f1
        self.f2 = f2
        self.L = L

        self.upper_bound = max(f1, f2) + 0.5 * L * (t2 - t1)


def get_point_on_segment(polygon: Polygon, sample: EdgeSample) -> Point:
    a, b = polygon.get_edge(sample.edge_idx)
    return a + sample.edge_position * (b - a)


def point_to_centers_distance(polygon: Polygon, edge_idx: int, t: float, centers: List[Point]) -> float:
    sample = EdgeSample(edge_idx, t)
    point = get_point_on_segment(polygon, sample)
    return min(point.dist(c) for c in centers)


