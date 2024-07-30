from shapely.geometry import Polygon
from shapely.ops import unary_union
import math
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon as MplPolygon

def create_rectangle_from_line(line):
    """Create a rectangle polygon from a line segment with thickness."""
    (x1, y1), (x2, y2), thickness = line['start'], line['end'], line['thickness']
    half_thickness = thickness / 2.0
    
    if x1 == x2:  # Vertical line
        return Polygon([
            (x1 - half_thickness, y1), 
            (x1 + half_thickness, y1), 
            (x1 + half_thickness, y2), 
            (x1 - half_thickness, y2)
        ])
    elif y1 == y2:  # Horizontal line
        return Polygon([
            (x1, y1 - half_thickness), 
            (x2, y1 - half_thickness), 
            (x2, y1 + half_thickness), 
            (x1, y1 + half_thickness)
        ])
    else:  # Diagonal line
        angle = math.atan2(y2 - y1, x2 - x1)
        dx = half_thickness * math.sin(angle)
        dy = half_thickness * math.cos(angle)
        return Polygon([
            (x1 - dx, y1 + dy), 
            (x1 + dx, y1 - dy),
            (x2 + dx, y2 - dy), 
            (x2 - dx, y2 + dy)
        ])

def find_enclosed_regions(lines):
    """Find regions enclosed by the given lines and return only the holes."""
    # Create rectangles for each line segment
    rectangles = [create_rectangle_from_line(line) for line in lines]
    
    # Merge all rectangles into a single polygon or multipolygon
    merged_polygon = unary_union(rectangles)
    
    # Extract holes (interiors) from the merged polygon
    holes = []
    if merged_polygon.geom_type == 'Polygon':
        for interior in merged_polygon.interiors:
            holes.append({
                'exterior': list(interior.coords),
                'interior': []
            })
    elif merged_polygon.geom_type == 'MultiPolygon':
        for polygon in merged_polygon:
            for interior in polygon.interiors:
                holes.append({
                    'exterior': list(interior.coords),
                    'interior': []
                })
    
    return holes

def plot_polygons(polygons):
    """Plot the polygons and annotate their coordinates."""
    fig, ax = plt.subplots()

    for polygon in polygons:
        # Plot the exterior of the hole
        exterior_coords = polygon['exterior']
        exterior_polygon = MplPolygon(exterior_coords, closed=True, edgecolor='red', facecolor='none')
        ax.add_patch(exterior_polygon)
        
        # Annotate exterior coordinates
        for (x, y) in exterior_coords:
            ax.text(x, y, f'({x}, {y})', fontsize=8, ha='right')

        # Plot the interiors (if any)
        for interior_coords in polygon['interior']:
            interior_polygon = MplPolygon(interior_coords, closed=True, edgecolor='blue', facecolor='none')
            ax.add_patch(interior_polygon)
            
            # Annotate interior coordinates
            for (x, y) in interior_coords:
                ax.text(x, y, f'({x}, {y})', fontsize=8, ha='right')

    # Set the plot limits
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.set_aspect('equal')
    plt.show()

# Test the function with the given input
input_lines = [
    {"start": [1, 0], "end": [1, 7], "thickness": 2},
    {"start": [2, 6], "end": [6, 6], "thickness": 2},
    {"start": [7, 7], "end": [7, 0], "thickness": 2},
    {"start": [6, 1], "end": [2, 1], "thickness": 2},
    {"start": [4, 3], "end": [4, 4], "thickness": 1},
]

holes_output = find_enclosed_regions(input_lines)
print("Holes Output:", holes_output)

# Plot the output
plot_polygons(holes_output)
