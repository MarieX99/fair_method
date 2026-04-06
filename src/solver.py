from typing import List
from geometry import Point, Polygon
from clipping import get_voronoi_cells_shapely
from min_enclosing_circle import get_minimum_enclosing_circle
from hausdorff_discrete import hausdorff_with_witness


def update_centers(cells: List[Polygon], old_centers: List[Point]) -> List[Point]:
    new_centers = []

    for i, cell in enumerate(cells):
        if not cell.vertices:
            new_centers.append(old_centers[i])
            continue

        center, _ = get_minimum_enclosing_circle(cell.vertices)
        new_centers.append(center)

    return new_centers


def make_one_iteration(polygon: Polygon, centers: List[Point]) -> List[Point]:
    cells = get_voronoi_cells_shapely(polygon, centers)
    new_centers = update_centers(cells, centers)
    return new_centers


def solve(
        polygon: Polygon,
        centers: List[Point],
        max_iter: int = 50,
        eps: float = 1e-3
) -> List[Point]:
    prev_dist = float("inf")

    for i in range(max_iter):
        new_centers = make_one_iteration(polygon, centers)

        hausdorff_dist, _ = hausdorff_with_witness(polygon, new_centers)

        if abs(prev_dist - hausdorff_dist) <= eps:
            print("Converged")
            break 
        
        centers = new_centers
        prev_dist = hausdorff_dist

    return centers