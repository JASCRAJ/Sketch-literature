from svgpath2mpl import parse_path
from shapely.geometry import Polygon, box
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon as MplPolygon
from matplotlib.patches import Rectangle
import numpy as np

# Sample SVG path data (replace with your actual SVG path)
#svg_path_data = "M 100 100 L 300 100 L 300 200 L 100 200 Z"
svg_path_data="M 206.5,121.5 C 207.347,122.966 208.68,123.8 210.5,124C 210.043,124.414 209.709,124.914 209.5,125.5C 210.667,125.833 211.833,126.167 213,126.5C 218.068,125.491 222.734,125.824 227,127.5C 228.716,127.252 230.216,126.585 231.5,125.5C 234.198,126.824 236.864,126.824 239.5,125.5C 239.657,126.873 239.49,128.207 239,129.5C 236.197,131.302 234.031,133.635 232.5,136.5C 231.821,133.805 230.487,131.139 228.5,128.5C 225.728,128.595 223.728,129.929 222.5,132.5C 224.182,136.111 226.848,137.278 230.5,136C 229.495,137.507 228.162,138.673 226.5,139.5C 226.968,141.134 227.968,142.3 229.5,143C 227.527,143.495 225.527,143.662 223.5,143.5C 223.5,144.5 223.5,145.5 223.5,146.5C 223.167,146.5 222.833,146.5 222.5,146.5C 217.987,146.588 213.987,148.088 210.5,151C 205.643,152.92 200.643,154.586 195.5,156C 192.393,158.699 188.727,160.033 184.5,160C 181.761,160.798 179.761,162.465 178.5,165C 173.534,166.402 168.868,168.402 164.5,171C 165.252,171.671 165.586,172.504 165.5,173.5C 161.492,173.15 157.492,172.817 153.5,172.5C 153.56,176.485 151.56,178.152 147.5,177.5C 145.776,179.914 144.442,182.58 143.5,185.5C 140.858,185.488 139.525,186.821 139.5,189.5C 139.5,190.167 139.167,190.5 138.5,190.5C 137.761,190.631 137.094,190.464 136.5,190C 138.975,188.257 138.975,187.257 136.5,187C 135.594,188.699 135.261,190.533 135.5,192.5C 134.022,192.238 132.689,192.571 131.5,193.5C 132.025,194.192 132.692,194.692 133.5,195C 130.74,195.674 128.073,196.507 125.5,197.5C 125.5,198.5 125.5,199.5 125.5,200.5C 124.5,200.5 123.5,200.5 122.5,200.5C 122.741,203.999 121.908,204.332 120,201.5C 117.233,203.599 115.233,206.266 114,209.5C 113.667,208.833 113.333,208.167 113,207.5C 112.918,210.748 111.418,213.081 108.5,214.5C 107.25,218.746 106.417,223.079 106,227.5C 104.926,228.618 103.76,229.618 102.5,230.5C 103.523,232.895 102.523,233.895 99.5,233.5C 99.5,234.5 99.5,235.5 99.5,236.5C 100.959,236.433 102.292,236.766 103.5,237.5C 102.368,243.16 100.368,248.494 97.5,253.5C 95.9328,252.319 95.0995,250.653 95,248.5C 94.6892,250.556 94.1892,252.556 93.5,254.5C 92.8333,255.833 92.1667,255.833 91.5,254.5C 92.8333,252.5 92.8333,250.5 91.5,248.5C 92.09,247.201 93.09,246.368 94.5,246C 92.6583,244.654 91.6583,242.821 91.5,240.5C 91.6107,239.883 91.944,239.383 92.5,239C 90.5624,236.102 89.8958,233.102 90.5,230C 91.0293,225.15 91.6959,220.317 92.5,215.5C 93.3081,215.192 93.9747,214.692 94.5,214C 93.1667,213 91.8333,212 90.5,211C 91.8333,210 93.1667,209 94.5,208C 92.6199,208.51 90.7866,208.343 89,207.5C 87.4804,210.488 87.3137,213.488 88.5,216.5C 84.4072,215.059 83.4072,216.559 85.5,221C 84.1153,222.597 83.4486,224.43 83.5,226.5C 82.6236,226.631 81.9569,226.298 81.5,225.5C 82.8333,224.167 82.8333,222.833 81.5,221.5C 81.8076,220.692 82.3076,220.025 83,219.5C 83.292,214.082 84.1253,208.748 85.5,203.5C 83.8761,199.332 84.2094,195.332 86.5,191.5C 88.6716,191.676 91.0049,191.843 93.5,192C 92.3279,192.419 91.3279,193.085 90.5,194C 90.6932,195.645 90.8598,197.479 91,199.5C 92,197.5 93,195.5 94,193.5C 94.4828,194.448 94.6495,195.448 94.5,196.5C 98.1106,196.044 101.444,196.711 104.5,198.5C 104.833,198 105.167,197.5 105.5,197C 103.495,193.319 103.495,189.819 105.5,186.5C 106.051,188.413 106.218,190.413 106,192.5C 106.98,190.941 107.813,189.274 108.5,187.5C 109.731,188.651 109.731,189.817 108.5,191C 110.927,193.252 111.927,196.086 111.5,199.5C 113.876,197.841 116.543,196.507 119.5,195.5C 119.833,194.833 120.167,194.167 120.5,193.5C 117.726,190.301 118.226,187.634 122,185.5C 123.396,187.527 125.062,187.86 127,186.5C 127.202,188.256 127.702,189.922 128.5,191.5C 130.374,190.065 132.374,188.898 134.5,188C 133.552,187.517 132.552,187.351 131.5,187.5C 131.286,185.856 131.62,184.356 132.5,183C 130.941,182.02 129.274,181.187 127.5,180.5C 130.095,179.976 132.761,179.976 135.5,180.5C 135.351,179.448 135.517,178.448 136,177.5C 136.333,177.833 136.667,178.167 137,178.5C 138.067,177.809 139.234,177.309 140.5,177C 136.178,177.071 131.845,176.238 127.5,174.5C 130.149,174.92 132.816,174.42 135.5,173C 133.097,171.273 130.597,171.106 128,172.5C 126.278,172.389 126.112,171.889 127.5,171C 133.892,171.531 139.392,169.698 144,165.5C 145.571,165.25 147.071,165.917 148.5,167.5C 150.764,167.096 152.93,167.096 155,167.5C 157.654,166.428 159.821,164.761 161.5,162.5C 160.408,160.817 159.741,158.984 159.5,157C 159.534,153.835 160.867,153.002 163.5,154.5C 159.597,156.283 159.93,157.45 164.5,158C 163.707,159.085 163.04,160.252 162.5,161.5C 164.078,162.072 165.578,162.406 167,162.5C 169.704,160.35 169.871,158.184 167.5,156C 169.598,156.984 171.598,156.651 173.5,155C 174.926,152.156 176.426,149.322 178,146.5C 178.483,147.448 178.649,148.448 178.5,149.5C 180.5,149.5 182.5,149.5 184.5,149.5C 184.617,147.516 183.95,145.85 182.5,144.5C 185.785,143.676 189.118,143.176 192.5,143C 193.815,141.605 193.481,140.605 191.5,140C 193.5,139.333 195.5,138.667 197.5,138C 198.38,136.644 198.714,135.144 198.5,133.5C 201.448,133.777 204.281,133.444 207,132.5C 206.503,130.802 206.67,129.135 207.5,127.5C 206.833,125.833 206.167,124.167 205.5,122.5C 205.624,121.893 205.957,121.56 206.5,121.5 Z"
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

