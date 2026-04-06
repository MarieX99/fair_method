from shapely.geometry import Polygon as ShapePoly
from geometry import Polygon


def total_hausdorff(convex_poly: Polygon, non_convex_poly: Polygon) -> float:
    convex_shape_poly = ShapePoly([(p.x, p.y) for p in non_convex_poly.vertices])
    non_convex_shape_poly = ShapePoly([(p.x, p.y) for p in convex_poly.vertices])

    return convex_shape_poly.hausdorff_distance(non_convex_shape_poly)