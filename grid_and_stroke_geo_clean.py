import json
import cv2
from shapely.geometry import Polygon
from shapely import wkt
import numpy as np
import math
from shapely.affinity import translate
import time
import re
import os
from PIL import Image
# Start the timer
start_time = time.time()

os.makedirs("results/style", exist_ok=True)
file_name = "van_gogh_portarait_6_c"
INPUT_JSON_FILE = f"json/style/{file_name}-combined-dsequence-with_attributes.json"
OUTPUT_VIDEO_NAME = f"results/style/{file_name}-geo-output-video-polygonandcropimageR1.mp4"
LAST_FRAME_OUTPUT = f"results/style/{file_name}-geo-last_frame-polygonandcropimageR1.png"
INPUT_CANVAS_IMAGE = f"sketch/{file_name}.png"

def parse_transform(transform):
    """Extract translate(x, y) values from transform attribute."""
    match = re.search(r'translate\((-?\d+\.?\d*),?\s*(-?\d+\.?\d*)?\)', transform)
    if match:
        x = float(match.group(1))
        y = float(match.group(2)) if match.group(2) else 0
        return x, y
    return 0, 0

# def hex_to_bgr(hex_color):
#     """Convert HEX color to BGR format for OpenCV."""
#     hex_color = hex_color.lstrip("#")
#     rgb = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
#     return rgb[::-1]  # Reverse to (B, G, R) for OpenCV

def hex_to_bgra(hex_color, alpha=255):
    """Convert hex color to BGRA format"""
    hex_color = hex_color.lstrip('#')
    if len(hex_color) != 6:
        raise ValueError("Invalid hex color format. Expected 6 characters (e.g., #RRGGBB).")
    r, g, b = [int(hex_color[i:i+2], 16) for i in (0, 2, 4)]  # Extract RGB
    return (r, g, b, alpha)  # Converrt to BGRA (OpenCV format)

def process_polygon_data(wkt_string, fill_colour, transform, canvas_width, canvas_height, current_frame):
    polygon = wkt.loads(wkt_string)
    tx, ty = parse_transform(transform)
    polygon = translate(polygon, xoff=tx, yoff=ty)

    rotated_rectangle = polygon.minimum_rotated_rectangle
    x, y = rotated_rectangle.exterior.coords.xy
    width_brush = math.floor(((x[1] - x[0])**2 + (y[1] - y[0])**2)**0.5)
    height_brush = math.floor(((x[2] - x[1])**2 + (y[2] - y[1])**2)**0.5)
    
    if width_brush < 1 or height_brush < 1:
        print("Width and height must be >= 2. Skipping resize operation.")
        return current_frame
    
    rotated_box_coords = list(rotated_rectangle.exterior.coords[:-1])
    print("start")
    print(rotated_box_coords)
    # # Find the bottom-left point (smallest y, then smallest x)
    # bottom_left = min(points, key=lambda p: (p[1], p[0]))
    # print(bottom_left)
    # # Find the index of the bottom-left point
    # min_index = points.index(bottom_left)
    
    # # Rotate the points list to start from the bottom-left point
    # ordered_points = points[min_index:] + points[:min_index]
    # print(ordered_points)
    ordered_points = sorted(rotated_box_coords, key=lambda p: (p[0], p[1]))
    min_x = min(x for x, y in ordered_points)
    min_y = min(y for x, y in ordered_points)
    max_x = max(x for x, y in ordered_points)
    max_y = max(y for x, y in ordered_points)
    print(min_x, min_y, max_x, max_y)
    width1 = int(max_x - min_x)
    height1 = int(max_y - min_y)
    adjusted_coords = [(x - min_x, y - min_y) for x, y in ordered_points]

    x1, y1, x2, y2 = map(int, [adjusted_coords[0][0], adjusted_coords[0][1],
                                adjusted_coords[1][0], adjusted_coords[1][1]])
    
    line_width = adjusted_coords[2][0] - adjusted_coords[0][0]
    print(adjusted_coords)
    #print(adjusted_coords[2][0], adjusted_coords[0][0])
    print(line_width)

    #print(jp)
    # Create transparent image (zero-initialized for RGBA)
    img = np.zeros((height1, width1, 4), dtype=np.uint8)  # Height first
    print(fill_colour)
    cv_color = hex_to_bgra(fill_colour, 255)
    print(cv_color)
    # Draw line with transparency
    cv2.line(img, (x1, y1), (x2, y2), cv_color, 10)
    #img = cv2.flip(img, 0)
    #rgb_image = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    # Convert NumPy array to PIL Image
    pil_image = Image.fromarray(img, mode="RGBA")
    
    # Save with transparency
    
    #pil_image.save("img.png", format="PNG")

    # Convert NumPy array to PIL Image
    # pil_image = Image.fromarray(img, mode="RGBA")
    # #pil_image = pil_image.convert("RGBA")
    pil_image.show()
    # pil_image.save('img.png')
    # cv2.imshow("image",img)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    # alpha = img[:, :, 3] / 255.0
    # overlay_rgb = img[:, :, :3]

    paste_x = int(min(max(min_x, 0), canvas_width - width1))
    paste_y = int(min(max(min_y, 0), canvas_height - height1))
    # roi = current_frame[paste_y:paste_y + img.shape[0], paste_x:paste_x + img.shape[1]]

    # for c in range(3):
    #     roi[:, :, c] = (1 - alpha) * roi[:, :, c] + alpha * overlay_rgb[:, :, c]

    # current_frame[paste_y:paste_y + img.shape[0], paste_x:paste_x + img.shape[1]] = roi
    current_frame.paste(pil_image, (int(paste_x), int(paste_y)), pil_image)
    #current_frame.show()
    return current_frame