def grid_based_decomposition(vertices, grid_size):
    polygon = Polygon(vertices)
    min_x, min_y, max_x, max_y = polygon.bounds
    cells = []
    x = min_x
    while x < max_x:
        y = min_y
        while y < max_y:
            cell = box(x, y, x + grid_size, y + grid_size)
            if polygon.intersects(cell):
                cells.append(cell)
            y += grid_size
        x += grid_size
    return cells

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
# Step 4: Apply grid decomposition
grid_cells = grid_based_decomposition(polygon_np, grid_size=2)
from shapely.ops import unary_union
import matplotlib.cm as cm
def construct_sequencing(polygon_vertices, grid_cells, strategy="proximity"):
    polygon = Polygon(polygon_vertices)
    if strategy == "proximity":
        centroid = polygon.centroid
        sequencing = sorted(grid_cells, key=lambda cell: cell.centroid.distance(centroid))
    elif strategy == "row-wise":
        sequencing = sorted(grid_cells, key=lambda cell: (cell.bounds[1], cell.bounds[0]))
    elif strategy == "column-wise":
        sequencing = sorted(grid_cells, key=lambda cell: (cell.bounds[0], cell.bounds[1]))
    else:
        raise ValueError("Unsupported strategy: Choose 'proximity' or 'row-wise'")
    return sequencing

