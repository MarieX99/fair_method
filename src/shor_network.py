import numpy as np
from typing import List, Tuple
from shapely.geometry import Polygon as ShapelyPolygon, Point as ShapelyPoint
from shapely.ops import nearest_points
from geometry import Point, Polygon

def to_shapely(poly: Polygon) ->ShapelyPolygon:
    vertices = [(p.x, p.y) for p in poly.vertices]
    return ShapelyPolygon(vertices)

def f_and_subgradient_network(
    A_shapely: ShapelyPolygon,
    centers: List[Point],
    shift: np.ndarray,
    eps: float = 1e-12
) -> Tuple[float, np.ndarray]:
    
    dx, dy = shift
    
    shifted_centers = [(c.x+dx, c.y+dy) for c in centers]

    max_val = 0.0
    best_h = np.zeros(2)

    for a_coord in A_shapely.exterior.coords[:-1]:
        
        min_dist_sq = float('inf')
        nearest_center = None
        
        for cx, cy in shifted_centers:
            d2 = (a_coord[0] - cx)**2 + (a_coord[1] - cy)**2
            if d2 < min_dist_sq:
                min_dist_sq = d2
                nearest_center = (cx, cy)
        dist = np.sqrt(min_dist_sq)
        if dist > max_val - eps:
            max_val = dist
            if dist > eps:
                vector = np.array([nearest_center[0] - a_coord[0],
                                   nearest_center[1] - a_coord[1]])
                best_h = vector / dist

    for cx, cy in shifted_centers:
        p = ShapelyPoint(cx, cy)
        dist = p.distance(A_shapely)
        if dist > max_val - eps:
            max_val = dist
            if dist > eps:
                nearest = nearest_points(p, A_shapely)[1]
                vector = np.array([p.x - nearest.x, p.y - nearest.y])
                best_h = vector / dist

    return max_val, best_h

def shor_min_hausdorff_network(
    A: Polygon,
    centers: List[Point],
    x0: Tuple[float, float],
    y0: float,
    iter: int = 500,
    accuracy: float = 1e-3,
) -> Tuple[Tuple[float, float], float]:
    
    A_shapely = to_shapely(A)

    x = np.array(x0, dtype=float)
    best_x = x.copy()
    best_f = f_and_subgradient_network(A_shapely, centers, x)[0]

    for i in range(iter):
        f_val, h= f_and_subgradient_network(A_shapely, centers, x)
        if f_val < best_f - accuracy:
            best_f = f_val
            best_x = x.copy()

        if f_val < accuracy:
            print(f"Итерация {i}: f={f_val:.6f} ниже точности")         
            break
        norm_h = np.linalg.norm(h)
        
        if norm_h < 1e-12:
            print(f"Итерация {i}: субградиент близок к нулю")
            break
        
        y = y0 / (i + 1)

        
        x = x - y * h

        if i % 50 == 0:
            print(f"Итерация {i}: f={f_val:.6f}, shift=({x[0]:.2f}, {x[1]:.2f})")

    return (float(best_x[0]), float(best_x[1])), best_f