fps = 3  # Frames per second
fourcc = cv2.VideoWriter_fourcc(*'XVID')
with open(INPUT_JSON_FILE, 'r') as file:
    data_1 = json.load(file)

first_entry = data_1[0]
canvas_width = int(float(first_entry["canvas_width"]))
canvas_height = int(float(first_entry["canvas_height"]))

video_writer = cv2.VideoWriter(OUTPUT_VIDEO_NAME, fourcc, fps, (canvas_width, canvas_height))

try:
    current_frame = Image.open(INPUT_CANVAS_IMAGE).convert('RGBA')
    current_frame = current_frame.resize((canvas_width, canvas_height))
    #current_frame.paste(current_frame, (0, 0), current_frame)
    #current_frame.show()
    #current_frame = cv2.cvtColor(np.array(current_frame), cv2.COLOR_RGBA2BGRA)
except FileNotFoundError:
    print(f"Sketch not found: {INPUT_CANVAS_IMAGE}")
    current_frame = Image.new('RGBA', (canvas_width, canvas_height), color=(255, 255, 255, 255))

for idx, row in enumerate(data_1):
    wkt_string = row.get('wkt_string')
    fill_colour = row.get('fill_colour', "red")
    transform = row.get("transform", "0")
    current_frame = process_polygon_data(wkt_string, fill_colour, transform, canvas_width, canvas_height, current_frame)
    # cv2.imshow("image",current_frame)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()


    #frame = current_frame
    frame = np.array(current_frame)
    frame = cv2.cvtColor(frame, cv2.COLOR_RGBA2BGR)
    # cv2.imshow("image",frame)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    if idx == len(data_1) - 1:
        current_frame.save(LAST_FRAME_OUTPUT)
        print(f"Image created and saved as {LAST_FRAME_OUTPUT}")

    video_writer.write(frame)

video_writer.release()
print(f"Video created and saved as {OUTPUT_VIDEO_NAME}")

# End the timer
end_time = time.time()

# Calculate and display the execution time
execution_time = end_time - start_time
print(f"Execution time: {execution_time:.6f} seconds")