def split_into_groups(grid_cells, num_groups):
    group_size = len(grid_cells) // num_groups
    groups = [grid_cells[i:i + group_size] for i in range(0, len(grid_cells), group_size)]
    if len(groups) > num_groups:
        groups[-2].extend(groups[-1])
        groups = groups[:-1]
    return groups

# Step 5: Construct sequencing and split into groups
sequenced_cells = construct_sequencing(polygon_np, grid_cells, strategy="row-wise")
groups = split_into_groups(sequenced_cells, num_groups=3)

# --- Extend plot with 5 subplots now ---
fig, axs = plt.subplots(1, 5, figsize=(25, 5))
titles = ['SVG Path Shape', 'Extracted Polygon', 'Polygon + Min Rotated Rect', 'Grid Decomposition', 'Grouped Grids + MinRects']


# # --- Plotting with Grid Decomposition ---
# fig, axs = plt.subplots(1, 4, figsize=(20, 5))
# titles = ['SVG Path Shape', 'Extracted Polygon', 'Polygon + Min Rotated Rect', 'Grid Decomposition']

# Subplot 1: SVG rendered from path
axs[0].set_title(titles[0], fontsize=16, fontname='Times New Roman')
axs[0].plot(*polygon_np.T, color='black')
axs[0].fill(*polygon_np.T, facecolor='lightblue', edgecolor='black')
axs[0].set_aspect('equal')
axs[0].axis('off')

axs[0].plot(*polygon_np.T, color='black')
axs[0].fill(*polygon_np.T, facecolor='lightblue', edgecolor='black')
axs[0].set_aspect('equal')
# axs[0].set_xticks([])
# axs[0].set_yticks([])
axs[0].autoscale()
axs[0].axis('off')

# Subplot 2: Shapely Polygon
axs[1].set_title(titles[1], fontsize=16, fontname='Times New Roman')
axs[1].add_patch(MplPolygon(polygon_np, closed=True, facecolor='None', edgecolor='black'))
axs[1].set_aspect('equal')
axs[1].autoscale()


# Subplot 3: SVG + Min Rotated Rectangle
axs[2].set_title(titles[2], fontsize=16, fontname='Times New Roman')
axs[2].add_patch(MplPolygon(polygon_np, closed=True, facecolor='lightblue', edgecolor='black'))
axs[2].plot(*min_rect_coords.T, 'k--', lw=2)
axs[2].set_aspect('equal')
axs[2].autoscale()

# Subplot 4: Grid Decomposition
axs[3].set_title(titles[3], fontsize=16, fontname='Times New Roman')
axs[3].add_patch(MplPolygon(polygon_np, closed=True, facecolor='lightblue', edgecolor='black'))
for cell in grid_cells:
    xs, ys = cell.exterior.xy
    axs[3].plot(xs, ys, color='grey', linewidth=0.7)
axs[3].set_aspect('equal')
axs[3].autoscale()
# axs[3].set_aspect('equal')
# axs[3].axis('off')
# Subplot 5: Grouped cells with min rotated rectangles
axs[4].set_title(titles[4], fontsize=16, fontname='Times New Roman')
axs[4].add_patch(MplPolygon(polygon_np, closed=True, facecolor='lightblue', edgecolor='black'))

# axs[1].set_xticks([])
# axs[1].set_yticks([])
# axs[2].set_xticks([])
# axs[2].set_yticks([])
# axs[3].set_xticks([])
# axs[3].set_yticks([])
# axs[4].set_xticks([])
# axs[4].set_yticks([])
axs[1].axis('off')
axs[2].axis('off')
axs[3].axis('off')
axs[4].axis('off')

colors = cm.get_cmap('Set1', len(groups))

for i, group in enumerate(groups):
    color = colors(i)
    for cell in group:
        xs, ys = cell.exterior.xy
        axs[4].plot(xs, ys, color=color, linewidth=0.8)

    # Combine group into single geometry and get min rotated rectangle
    unioned = unary_union(group)
    if unioned.geom_type == 'Polygon':
        group_minrect = unioned.minimum_rotated_rectangle
        xs, ys = group_minrect.exterior.xy
        axs[4].plot(xs, ys, color=color, linestyle='--', linewidth=2)
    elif unioned.geom_type == 'MultiPolygon':
        for part in unioned.geoms:
            rect = part.minimum_rotated_rectangle
            xs, ys = rect.exterior.xy
            axs[4].plot(xs, ys, color=color, linestyle='--', linewidth=2)

axs[4].set_aspect('equal')
axs[4].autoscale()

plt.tight_layout()
plt.show()