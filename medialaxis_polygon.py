# import json
# import numpy as np
# import matplotlib.pyplot as plt
# from shapely.wkt import loads
# from shapely.affinity import translate
# from shapely.geometry import Polygon, LineString, MultiLineString
# from scipy.spatial import Voronoi
# from scipy.interpolate import CubicSpline

# def compute_medial_axis(polygon):
#     """
#     Compute the medial axis approximation using the Voronoi diagram.
#     """
#     boundary_points = np.array(polygon.exterior.coords)
#     vor = Voronoi(boundary_points)

#     medial_axis_points = []
#     for vpair in vor.ridge_vertices:
#         if -1 in vpair:
#             continue
#         p1, p2 = vor.vertices[vpair]
#         line = LineString([p1, p2])
#         if polygon.contains(line):
#             medial_axis_points.append(p1)
#             medial_axis_points.append(p2)

#     if len(medial_axis_points) < 4:  # Need at least 4 points for cubic spline
#         return None  

#     return np.array(medial_axis_points)

# def smooth_medial_axis(points, num_interp=100):
#     """
#     Smooth the medial axis using a cubic spline.
#     """
#     points = np.array(points)
#     t = np.linspace(0, 1, len(points))  # Parameterize points
#     spline_x = CubicSpline(t, points[:, 0])  # Fit cubic spline for x-coordinates
#     spline_y = CubicSpline(t, points[:, 1])  # Fit cubic spline for y-coordinates
    
#     t_fine = np.linspace(0, 1, num_interp)  # Smooth parameter space
#     x_smooth = spline_x(t_fine)
#     y_smooth = spline_y(t_fine)
    
#     return x_smooth, y_smooth

# def plot_nth_polygon_with_smooth_medial_axis(json_file, n):
#     with open(json_file, "r") as f:
#         data = json.load(f)

#     if n >= len(data):
#         print(f"Error: Only {len(data)} entries found. Requested index {n} is out of range.")
#         return

#     entry = data[n]
#     wkt_string = entry["wkt_string"]
#     transform = entry["transform"]

#     tx, ty = map(float, transform.replace("translate(", "").replace(")", "").split(","))
#     polygon = loads(wkt_string)
#     translated_polygon = translate(polygon, xoff=tx, yoff=ty)

#     medial_axis_points = compute_medial_axis(translated_polygon)
#     if medial_axis_points is None:
#         print("Medial axis computation failed (too few points).")
#         return

#     x_smooth, y_smooth = smooth_medial_axis(medial_axis_points)

#     fig, ax = plt.subplots(figsize=(6, 6))
#     x, y = translated_polygon.exterior.xy
#     ax.plot(x, y, 'b-', linewidth=2, label="Polygon Boundary")

#     ax.plot(x_smooth, y_smooth, 'r-', linewidth=3, label="Smooth Medial Axis")  # Smoothed curve

#     ax.set_aspect('equal')
#     plt.legend()
#     plt.show()

# # Example Usage
# file_name = "pavan"
# brush_name = "brush_7"
# INPUT_JSON_FILE = f"json/style/{file_name}-combined-dsequence-with_attributes.json"

# plot_nth_polygon_with_smooth_medial_axis(INPUT_JSON_FILE, 146)
import json
import numpy as np
import matplotlib.pyplot as plt
from shapely.wkt import loads
from shapely.affinity import translate
from shapely.geometry import Polygon, LineString, MultiLineString
from scipy.spatial import Voronoi
from scipy.interpolate import splprep, splev

def compute_medial_axis(polygon):
    """
    Compute the medial axis approximation using the Voronoi diagram.
    """
    boundary_points = np.array(polygon.exterior.coords)
    vor = Voronoi(boundary_points)

    medial_axis_points = []
    for vpair in vor.ridge_vertices:
        if -1 in vpair:
            continue
        p1, p2 = vor.vertices[vpair]
        line = LineString([p1, p2])
        if polygon.contains(line):
            medial_axis_points.append(p1)
            medial_axis_points.append(p2)

    if len(medial_axis_points) < 4:  # Need at least 4 points for splines
        return None  

    return np.array(medial_axis_points)

def smooth_medial_axis_splprep(points, num_interp=100, smoothing=0.1):
    """
    Smooth the medial axis using B-spline fitting (`splprep`).
    Handles input validation to avoid errors.
    """
    points = np.array(points)

    # Ensure we have enough points
    if points.shape[0] < 4:  # k=3 requires at least 4 points
        print("Error: Too few points for spline fitting.")
        return None, None

    # Remove duplicate consecutive points
    points = np.unique(points, axis=0)

    # Ensure the correct shape (2, N) for `splprep`
    points = points.T  # Transpose to get shape (2, N)
    
    try:
        tck, u = splprep(points, s=smoothing)  # Compute B-spline
        u_fine = np.linspace(0, 1, num_interp)  # Smooth parameter space
        x_smooth, y_smooth = splev(u_fine, tck)  # Evaluate spline

        return x_smooth, y_smooth

    except ValueError as e:
        print(f"Error in splprep: {e}")
        return None, None


def plot_nth_polygon_with_smooth_medial_axis(json_file, n):
    with open(json_file, "r") as f:
        data = json.load(f)

    if n >= len(data):
        print(f"Error: Only {len(data)} entries found. Requested index {n} is out of range.")
        return

    entry = data[n]
    wkt_string = entry["wkt_string"]
    transform = entry["transform"]

    tx, ty = map(float, transform.replace("translate(", "").replace(")", "").split(","))
    polygon = loads(wkt_string)
    translated_polygon = translate(polygon, xoff=tx, yoff=ty)
    coords = list(translated_polygon.exterior.coords)
    medial_axis_points = compute_medial_axis(translated_polygon)
    if medial_axis_points is None:
        print("Medial axis computation failed (too few points).")
        return

    x_smooth, y_smooth = smooth_medial_axis_splprep(medial_axis_points)

    fig, ax = plt.subplots(figsize=(6, 6))
    x, y = translated_polygon.exterior.xy
    ax.plot(x, y, 'b-', linewidth=2, label="Polygon Boundary")
    # Plot medial axis points
    polygon_x, polygon_y = zip(*coords)
    ax.scatter(polygon_x, polygon_y, color="green", marker="o", label="Polygon Vertices", zorder=2)
    if len(medial_axis_points) > 0:
        ax.scatter(medial_axis_points[:, 0], medial_axis_points[:, 1], c="blue", label="Medial Axis", s=10)


    ax.plot(x_smooth, y_smooth, 'r-', linewidth=3, label="Smooth Medial Axis")  # Smoothed curve

    ax.set_aspect('equal')
    #plt.legend()
    plt.show()

# Example Usage
file_name = "pavan"
brush_name = "brush_7"
INPUT_JSON_FILE = f"json/style/{file_name}-combined-dsequence-with_attributes.json"

plot_nth_polygon_with_smooth_medial_axis(INPUT_JSON_FILE, 151)
