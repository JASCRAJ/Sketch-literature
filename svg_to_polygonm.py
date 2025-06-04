from svgpath2mpl import parse_path
from shapely.geometry import Polygon
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon as MplPolygon
from matplotlib.patches import Rectangle
import numpy as np

# Sample SVG path data (replace with your actual SVG path)
#svg_path_data = "M 100 100 L 300 100 L 300 200 L 100 200 Z"
svg_path_data="M 551.5,419.5 C 552.404,420.209 552.737,421.209 552.5,422.5C 554.5,422.167 556.5,421.833 558.5,421.5C 550.241,427.128 542.574,433.461 535.5,440.5C 533.182,440.818 531.848,442.152 531.5,444.5C 532.858,446.503 534.191,448.503 535.5,450.5C 534.833,450.5 534.167,450.5 533.5,450.5C 531.799,449.789 530.799,448.455 530.5,446.5C 530.795,444.265 530.461,442.265 529.5,440.5C 531.244,438.25 533.244,436.083 535.5,434C 540.479,430.362 545.479,426.696 550.5,423C 551.337,421.989 551.67,420.822 551.5,419.5 Z"
#"M 531.5,493.5 C 532.338,493.842 532.672,494.508 532.5,495.5C 532.062,495.435 531.728,495.601 531.5,496C 532.692,498.572 533.692,501.239 534.5,504C 534.164,505.03 533.497,505.53 532.5,505.5C 530.611,504.396 528.945,503.063 527.5,501.5C 528.847,502.028 530.181,502.195 531.5,502C 528.329,499.659 525.329,497.159 522.5,494.5C 524.909,493.278 526.742,493.945 528,496.5C 529.518,495.837 530.685,494.837 531.5,493.5 Z"
#"M0 0 C0.66 0.99 1.32 1.98 2 3 C1.34 3.66 0.68 4.32 0 5 C-0.64 5.87 -1.28 6.73 -1.94 7.62 C-2.96 8.8 -2.96 8.8 -4 10 C-4.99 10 -5.98 10 -7 10 C-6.67 10.99 -6.34 11.98 -6 13 C-6.66 13 -7.32 13 -8 13 C-8 13.66 -8 14.32 -8 15 C-9.65 15 -11.3 15 -13 15 C-13.66 16.32 -14.32 17.64 -15 19 C-18.3 19 -21.6 19 -25 19 C-24.01 18.34 -23.02 17.68 -22 17 C-21.37 16.54 -20.74 16.07 -20.1 15.6 C-19.09 14.84 -19.09 14.84 -18.06 14.06 C-17.39 13.56 -16.72 13.05 -16.04 12.54 C-15.36 12.03 -14.69 11.52 -14 11 C-12.95 10.16 -12.95 10.16 -11.87 9.31 C-11.25 8.88 -10.64 8.44 -10 8 C-9.34 8 -8.68 8 -8 8 C-7.79 7.42 -7.59 6.85 -7.38 6.25 C-6.92 5.51 -6.47 4.76 -6 4 C-5.52 3.62 -5.03 3.24 -4.53 2.84 C-3.98 2.48 -3.44 2.12 -2.88 1.75 C-1.93 1.17 -0.98 0.6 0 0 Z " 

# # Step 1: Parse the SVG path
# mpl_path = parse_path(svg_path_data)

# # Step 2: Convert to list of polygons (as numpy arrays of shape (N, 2))
# polygons = mpl_path.to_polygons()

# # Assume the first polygon is what we want to process
# if not polygons:
#     raise ValueError("No polygons extracted from the SVG path.")

# polygon_np = polygons[0]  # numpy array of shape (N, 2)

# # Step 3: Create Shapely Polygon from numpy array
# shapely_polygon = Polygon(polygon_np)

# # Step 4: Compute the Minimum Rotated Rectangle
# rotated_rectangle = shapely_polygon.minimum_rotated_rectangle
# rotated_coords = np.array(rotated_rectangle.exterior.coords)

# # Step 5: Plotting original polygon and its minimum rotated rectangle
# fig, ax = plt.subplots()
# ax.set_aspect('equal')

# # Plot original polygon
# patch = MplPolygon(polygon_np, closed=True, facecolor='lightblue', edgecolor='blue', label="Original Polygon")
# ax.add_patch(patch)

# # Plot minimum rotated rectangle
# ax.plot(*rotated_coords.T, 'r--', lw=2, label="Min Rotated Rectangle")

# plt.legend()
# plt.title("SVG Polygon and Minimum Rotated Rectangle")
# plt.grid(True)
# plt.show()
# Step 1: Parse SVG path
mpl_path = parse_path(svg_path_data)

# Step 2: Convert to polygon(s)
polygons = mpl_path.to_polygons()
if not polygons:
    raise ValueError("No polygons extracted from the SVG path.")

polygon_np = polygons[0]

# Step 3: Create shapely polygon and get minimum rotated rectangle
shapely_polygon = Polygon(polygon_np)
min_rect = shapely_polygon.minimum_rotated_rectangle
min_rect_coords = np.array(min_rect.exterior.coords)

# --- Plotting ---
fig, axs = plt.subplots(1, 3, figsize=(5, 5))
titles = ['SVG Path Shape', 'Extracted Polygon', 'Polygon + Min Rotated Rect']

# Subplot 1: SVG rendered from path
axs[0].set_title(titles[0], fontsize=16, fontname='Times New Roman')
axs[0].plot(*polygon_np.T, color='black')
axs[0].fill(*polygon_np.T, facecolor='lightblue', edgecolor='black')
axs[0].set_aspect('equal')
axs[0].axis('off')

# Subplot 2: Shapely Polygon
axs[1].set_title(titles[1], fontsize=16, fontname='Times New Roman')
axs[1].add_patch(MplPolygon(polygon_np, closed=True, facecolor='None', edgecolor='black'))
axs[1].set_aspect('equal')
axs[1].autoscale()
#axs[1].grid(True)

# Subplot 3: SVG + Min Rotated Rectangle
axs[2].set_title(titles[2], fontsize=16, fontname='Times New Roman')
axs[2].add_patch(MplPolygon(polygon_np, closed=True, facecolor='lightblue', edgecolor='black'))
axs[2].plot(*min_rect_coords.T, 'k--', lw=2)
axs[2].set_aspect('equal')
axs[2].autoscale()
#axs[2].grid(True)
axs[1].axis('off')
axs[2].axis('off')

plt.tight_layout()
plt.show()