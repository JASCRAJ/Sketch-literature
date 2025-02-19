import json
import cv2
from shapely.geometry import Polygon, box
from PIL import Image, ImageDraw, ImageChops, ImageFilter
from shapely import wkt, Point
import numpy as np
import math
from sklearn.decomposition import PCA
import os
os.makedirs("results/comp", exist_ok=True)
file_name = "paris_river"#"pavan_noseg"#"Van_Skeleton"#"sequence-Van_Skeleton_segment_2"
brush_name = "brush_7"
INPUT_JSON_FILE = f"json/comp/{file_name}-combined-dsequence-with_attributes.json"  # Input JSON file
OUTPUT_VIDEO_NAME = f"results/comp/{file_name}-combined-sequence-{brush_name}-combined-output-video-polygonandcropimageR2.mp4"  # Output video file
LAST_FRAME_OUTPUT = f"results/comp/{file_name}-combined-sequence-{brush_name}-combined-last_frame-polygonandcropimageR2.png"  # Last frame output
INPUT_CANVAS_IMAGE = f"sketch/{file_name}.png"  # Input canvas image


#input_image = f"input/{file_name}.jpg"
BRUSH_IMAGE = f"brushes/{brush_name}.png"  # Brush stroke image
def hex_to_rgb(hex_color):
    """Convert a hex color (e.g., #FF5733) to an RGB tuple."""
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

#input_image_for_crop = Image.open(input_image).convert('RGBA')
brush_stroke = Image.open(BRUSH_IMAGE).convert('RGBA')

# Function to process each row in the JSON and update the current frame
def process_polygon_data(wkt_string, fill_colour, canvas_width, canvas_height, current_frame):
    # Parse the WKT string into a Shapely Polygon

    polygon = wkt.loads(wkt_string)
    #vertices = list(polygon.exterior.coords)
    minx, miny, maxx, maxy = polygon.bounds
    
    width = maxx - minx
    height = maxy - miny
    if width < 1 or height < 1:
        print("Width and height must be >= 2. Skipping resize operation.")
        return current_frame
    rotated_rectangle = polygon.minimum_rotated_rectangle
    # Extract the rectangle's coordinates and calculate width and height
    x, y = rotated_rectangle.exterior.coords.xy
    width_brush = math.floor(((x[1] - x[0])**2 + (y[1] - y[0])**2)**0.5)
    height_brush = math.floor(((x[2] - x[1])**2 + (y[2] - y[1])**2)**0.5)
    if width_brush < 1 or height_brush < 1:
        print("Width and height must be >= 2. Skipping resize operation.")
        return current_frame
    
    rotated_box_coords = list(rotated_rectangle.exterior.coords[:-1])  # Exclude duplicate last point

    # Find the minimum x and y to align the polygon with (0, 0)
    min_x = min(x for x, y in rotated_box_coords)
    min_y = min(y for x, y in rotated_box_coords)
    max_x = max(x for x, y in rotated_box_coords)
    max_y = max(y for x, y in rotated_box_coords)
    width1 = max_x - min_x
    height1 = max_y - min_y
    
    #pad = 100
    # width1 +=pad
    # height1 +=pad

    adjusted_coords = [(x - min_x, y - min_y) for x, y in rotated_box_coords]

    #img = Image.new('RGBA', (int(width1), int(height1)), (0, 0, 0, 0))  # Transparent background
    #draw = ImageDraw.Draw(img)
    #draw.polygon(adjusted_coords, outline= None, fill=fill_colour, width=5)
   
    def get_angle(p1, p2):
        """ Calculate the angle between two points relative to the horizontal axis. """
        dx = p2[0] - p1[0]
        dy = p2[1] - p1[1]
        return math.degrees(math.atan2(dy, dx))

    angle = get_angle(adjusted_coords[0], adjusted_coords[1])

    # width_brush +=5
    # height_brush +=5

    resized_image = brush_stroke.resize((width_brush, height_brush))
    pixels = resized_image.load()
    fill_colour = hex_to_rgb(fill_colour)
    for y in range(resized_image.height):
        for x in range(resized_image.width):
            r, g, b, a = pixels[x, y]
            if a !=0:
                pixels[x, y] = (*fill_colour, a)
    
    # 4. Rotate the resized image to match the rotated bounding box
    rotated_image = resized_image.rotate(-angle, expand=True)
    
    # 5. Create a new transparent background to hold the rotated image
    rotated_brush = Image.new('RGBA', (int(width1), int(height1)), (0, 0, 0, 0))

    # 6. Paste the rotated image into the final image (no clipping)
    rotated_brush.paste(rotated_image, (0,0), rotated_image)
    # pixels = rotated_brush.load()
    # fill_colour = hex_to_rgb(fill_colour)
    # for y in range(rotated_brush.height):
    #     for x in range(rotated_brush.width):
    #         r, g, b, a = pixels[x, y]
    #         if a != 0:  # Check if the pixel is not transparent
    #             pixels[x, y] = (*fill_colour, a)
    
    #base_r, base_g, base_b, base_a = img.split()
    #overlay_r, overlay_g, overlay_b, overlay_a = rotated_brush.split()

    # Multiply the RGB channels of base and overlay
    #result_r = Image.composite(ImageChops.multiply(base_r, overlay_r), base_r, overlay_a)
    #result_g = Image.composite(ImageChops.multiply(base_g, overlay_g), base_g, overlay_a)
    #result_b = Image.composite(ImageChops.multiply(base_b, overlay_b), base_b, overlay_a)

    # Combine the result and use the overlay's alpha channel
    #result_image = Image.merge("RGBA", (result_r, result_g, result_b, overlay_a))
    
    result_image = rotated_brush.resize((int(width1+5), int(height1+10)))
    paste_x = min(max(min_x, 0), canvas_width - width1)
    paste_y = min(max(min_y, 0), canvas_height - height1)
    
    current_frame.paste(rotated_brush, (int(paste_x), int(paste_y)), rotated_brush)  # Use result_image as a mask
    return current_frame


fps = 60  # Frames per second
fourcc = cv2.VideoWriter_fourcc(*'XVID')  # Codec for .avi format
with open(INPUT_JSON_FILE, 'r') as file:
    data_1 = json.load(file)

first_entry = data_1[0]
#print(first_entry)
canvas_width = int(float(first_entry["canvas_width"]))
canvas_height = int(float(first_entry["canvas_height"]))

#video_writer = cv2.VideoWriter(OUTPUT_VIDEO_NAME, cv2.VideoWriter_fourcc(*'XVID'), fps, (canvas_width, canvas_height))
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

print(canvas_width, canvas_height)
print(len(data_1))
for idx, row in enumerate(data_1):
    wkt_string = row.get('wkt_string')
    fill_colour = row.get('fill_colour', "red")
    current_frame = process_polygon_data(wkt_string, fill_colour, canvas_width, canvas_height, current_frame)

    frame = np.array(current_frame)
    frame = cv2.cvtColor(frame, cv2.COLOR_RGBA2BGR)
    
    if idx == len(data_1) - 1:
        current_frame.save(LAST_FRAME_OUTPUT)
        print(f"Image created and saved as {LAST_FRAME_OUTPUT}")

    video_writer.write(frame)
    #print(f"Processed frame {idx + 1}")

video_writer.release()
print(f"Video created and saved as {OUTPUT_VIDEO_NAME}")
