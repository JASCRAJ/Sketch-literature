import json
from PIL import Image, ImageDraw
import os

file_name = "244530fgsdl"
folder_name = "artworks_18_04_seg_selected"

# Paths
INPUT_JSON_PATH = f"results/{folder_name}/{file_name}_stroke_params.json"
INPUT_IMAGE_PATH = f"{folder_name}/{file_name}-w/{file_name}.jpg"
OUTPUT_IMAGE_PATH = f"results/{folder_name}/{file_name}_with_bboxes.png"

# Load input image
try:
    image = Image.open(INPUT_IMAGE_PATH)
except FileNotFoundError:
    raise FileNotFoundError(f"Input image not found at: {INPUT_IMAGE_PATH}")

draw = ImageDraw.Draw(image)

# Load stroke parameters
with open(INPUT_JSON_PATH, "r") as f:
    strokes = json.load(f)

# Step 3: Draw each bbox as a polygon
for stroke in strokes:
    bbox = stroke.get("bbox", [])
    if len(bbox) == 4:  # Ensure it's a valid quadrilateral
        polygon_points = [tuple(pt) for pt in bbox]
        draw.polygon(polygon_points, outline="red", width=0.2)

# Save output image
os.makedirs(os.path.dirname(OUTPUT_IMAGE_PATH), exist_ok=True)
image.save(OUTPUT_IMAGE_PATH)
print(f"Image with bounding boxes saved to: {OUTPUT_IMAGE_PATH}")
