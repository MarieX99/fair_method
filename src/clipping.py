from shapely.geometry import Polygon as ShapePolygon, Point as ShapePoint, MultiPoint
from shapely.ops import voronoi_diagram
from typing import List
from geometry import Point, Polygon

def get_voronoi_cells_shapely(polygon: Polygon, centers: List[Point]) -> List[Polygon]:
    polygon_vertices = [(p.x, p.y) for p in polygon.vertices]
    polygon_shape = ShapePolygon(polygon_vertices)

    points_shape = [ShapePoint(c.x, c.y) for c in centers]
    points_multipoint = MultiPoint(points_shape)

    min_x, max_x, min_y, max_y = polygon_shape.bounds

    envelope = polygon_shape.buffer(max(max_x-min_x, max_y-min_y))
    voronoi_polys = voronoi_diagram(points_multipoint, envelope=envelope)
    
    cells = []

    for center_idx, center in enumerate(centers):
        target_pt = ShapePoint(center.x, center.y)
        
        for poly in voronoi_polys.geoms:
            if poly.distance(target_pt) < 1e-9:
                intersection = poly.intersection(polygon_shape)

                if intersection.is_empty:
                    cells.append(Polygon([]))
                elif intersection.geom_type == 'Polygon':
                    new_vertices = [Point(x, y) for x, y in intersection.exterior.coords[:-1]]
                    cells.append(Polygon(new_vertices))
                elif intersection.geom_type == 'MultiPolygon':
                    all_pts = []
                    for sub_poly in intersection.geoms:
                        for x, y in sub_poly.exterior.coords[:-1]:
                            all_pts.append(Point(x, y))
                    cells.append(Polygon(all_pts))
                break
                
    return cells