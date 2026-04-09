from shapely.geometry import Polygon as ShapePoly
from geometry import Polygon, Point
from shor_network import shor_min_hausdorff_network
from typing import List, Tuple, Optional


def total_hausdorff(convex_poly: Polygon, non_convex_poly: Polygon) -> float:
    
    convex_shape_poly = ShapePoly([(p.x, p.y) for p in convex_poly.vertices])
    non_convex_shape_poly = ShapePoly([(p.x, p.y) for p in non_convex_poly.vertices])
    return convex_shape_poly.hausdorff_distance(non_convex_shape_poly)

def total_hausdorff_with_network(
    convex_poly: Polygon,
    centers: List[Point],
    initial_shift: Tuple[float, float] = (0.0, 0.0),
    step_size: Optional[float] = None,
    max_iter: int = 500,
    accuracy: float = 1e-3
) -> float:
    
    if step_size is None:
        min_x, max_x, min_y, max_y = convex_poly.compute_bounging_box()
        diag = ((max_x - min_x)**2 + (max_y - min_y)**2)**0.5
        step_size = diag * 0.5  

    _, min_dist = shor_min_hausdorff_network(
        convex_poly, centers, initial_shift, step_size,
        iter=max_iter, accuracy=accuracy
    )
    return min_dist