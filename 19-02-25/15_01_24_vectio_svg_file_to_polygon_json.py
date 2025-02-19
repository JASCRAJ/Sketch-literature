import xml.etree.ElementTree as ET
from svgpath2mpl import parse_path
from shapely.geometry import Polygon, box
import json
import re
import numpy as np
import os
# Input SVG file
filename = "2" #"sequence-Van_Skeleton_segment_0"
input_svg_file = f"output_svg/combined/style/{filename}-combined-sequence.svg"
output_file = f"json/style/{filename}-combined-dsequence-with_attributes.json"
os.makedirs("json/style", exist_ok=True)

def extract_fill_colour(style):
    match = re.search(r'fill:\s*([^;]+)', style)
    if match:
        return match.group(1)
    return None

def extract_svg_paths_with_attributes(svg_file):
    tree = ET.parse(svg_file)
    root = tree.getroot()
    namespace = {'svg': 'http://www.w3.org/2000/svg'}
    path_data = []
    viewbox = root.attrib.get("viewBox")

    if viewbox:
        min_x, min_y, width, height = map(int, viewbox.split())
    else:
        width = root.attrib.get("width", "1500").replace("px", "").strip()
        height = root.attrib.get("height", "1500").replace("px", "").strip()

    for path in root.findall('.//svg:path', namespace):
        svg_path_data = path.get('d')
        transform = path.get('transform')
        style = path.get('style')
        fill_colour = path.get('fill')

        if svg_path_data:
            path_data.append({
                'path': svg_path_data,
                'transform': transform,
                'style': style,
                'fill_colour': fill_colour,
                'width': width,
                'height': height
            })
    return path_data

def apply_transform(poly, transform):
    if transform and "translate" in transform:
        match = re.search(r"translate\(([^,]+),([^\)]+)\)", transform)
        if match:
            tx, ty = map(float, match.groups())
            poly[:, 0] += tx
            poly[:, 1] += ty
    return poly

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

svg_data = extract_svg_paths_with_attributes(input_svg_file)
output_data = []
threshold_area = 20000  # Define the area threshold

from shapely.ops import unary_union
from shapely.geometry import MultiPolygon
def save_decomposed_polygon(groups, original_data):
    for group in groups:
        unified_polygon = unary_union([Polygon(list(cell.exterior.coords)) for cell in group])
        # Convert MULTIPOLYGON to a single polygon by taking the convex hull
        # if isinstance(unified_polygon, MultiPolygon):
        #     unified_polygon = unified_polygon.convex_hull
        #shapely_group = [Polygon(list(cell.exterior.coords)) for cell in group]
        output_data.append({
            #'wkt_string': [g.wkt for g in shapely_group],
            'wkt_string': unified_polygon.wkt,
            #'path': original_data['path'],
            #'transform': original_data['transform'],
            #'style': original_data['style'],
            'fill_colour': original_data['fill_colour'],
            'canvas_width': original_data['width'],
            'canvas_height': original_data['height']
        })

for data in svg_data:
    svg_path_data = data['path']
    #transform = data['transform']
    #style = data['style']
    fill_colour = data['fill_colour']
    width = data['width']
    height = data['height']

    mpl_path = parse_path(svg_path_data)
    polygons = mpl_path.to_polygons()

    for poly in polygons:
        poly = np.array(poly)
        shapely_polygon = Polygon(poly)

        if shapely_polygon.area > threshold_area:
            
            vertices = list(shapely_polygon.exterior.coords)
            grid_size = 2
            grid_cells = grid_based_decomposition(vertices, grid_size)
            sequencing = construct_sequencing(vertices, grid_cells, strategy="row-wise")
            num_groups = max(1, len(grid_cells) // 1000)
            print(num_groups)
            groups = split_into_groups(sequencing, num_groups)
            save_decomposed_polygon(groups, data)
        else:
            output_data.append({
                'wkt_string': shapely_polygon.wkt,
                #'path': data['path'],
                #'transform': transform,
                #'style': style,
                'fill_colour': fill_colour,
                'canvas_width': width,
                'canvas_height': height
            })

with open(output_file, "w") as json_file:
    json.dump(output_data, json_file, indent=4)

print(f"Processed {len(output_data)} polygons and saved to {output_file}")
