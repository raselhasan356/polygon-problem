from shapely.geometry import Polygon, box
from shapely.ops import unary_union

import matplotlib.pyplot as plt

# Define the main polygon (a simple rectangle in this case)
main_polygon = box(0, 0, 10, 10)

# Define rectangular holes
hole1 = box(2, 2, 4, 4)
hole2 = box(6, 6, 8, 8)

# Subtract holes from the main polygon
result_polygon = main_polygon.difference(unary_union([hole1, hole2]))

print(result_polygon)

# Plot the main polygon with holes
x, y = result_polygon.exterior.xy
plt.fill(x, y, color='blue', alpha=0.5)

for interior in result_polygon.interiors:
    x, y = interior.xy
    plt.fill(x, y, color='white', alpha=0.5)

plt.show()

