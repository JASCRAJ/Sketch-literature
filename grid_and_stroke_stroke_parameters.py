import json
import os
import math
import numpy as np
from shapely import wkt

file_name = "244530fgsdl"
folder_name = "artworks_18_04_seg_selected"
folder_path = os.path.join("results", folder_name)
os.makedirs(folder_path, exist_ok=True)


INPUT_JSON_FILE = f"json/{folder_name}/{file_name}-combined-dsequence-with_attributes.json"
OUTPUT_JSON_FILE = f"results/{folder_name}/{file_name}_stroke_params.json"
OUTPUT_NPZ_FILE = f"results/{folder_name}/{file_name}_stroke_params.npz"

with open(INPUT_JSON_FILE, 'r') as file:
    data_1 = json.load(file)

first_entry = data_1[0]
canvas_width = int(float(first_entry["canvas_width"]))
canvas_height = int(float(first_entry["canvas_height"]))

def get_angle(p1, p2):
    dx = p2[0] - p1[0]
    dy = p2[1] - p1[1]
    return math.degrees(math.atan2(dy, dx))

all_strokes = []

for idx, row in enumerate(data_1):
    stroke_info = {}
    wkt_string = row.get('wkt_string')
    fill_colour = row.get('fill_colour', "None")

    polygon = wkt.loads(wkt_string)
    minx, miny, maxx, maxy = polygon.bounds
    width = maxx - minx
    height = maxy - miny

    if width < 2 or height < 2:
        continue  # Skip small strokes

    rotated_rectangle = polygon.minimum_rotated_rectangle
    rotated_box_coords = list(rotated_rectangle.exterior.coords[:-1])  # Remove last duplicate point

    if len(rotated_box_coords) < 2:
        continue
    angle = get_angle(rotated_box_coords[0], rotated_box_coords[1])
    stroke_info['angle'] = angle
    stroke_info['index'] = idx
    stroke_info['bbox'] = rotated_box_coords
    stroke_info['canvas_width'] = canvas_width
    stroke_info['canvas_height'] = canvas_height
    stroke_info['fill_colour'] = fill_colour
    all_strokes.append(stroke_info)

# # Save to JSON
with open(OUTPUT_JSON_FILE, 'w') as out_file:
    json.dump(all_strokes, out_file, indent=2)

# Optional: Save to NPZ (carefully)
np.savez(OUTPUT_NPZ_FILE, strokes=np.array(all_strokes, dtype=object))


print(f"Saved stroke parameters to:\n- {OUTPUT_JSON_FILE}\n- {OUTPUT_NPZ_FILE}")
