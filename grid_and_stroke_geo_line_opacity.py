import json
import cv2
from shapely.geometry import Polygon, LineString
from shapely import wkt
import numpy as np
import re
import os
from PIL import Image
import time
from shapely.affinity import translate
import math

# Start timer
start_time = time.time()

# Create output directories
os.makedirs("results/style", exist_ok=True)

file_name = "van_gogh_portarait_6_c"
INPUT_JSON_FILE = f"json/style/{file_name}-combined-dsequence-with_attributes.json"
OUTPUT_VIDEO_NAME = f"results/style/{file_name}-geo-output-video-polygonandcropimageR1.mp4"
LAST_FRAME_OUTPUT = f"results/style/{file_name}-geo-last_frame-polygonandcropimageR1.png"

# Gaussian function parameters
mu = 0.5  # Mean at the middle
sigma = 0.2  # Spread

# Function to extract transform data
def parse_transform(transform):
    match = re.search(r'translate\((-?\d+\.?\d*),?\s*(-?\d+\.?\d*)?\)', transform)
    if match:
        x = float(match.group(1))
        y = float(match.group(2)) if match.group(2) else 0
        return x, y
    return 0, 0

# Convert hex to OpenCV BGR format
def hex_to_bgr(hex_color):
    hex_color = hex_color.lstrip('#')
    r, g, b = [int(hex_color[i:i+2], 16) for i in (0, 2, 4)]
    return (b, g, r)  # OpenCV uses BGR format
 #int(height * 2)  # Increase for smooth animation
# Process a polygon frame
# Define Gaussian function with normalization
def gaussian_opacity(fraction, mu=0.5, sigma=0.2, min_alpha=0.2, max_alpha=1.0):
    """
    Compute Gaussian opacity for smooth animation transition.
    Ensures that opacity starts and ends at min_alpha (0.2) and peaks at max_alpha.
    """
    raw_alpha = math.exp(-((fraction - mu) ** 2) / (2 * sigma ** 2))
    
    # Normalize to range [0, 1] (max value occurs at fraction = mu)
    peak_value = math.exp(0)  # exp(0) = 1 (highest value in Gaussian curve)
    normalized_alpha = raw_alpha / peak_value  # Scale between 0 and 1

    # Rescale to [min_alpha, max_alpha]
    alpha = min_alpha + (max_alpha - min_alpha) * normalized_alpha
    return alpha

# # Example usage
# for i in range(6):  # steps = 5, so index from 0 to 5
#     fraction = i / 5
#     alpha = gaussian_opacity(fraction)
#     print(f"Step {i}: Opacity = {alpha:.3f}")

