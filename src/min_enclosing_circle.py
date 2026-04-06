from typing import Tuple, List
from geometry import Point



def get_circle_from_two(first_point: Point, second_point: Point) -> Tuple[Point, float]:
    center_point = (first_point + second_point) * 0.5
    radius = (first_point - center_point).norm()
    return center_point, radius


def get_circle_from_three(first_point: Point, second_point: Point, third_point: Point) -> Tuple[Point, float]:
    determinant = 2 * (
        first_point.x * (second_point.y - third_point.y) +
        second_point.x * (third_point.y - first_point.y) +
        third_point.x * (first_point.y - second_point.y)
    )

    if abs(determinant) < 1e-10:
        return None
    
    ux = (
        (first_point.x**2 + first_point.y**2) * (second_point.y - third_point.y) +
        (second_point.x**2 + second_point.y**2) * (third_point.y - first_point.y) +
        (third_point.x**2 + third_point.y**2) * (first_point.y - second_point.y)
    ) / determinant

    uy = (
        (first_point.x**2 + first_point.y**2) * (third_point.x - second_point.x) +
        (second_point.x**2 + second_point.y**2) * (first_point.x - third_point.x) +
        (third_point.x**2 + third_point.y**2) * (second_point.x - first_point.x)
    ) / determinant

    center = Point(ux, uy)
    radius = (center - first_point).norm()

    return center, radius


def is_covers_all(center: Point, radius: float, points: List[Point], eps=1e-9):
    for p in points:
        if (p - center).norm() > radius + eps:
            return False
    return True


def get_minimum_enclosing_circle(points: List[Point]) -> Tuple[Point, float]:
    n = len(points)

    if n == 0:
        return None, 0.0

    if n == 1:
        return points[0], 0.0

    best_center = None
    best_radius = float("inf")

    for i in range(n):
        for j in range(i + 1, n):
            center, radius = get_circle_from_two(points[i], points[j])

            if radius < best_radius and is_covers_all(center, radius, points):
                best_center = center
                best_radius = radius

    for i in range(n):
        for j in range(i + 1, n):
            for k in range(j + 1, n):
                circle = get_circle_from_three(points[i], points[j], points[k])
                if circle is None:
                    continue

                center, radius = circle

                if radius < best_radius and is_covers_all(center, radius, points):
                    best_center = center
                    best_radius = radius

    if best_center is None:
        max_dist = -float("inf")
        for i in range(n):
            for j in range(i + 1, n):
                d = points[i].dist(points[j])
                if d > max_dist:
                    max_dist = d
                    best_center = (points[i] + points[j]) * 0.5
        
        best_radius = max_dist * 0.5

    return best_center, best_radius


