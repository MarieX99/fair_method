from geometry import Point, Polygon, get_point_on_segment
from hausdorff_discrete import generate_samples
from solver import solve
from hausdorff_poly import total_hausdorff_with_network
from typing import List


def init_centers(polygon: Polygon, k: int) -> List[Point]:
    samples = generate_samples(polygon, k)
    return [get_point_on_segment(polygon, s) for s in samples]


if __name__ == "__main__":
    convex_poly = Polygon([
        Point(8.5, 4.5), Point(9.5, 4.5), Point(9.5, 5.5), Point(8.5, 5.5)
    ])


    non_convex_poly = Polygon([
        Point(0, 0), Point(10, 0), Point(10, 10), Point(0, 10), 
        Point(0, 6),   
        Point(8, 6),   
        Point(8, 4),   
        Point(0, 4)       
    ])

    centers = init_centers(non_convex_poly, 16)

    centers = solve(non_convex_poly, centers)

    from hausdorff_poly import total_hausdorff_with_network
    min_distance = total_hausdorff_with_network(
        convex_poly, centers,
        initial_shift=(0.0, 0.0),   
        step_size=5.0,              
        max_iter=500,
        accuracy=1e-3
    )
    print(f"Минимальное хаусдорфово расстояние: {min_distance}")