def process_polygon_data(idx, wkt_string, fill_colour, transform, canvas_width, canvas_height, current_canvas, video_writer):
    polygon = wkt.loads(wkt_string)
    tx, ty = parse_transform(transform)
    polygon = translate(polygon, xoff=tx, yoff=ty)

    rotated_rectangle = polygon.minimum_rotated_rectangle
    #coords = list(rotated_rectangle.exterior.coords[:-1])
    if not rotated_rectangle.is_valid:
        print("Rotated rectangle is invalid.")
    else:
        min_x, min_y, max_x, max_y = rotated_rectangle.bounds
        width = max_x - min_x
        height = max_y - min_y

    # Compute actual width and height
    # edge_lengths = [np.linalg.norm(np.array(coords[i]) - np.array(coords[i-1])) for i in range(len(coords))]
    # print(edge_lengths)
    # width, height = sorted(set(edge_lengths))[:2]  # Extract two unique values

    if width < 2 or height < 2:
        print(f"Skipping frame {idx}: Invalid rectangle dimensions.")
        return current_canvas

    # Convert polygon to integer pixel coordinates
    #pts = np.array(coords, dtype=np.int32)

    # Get BGR color
    cv_color = hex_to_bgr(fill_colour)
    rotated_box_coords = list(rotated_rectangle.exterior.coords[:-1])
    edges = [
        LineString([rotated_box_coords[i], rotated_box_coords[(i + 1) % 4]]) for i in range(4)
    ]

    # Find the longest edge (this determines the orientation)
    longest_edge = max(edges, key=lambda e: e.length)

    # Get the two points defining this longest edge
    p1, p2 = longest_edge.coords  # Extract coordinates

    # Compute the center of the rectangle
    center_x = sum(p[0] for p in rotated_box_coords) / 4
    center_y = sum(p[1] for p in rotated_box_coords) / 4
    center = (center_x, center_y)

    # Compute angle of the longest edge
    angle = np.arctan2(p2[1] - p1[1], p2[0] - p1[0])
    #print(angle)
    # Define a line through the center with the same angle
    line_length = longest_edge.length  # Or set custom length
    half_length = line_length / 2

    mid_line_point1 = (center_x - half_length * np.cos(angle), center_y - half_length * np.sin(angle))
    mid_line_point2 = (center_x + half_length * np.cos(angle), center_y + half_length * np.sin(angle))
    # angle = get_angle(mid_line_point1, mid_line_point2)
    # print(angle)
    # angle3 = get_angle(p2, p1)
    # angle2 = get_angle(p3, p4)
    # angle4 = get_angle(p4, p3)
    #print(angle, angle1, angle2, angle3, angle4)
    # Convert to integer tuples
    x1 = int(mid_line_point1[0])
    y1 = int(mid_line_point1[1])
    x2 = int(mid_line_point2[0]) 
    y2 = int(mid_line_point2[1])
    #print(midpoint_1_2)
    #x1, y1, x2, y2 = map(int, [ordered_points[0][0], ordered_points[0][1], ordered_points[1][0], ordered_points[1][1]])
    #print(ordered_points[2])
    #distance = int(np.linalg.norm(np.array(p1) - np.array(p2)))
    #distance2 = int(np.linalg.norm(np.array(r1) - np.array(r2)))
    # distance = min(distance1, distance2)
    #distance3 = int(np.linalg.norm(np.array(p3) - np.array(p4)))
    #print(distance1, distance2)

    # line_width = int(ordered_points[2][0] - ordered_points[1][0])  # Ensure line width ≥ 1
    # line_width = int(ordered_points[2][0] - ordered_points[1][0])
    # if distance > width or distance > height:
    #     print(distance, width, height) 
    thickness = int(min(width, height)/2)
    # Define step count based on height
    

    # Progressive animation loop
    #for i in range(steps + 1):
        # # Get interpolated point for stroke animation
        # fraction = i / steps
        # # interp_x = int(x1 + (pts[1][0] - pts[0][0]) * fraction)
        # # interp_y = int(y1 + (pts[1][1] - pts[0][1]) * fraction)
        # x = int(x1 + (x2 - x1) * fraction)
        # y = int(y1 + (y2 - y1) * fraction)
        # # Gaussian opacity (peaks at the middle)
        # alpha = math.exp(-((fraction - mu) ** 2) / (2 * sigma ** 2))
        #  # Apply minimum opacity limit
        # alpha = max(0.1, alpha)
        # # Draw line progressively
        # cv2.line(current_canvas, (x1, y1), (x, y), cv_color, thickness=thickness, lineType=cv2.LINE_AA)
        # cv2.addWeighted(current_canvas, alpha, current_canvas, 1 - alpha, 0, current_canvas)
        # # Save each frame to video
        # video_writer.write(current_canvas)
    print("start")
    for i in range(steps + 1):
        fraction = i / steps
        x = int(x1 + (x2 - x1) * fraction)
        y = int(y1 + (y2 - y1) * fraction)
        
        # Gaussian opacity (peaks at the middle)
        # alpha = math.exp(-((fraction - mu) ** 2) / (2 * sigma ** 2))
        # print(alpha)
        # alpha = max(0.2, alpha)  # Apply minimum opacity limit
        #alpha = max(0.2, 0.9 - fraction)
        alpha = gaussian_opacity(fraction, mu=0.5, sigma=0.2, min_alpha=0.1, max_alpha=0.9)
        print(alpha)
        # Create a transparent overlay
        overlay = current_canvas.copy()
        # Draw the line on the overlay
        cv2.line(overlay, (x1, y1), (x, y), cv_color, thickness=thickness, lineType=cv2.LINE_AA)

        # Blend the overlay with the main canvas using Gaussian opacity
        cv2.addWeighted(overlay, alpha, current_canvas, 1 - alpha, 0, current_canvas)
        # cv2.imshow("Animation", current_canvas)
        # cv2.waitKey(300)
        # cv2.destroyAllWindows()
        #print(jp)
        # Save each frame to video
        video_writer.write(current_canvas)

    return current_canvas

# Video settings
fps = 90
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
steps = 10
# Load JSON data
with open(INPUT_JSON_FILE, 'r') as file:
    data_1 = json.load(file)

first_entry = data_1[0]
canvas_width = int(float(first_entry["canvas_width"]))
canvas_height = int(float(first_entry["canvas_height"]))

video_writer = cv2.VideoWriter(OUTPUT_VIDEO_NAME, fourcc, fps, (canvas_width, canvas_height), isColor=True)

# Initialize blank white RGB image
current_canvas = np.ones((canvas_height, canvas_width, 3), dtype=np.uint8) * 255

# Process each polygon in sequence
for idx, row in enumerate(data_1):
    wkt_string = row.get('wkt_string')
    fill_colour = row.get('fill_colour', "#FF0000")  # Default to red
    transform = row.get("transform", "translate(0,0)")

    # Draw and animate polygon on canvas
    current_canvas = process_polygon_data(idx, wkt_string, fill_colour, transform, canvas_width, canvas_height, current_canvas, video_writer)
    
    # Uncomment for real-time preview
    # cv2.imshow("Animation", current_canvas)
    # cv2.waitKey(30)
    # if idx == 50:
    #     break
    # Save last frame
    if idx == len(data_1) - 1:
        Image.fromarray(cv2.cvtColor(current_canvas, cv2.COLOR_BGR2RGB)).save(LAST_FRAME_OUTPUT)
        print(f"Last frame saved as {LAST_FRAME_OUTPUT}")

# Cleanup
video_writer.release()
cv2.destroyAllWindows()
print(f"Video saved as {OUTPUT_VIDEO_NAME}")

# End timer
end_time = time.time()
print(f"Execution time: {(end_time - start_time)/60:.6f} seconds")
