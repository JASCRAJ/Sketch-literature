import json
import cv2
from shapely.geometry import Polygon
from PIL import Image, ImageDraw, ImageChops
from shapely import wkt, Point
import numpy as np
import math
from sklearn.decomposition import PCA
import os
os.makedirs("results", exist_ok=True)
file_name = "Van_Skeleton"#"pavan_noseg"#"Van_Skeleton"#s"sequence-Van_Skeleton_segment_2"
brush_name = "brush_15"
INPUT_JSON_FILE = f"json/{file_name}-combined-sequence-with_attributes.json"  # Input JSON file
OUTPUT_VIDEO_NAME = f"results/{file_name}-combined-sequence-{brush_name}-output-video-polygonandcropimageR1wp.mp4"  # Output video file
LAST_FRAME_OUTPUT = f"results/{file_name}-combined-sequence-{brush_name}-last_frame-polygonandcropimageR1wp.png"  # Last frame output
INPUT_CANVAS_IMAGE = f"sketch/{file_name}.png"  # Input canvas image
#input_image = f"input/{file_name}.jpg"
BRUSH_IMAGE = f"brushes/{brush_name}.png"  # Brush stroke image
output_folder = f"frames_output/{file_name}_{brush_name}"
os.makedirs(output_folder, exist_ok=True) 

#input_image_for_crop = Image.open(input_image).convert('RGBA')
brush_stroke = Image.open(BRUSH_IMAGE).convert('RGBA')
def hex_to_rgb(hex_color):
    """Convert a hex color (e.g., #FF5733) to an RGB tuple."""
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
# Function to process each row in the JSON and update the current frame
def process_polygon_data(wkt_string, fill_colour, canvas_width, canvas_height, current_frame):
    # Parse the WKT string into a Shapely Polygon
    # polygon = wkt.loads(wkt_string)
    # minx, miny, maxx, maxy = polygon.bounds
    # minx, miny, maxx, maxy = map(lambda x: round(x), (minx, miny, maxx, maxy))
    
    # # Create a blank image with a transparent background (RGBA mode) for the polygon
    # width = maxx - minx
    # height = maxy - miny
    # img = Image.new('RGBA', (width, height), (0, 0, 0, 0))  # Transparent background
    # draw = ImageDraw.Draw(img)

    # # Adjust the coordinates of the polygon to align with the image's (0, 0) origin
    # adjusted_coords = [(x - minx, y - miny) for x, y in polygon.exterior.coords]
    
    # # Draw the polygon on the image
    # draw.polygon(adjusted_coords, outline=None, fill=fill_colour)
    polygon = wkt.loads(wkt_string)
    #print(polygon[0])
    #centroid = polygon.centroid
    #print(f"Centroid: {centroid.x}, {centroid.y}")
    # Calculate the minimum rotated rectangle (Oriented Bounding Box)
    

    # Print results
    # print(f"Width: {width:.2f}")
    # print(f"Height: {height:.2f}")
    # Extract the coordinates of the bounding box
    #rotated_box_coords = list(rotated_rectangle.exterior.coords)
    #rotated_box_points = [(x, y) for x, y in rotated_box_coords]
    #print(rotated_box_coords)
    #print(rotated_box_points)
    minx, miny, maxx, maxy = polygon.bounds
    # #print(polygon.bounds)
    # bounding_box = [(minx, miny), (maxx, miny), (maxx, maxy), (minx, maxy)]
    # minx, miny, maxx, maxy = map(lambda x: round(x), (minx, miny, maxx, maxy))
    # print(minx, miny, maxx, maxy)
    #print(jp)
    #print(minx, miny, maxx, maxy)
    # point1, point2 = Point(minx, miny), Point(maxx, maxy)
    # angle_deg = np.degrees(np.arctan2(point2.y - point1.y, point2.x - point1.x))
    # delta_x = maxx - minx
    # delta_y = miny - maxy
    # angle_deg = np.degrees(np.arctan2(delta_y, delta_x))  # atan2 handles all quadrants
    # #angle_deg = math.degrees(angle_radians) 
    # if 0 >= angle_deg >= -45:
    #     angle_deg=45+angle_deg
    #     angle_deg=-angle_deg
    # else:
    #     angle_deg = 0
    #print(f"The orientation angle of the object relative to the x-axis is: {angle_deg} degrees")
    #print(point1, point2, angle_deg)

    # Check if the polygon is clockwise or counterclockwise
    # from sklearn.decomposition import PCA
    # coords = list(polygon.exterior.coords)
    # pca = PCA(n_components=1)
    # pca.fit(coords)

    # # Get the angle of the principal component
    # angle = np.arctan2(pca.components_[0, 1], pca.components_[0, 0])
    # angle_deg = np.degrees(angle)
    # if (maxy-miny) > (maxx-minx):
    #     print("minor")
    #     angle_deg = angle_deg+90
    # #angle_deg = max(0, angle_deg)
    # print(angle_deg)
    # Create a blank image with a transparent background (RGBA mode)
    width = maxx - minx
    height = maxy - miny
    if width < 1 or height < 1:
        print("Width and height must be >= 2. Skipping resize operation.")
        return current_frame
    rotated_rectangle = polygon.minimum_rotated_rectangle
    # Extract the rectangle's coordinates and calculate width and height
    x, y = rotated_rectangle.exterior.coords.xy
    width_brush = math.ceil(((x[1] - x[0])**2 + (y[1] - y[0])**2)**0.5)
    height_brush = math.ceil(((x[2] - x[1])**2 + (y[2] - y[1])**2)**0.5)
    if width_brush < 1 or height_brush < 1:
        print("Width and height must be >= 2. Skipping resize operation.")
        return current_frame
    #print(width, height)
    # v1 = np.array([maxx - minx, maxy - miny])  # Vector for line (x1, y1) to (x2, y2)
    # v2 = np.array([minx - minx, maxy - miny])  # Vector for line (x1, y1) to (x3, y3)

    # # Compute the dot product and magnitudes
    # dot_product = np.dot(v1, v2)
    # magnitude_v1 = np.linalg.norm(v1)
    # magnitude_v2 = np.linalg.norm(v2)

    # # Calculate the cosine of the angle
    # cos_theta = dot_product / (magnitude_v1 * magnitude_v2)

    # # Compute the angle in radians and then convert to degrees
    # angle_radians = np.arccos(cos_theta)
    # angle_deg = np.degrees(angle_radians)
    # delta_x = maxx - minx
    # delta_y = maxy - miny
    # delta_x = maxx - minx
    # delta_y = miny - maxy
    # angle_radians = math.atan2(delta_y, delta_x)  # atan2 handles all quadrants
    # angle_deg = math.degrees(angle_radians)  # Convert to degrees
    # #print(angle_deg)
    # #angle_deg=135 * round(angle_deg / 135)
    # print(angle_deg)
    # Adjust the coordinates of the polygon to align with the image's (0, 0) origin
    #adjusted_coords = [(x - minx, y - miny) for x, y in polygon.exterior.coords]
    #*adjusted_bounding_box = [(x - minx, y - miny) for x, y in bounding_box]
    # Draw the polygon on the image
    #draw.polygon(adjusted_coords, outline=None, fill=fill_colour)
    # print(bounding_box)
    # print(adjusted_bounding_box)
    # scaled_bounding_box = [
    #     (
    #         (x / width) * canvas_width,  # Scale x
    #         (y / height) * canvas_height  # Scale y
    #     )
    #     for x, y in adjusted_bounding_box
    #     ]
    # print(scaled_bounding_box)
    # #draw.polygon(adjusted_bounding_box, outline="red", fill=fill_colour)

    # min_x = min(scaled_bounding_box, key=lambda coord: coord[0])[0]
    # max_x = max(scaled_bounding_box, key=lambda coord: coord[0])[0]
    # min_y = min(scaled_bounding_box, key=lambda coord: coord[1])[1]
    # max_y = max(scaled_bounding_box, key=lambda coord: coord[1])[1]

    # Calculate the width and height of the scaled polygon
    # scaled_polygon_width = max_x - min_x
    # scaled_polygon_height = max_y - min_y

    # # Print the width and height
    # print(f"Scaled Polygon Width: {scaled_polygon_width}")
    # print(f"Scaled Polygon Height: {scaled_polygon_height}")
    #print(jp)
    #rotated_box_points = [(x, y) for x, y in rotated_box_coords]
    #draw.line(rotated_box_points + [rotated_box_points[0]], fill="red", width=2)
    rotated_box_coords = list(rotated_rectangle.exterior.coords[:-1])  # Exclude duplicate last point

    # Find the minimum x and y to align the polygon with (0, 0)
    min_x = min(x for x, y in rotated_box_coords)
    min_y = min(y for x, y in rotated_box_coords)
    max_x = max(x for x, y in rotated_box_coords)
    max_y = max(y for x, y in rotated_box_coords)
    width1 = max_x - min_x
    height1 = max_y - min_y
    # if width1 < 1 or height1 < 1:
    #     print("Width and height must be >= 2. Skipping resize operation.")
    #     return current_frame
    
    #print(width, height)
    #print(width1, height1)
    # Translate the coordinates to align with (0, 0)
    
    adjusted_coords = [(x - min_x, y - min_y) for x, y in rotated_box_coords]
    # min_x = min(x for x, y in adjusted_coords)
    # min_y = min(y for x, y in adjusted_coords)
    # max_x = max(x for x, y in adjusted_coords)
    # max_y = max(y for x, y in adjusted_coords)
    # width1 = max_x - min_x
    # height1 = max_y - min_y
    # print(rotated_box_coords)
    # print(rotated_box_coords[0])
    # img = Image.new('RGBA', (int(width1), int(height1)), (0, 0, 0, 0))  # Transparent background
    # draw = ImageDraw.Draw(img)
    # draw.polygon(adjusted_coords, outline=None, fill=fill_colour)
    #img.save("img.png")
    #img.show()
    # print(min_x, min_y, max_x, max_y, width1, height1)
    # resized_image_brush = brush_stroke.resize((int(12), int(103))).convert('RGBA')
    # resized_image_brush.show()
    # print(jp)
    #patch = MplPolygon(polygon_vertices, closed=True, edgecolor='black', facecolor='lightgray')
    # img1 = Image.new('RGBA', (canvas_width, canvas_height), (0, 0, 0, 0))  # Transparent background
    # draw = ImageDraw.Draw(img1)
    # points = [(x, y) for x, y in polygon.exterior.coords]

    # # Draw the polygon
    # draw.polygon(points, fill= "red", outline="black")
    #img1.show()
    # rotated_rectangle = polygon.minimum_rotated_rectangle

    # # Exract the coordinates of the bounding box
    # rotated_box_coords = list(rotated_rectangle.exterior.coords)
    
    # img2 = Image.new('RGBA', (canvas_width, canvas_height), (0, 0, 0, 0))  # Transparent background
    # draw = ImageDraw.Draw(img2)
    # #points =[(x, y) for x, y in bounding_box]
    # rotated_box_points = [(x, y) for x, y in rotated_box_coords]
    # draw.line(rotated_box_points + [rotated_box_points[0]], fill="red", width=2)
    # #draw.rectangle([bounding_box[0], bounding_box[2]], outline="red", width=3)
    # # Draw the polygon
    # #draw.polygon(points, fill= "green", outline="black")
    # img2.show()
    # angle_deg = 90
    # print(angle_deg)
    # print(angle_deg/45)
    # print(angle_deg%45)
    # #print(polygon.bounds)
    # print(jp)
    #print(jp)
    # Load the brush stroke image
    # Load the brush stroke image
    # try:
    #     brush_stroke = Image.open("brushes/brush_1.png")
    # except Exception as e:
    #     print(f"Error loading brush stroke image: {e}")
    #     return current_frame

    # Resize the brush stroke to fit the cropped region size
    #resized_image_brush = brush_stroke.resize((width, height))
    # Calculate the width and height of the adjusted bounding box
    # min_x = min(x for x, y in adjusted_coords)
    # min_y = min(y for x, y in adjusted_coords)
    # max_x = max(x for x, y in adjusted_coords)
    # max_y = max(y for x, y in adjusted_coords)
    # box_width = int(max_x - min_x)
    # box_height = int(max_y - min_y)
    # min_x, min_y, max_x, max_y = rotated_rectangle.bounds
    # width1 = max_x - min_x
    # height1 = max_y - min_y
    def get_angle(p1, p2):
        """ Calculate the angle between two points relative to the horizontal axis. """
        dx = p2[0] - p1[0]
        dy = p2[1] - p1[1]
        return math.degrees(math.atan2(dy, dx))

    # Angle between the first two vertices (adjust based on rectangle orientation)
    angle = get_angle(adjusted_coords[0], adjusted_coords[1])

    # 3. Load and resize the image to fit within the bounding box
    #image = brush_stroke#Image.open('brush_stroke.png')  # Replace with the path to your image
    resized_image = brush_stroke.resize((width_brush, height_brush))
    pixels = resized_image.load()
    center_x, center_y = resized_image.width // 2, resized_image.height // 2
    max_distance = math.hypot(center_x, center_y)
    fill_colour = hex_to_rgb(fill_colour)
    for y in range(resized_image.height):
        for x in range(resized_image.width):
            r, g, b, a = pixels[x, y]
            if a !=0:
                pixels[x, y] = (*fill_colour, a)
            # if a == 0:  # If the pixel is transparent
            #     # Calculate the distance of the current pixel from the center
            #     distance = math.hypot(x - center_x, y - center_y)
                
            #     # Map the distance to a gradient factor (0 at the center, 1 at the border)
            #     gradient_factor = (distance / max_distance) + 0.3  # Normalize the distance
            #     gradient_factor = max(1, gradient_factor)
            #     #print(gradient_factor)
            #     # Calculate the blended color based on the gradient factor
            #     blended_r = int(fill_colour[0] + (255 - fill_colour[0]) * gradient_factor)
            #     blended_g = int(fill_colour[1] + (255 - fill_colour[1]) * gradient_factor)
            #     blended_b = int(fill_colour[2] + (255 - fill_colour[2]) * gradient_factor)
                
            #     # Set the new pixel color with transparency (a = 0)
            #     pixels[x, y] = (blended_r, blended_g, blended_b, 255)
            # # Calculate gradient based on position
                # gradient_factor = y / resized_image.height  # Change gradient based on height
                # gradient_factor = 0.9
                # # Calculate the blended color by mixing the fill_colour with white
                # blended_r = int(fill_colour[0] + (255 - fill_colour[0]) * gradient_factor)
                # blended_g = int(fill_colour[1] + (255 - fill_colour[1]) * gradient_factor)
                # blended_b = int(fill_colour[2] + (255 - fill_colour[2]) * gradient_factor)
                # pixels[x, y] = (blended_r, blended_g, blended_b, 255) 
                # gradient_factor = y / rotated_brush.height  # Change gradient based on height
                # gradient_colour = tuple(int(channel * gradient_factor) for channel in fill_colour)
                # #print(gradient_colour)
                # pixels[x, y] = (*fill_colour, 255)  # Set gradient color with full alpha
            #else:
                # Keep the original fill color for non-transparent pixels
                #pixels[x, y] = (*fill_colour, a)
    #resized_image.show()
    #print(Jp)
    # 4. Rotate the resized image to match the rotated bounding box
    rotated_image = resized_image.rotate(-angle, expand=True)
    #rotated_image = rotated_image.transpose(Image.FLIP_LEFT_RIGHT)
    # 5. Create a new transparent background to hold the rotated image
    rotated_brush = Image.new('RGBA', (int(width1), int(height1)), (0, 0, 0, 0))
    # 6. Paste the rotated image into the final image (no clipping)
    rotated_brush.paste(rotated_image, (0,0), rotated_image)
    # pixels = rotated_brush.load()
    # fill_colour = hex_to_rgb(fill_colour)
    # for y in range(rotated_brush.height):
    #     for x in range(rotated_brush.width):
    #         r, g, b, a = pixels[x, y]
    #         if a == 0:  # If the pixel is transparent
    #         # Calculate gradient based on position
    #             gradient_factor = y / rotated_brush.height  # Change gradient based on height
    #             # Calculate the blended color by mixing the fill_colour with white
    #             blended_r = int(fill_colour[0] + (255 - fill_colour[0]) * gradient_factor)
    #             blended_g = int(fill_colour[1] + (255 - fill_colour[1]) * gradient_factor)
    #             blended_b = int(fill_colour[2] + (255 - fill_colour[2]) * gradient_factor)
    #             pixels[x, y] = (blended_r, blended_g, blended_b, 255) 
    #             # gradient_factor = y / rotated_brush.height  # Change gradient based on height
    #             # gradient_colour = tuple(int(channel * gradient_factor) for channel in fill_colour)
    #             # #print(gradient_colour)
    #             # pixels[x, y] = (*fill_colour, 255)  # Set gradient color with full alpha
    #         else:
    #             # Keep the original fill color for non-transparent pixels
    #             pixels[x, y] = (*fill_colour, a)
            # if a != 0:  # Check if the pixel is not transparent
            #     pixels[x, y] = (*fill_colour, a)
    #rotated_brush.show()
    #pirnt(Jp)
    # Width and height of the bounding box
    
    #print(box_width, box_height)
    #print(width1, height1)
    # resized_image_brush = brush_stroke.resize((int(width_brush), int(height_brush))).convert('RGBA')
    # #resized_image_brush = brush_stroke.resize((box_width, box_height), Image.ANTIALIAS).convert('RGBA')

    # resized_image_brush.show()
    # mask = Image.new('L', (int(width1), int(height1)), 0)  # 'L' mode for grayscale (mask)
    # mask_draw = ImageDraw.Draw(mask)
    # mask_draw.polygon(adjusted_coords, fill=255)
    # #mask.show()
    # masked_brush_stroke = Image.new('RGBA', (int(width1), int(height1)), (0, 0, 0, 0))
    # masked_brush_stroke.paste(resized_image_brush, mask=mask)  
    # #img.alpha_composite(masked_brush_stroke)
    # #img.alpha_composite(resized_image_brush)
    # masked_brush_stroke.show()
    # masked_brush_stroke.save("patch_rotate.png")
    # print(Jp)
    # pad=5
    # img = img.resize((width+pad, height+pad))
    # resized_image_brush = brush_stroke.resize((width+pad, height+pad))
    #print(img.size)
    #print(resized_image_brush.size)
    #resized_image_brush.show()
    #print(jp)
    # Ensure the brush stroke image is in RGBA mode
    # if resized_image_brush.mode != 'RGBA':
    #     resized_image_brush = resized_image_brush.convert('RGBA')

    # Split into individual bands for blending
    # base_r, base_g, base_b, base_a = img.split()
    # overlay_r, overlay_g, overlay_b, overlay_a = rotated_brush.split()

    # # Multiply the RGB channels of base and overlay
    # result_r = Image.composite(ImageChops.multiply(base_r, overlay_r), base_r, overlay_a)
    # result_g = Image.composite(ImageChops.multiply(base_g, overlay_g), base_g, overlay_a)
    # result_b = Image.composite(ImageChops.multiply(base_b, overlay_b), base_b, overlay_a)

    # # Combine the result and use the overlay's alpha channel
    # result_image = Image.merge("RGBA", (result_r, result_g, result_b, overlay_a))
    #result_image.show()
    #print(Jp)
    # angle_deg=130
    #result_image = result_image.rotate(-angle_deg, expand=True)
    #result_image = result_image.rotate(angle_deg, center= (int(centroid.x), int(centroid.y)), expand=True)
    #result_image = result_image.rotate(angle_deg, expand=True, center=(minx, maxy))
    #result_image.save("patch_rotate.png")
    #result_image.show()
    #print(Jp)
    # Paste the composite image onto the current frame
    #coords = polygon.exterior.coords   

    # Get the first two vertices (coordinates)
    #vertex_1 = (int(coords[0][0]), int(coords[0][1]))  # First vertex
    #vertex_2 = coords[1]  # Second vertex

    #print("First vertex:", vertex_1)
    #print("Second vertex:", vertex_2)
    paste_x = min(max(min_x, 0), canvas_width - width1)
    paste_y = min(max(min_y, 0), canvas_height - height1)
    
    #print(paste_x, paste_y)
    #print(fill_colour)
    #result_image = result_image.rotate(angle_deg, expand=True, center=(paste_x, paste_y))
    #print(minx, miny)
    current_frame.paste(rotated_brush, (int(paste_x), int(paste_y)), rotated_brush)  # Use result_image as a mask
    #current_frame.show()
    #current_frame.paste(img1, (0, 0), img1)  # Use result_image as a mask
    #current_frame.paste(img2, (0, 0), img2)
    #current_frame.show()
    #print(jp)
    return current_frame

# Load the JSON data
# input_json_file = "json/pavan-combined-sequence-with_attributes.json"
# output_video_name = 'results/pavan-combined-sequence-brush_1-output-video.mp4'

# OpenCV VideoWriter setup
fps = 30  # Frames per second
fourcc = cv2.VideoWriter_fourcc(*'XVID')  # Codec for .avi format
with open(INPUT_JSON_FILE, 'r') as file:
    data_1 = json.load(file)

first_entry = data_1[0]
#print(first_entry)
canvas_width = int(float(first_entry["canvas_width"]))
canvas_height = int(float(first_entry["canvas_height"]))

#video_writer = cv2.VideoWriter(OUTPUT_VIDEO_NAME, cv2.VideoWriter_fourcc(*'XVID'), fps, (canvas_width, canvas_height))
video_writer = cv2.VideoWriter(OUTPUT_VIDEO_NAME, fourcc, fps, (canvas_width, canvas_height))
# Use 'mp4v' codec for MP4 files
# fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # You can also try 'avc1' for H.264

# video_writer = cv2.VideoWriter(OUTPUT_VIDEO_NAME, fourcc, fps, (canvas_width, canvas_height))

#INPUT_CANVAS_IMAGE = "sketch/Van_Skeleton.png"
try:
    current_frame = Image.open(INPUT_CANVAS_IMAGE).convert('RGBA')
    current_frame = current_frame.resize((canvas_width, canvas_height))
    #current_frame.paste(current_frame, (0, 0), current_frame)
    #current_frame.show()
    #current_frame = cv2.cvtColor(np.array(current_frame), cv2.COLOR_RGBA2BGRA)
except FileNotFoundError:
    print(f"Sketch not found: {INPUT_CANVAS_IMAGE}")
    current_frame = Image.new('RGBA', (canvas_width, canvas_height), color=(255, 255, 255, 255))

# with open(input_json_file, 'r') as file:
#     data_1 = json.load(file)  # Load the JSON data from the file

# Access the desired data
# print(len(data_1))
# first_entry = data_1[0]  # Get the first dictionary

# # Extract the desired data
# canvas_width = int(first_entry["canvas_width"])
# canvas_height = int(first_entry["canvas_height"])
print(canvas_width, canvas_height)
for idx, row in enumerate(data_1):
    wkt_string = row.get('wkt_string')
    fill_colour = row.get('fill_colour', "red")
    current_frame = process_polygon_data(wkt_string, fill_colour, canvas_width, canvas_height, current_frame)

    frame = np.array(current_frame)
    # if frame.shape[-1] != 4: 
    #     pil_image = Image.fromarray(frame)    

    #     # Now you can use show() to display the image
    #     pil_image.show()
    #     #frame.show()
    frame = cv2.cvtColor(frame, cv2.COLOR_RGBA2BGR)
    if (idx + 1) % 10 == 0:  # idx + 1 to ensure it's based on the actual frame number
        frame_filename = os.path.join(output_folder, f"frame_{idx + 1}.png")
        cv2.imwrite(frame_filename, frame)
    if idx == len(data_1) - 1:
        current_frame.save(LAST_FRAME_OUTPUT)
        print(f"Image created and saved as {LAST_FRAME_OUTPUT}")

    video_writer.write(frame)
    print(f"Processed frame {idx + 1}")

video_writer.release()
print(f"Video created and saved as {OUTPUT_VIDEO_NAME}")

# canvas_width = data_1['canvas_width'][0]
# canvas_height = data_1["canvas_height"][0]
#canvas_width = 1270  # Default canvas width
#canvas_height = 1240  # Default canvas height

# Create a VideoWriter object to write frames to the video file
#video_writer = cv2.VideoWriter(output_video_name, fourcc, fps, (canvas_width, canvas_height))

# Initialize the current frame with a blank canvas

#current_frame = Image.new('RGBA', (canvas_width, canvas_height), color=(255, 255, 255, 255))
# file_name = "pavan"
# INPUT_CANVAS_IMAGE = f"sketch/{file_name}.png"
# try:
#     current_frame = Image.open(INPUT_CANVAS_IMAGE).convert('RGBA')
# except FileNotFoundError:
#     print(f"Sketch not found: {INPUT_CANVAS_IMAGE}")
#     current_frame = Image.new('RGBA', (canvas_width, canvas_height), color=(255, 255, 255, 255))
# Process each entry in the JSON file and accumulate frames
# with open(input_json_file, "r") as json_file:
#     print(json_file)
#     data = json.load(json_file)
#     l_data = len(data)
#     print(l_data)
#     #print(jp)
#     for idx, row in enumerate(data):
#         wkt_string = row.get('wkt_string')
#         fill_colour = row.get('fill_colour', "red")  # Default to red if not provided
#         #canvas_width = row.get('canvas_width')
#         #print(canvas_width)
#         #print(jp)
#         #print(idx)
#         #canvas_height = row.get('canvas_height')
#         # Update the current frame with the new polygon data
#         current_frame = process_polygon_data(wkt_string, fill_colour, canvas_width, canvas_height, current_frame)

#         # Convert the current frame to a format suitable for OpenCV (BGR)
#         frame = np.array(current_frame)
#         frame = cv2.cvtColor(frame, cv2.COLOR_RGBA2BGR)
#         if idx == l_data-1:
#             current_frame.save("results/pavan-combined-sequence-brush_1-last_frame.png")
#             print(f"image created and saved")
#         # if idx == 10:
#         #     break;
#         # Write the frame to the videoWWW
#         video_writer.write(frame)

#         print(f"Processed frame {idx + 1}")

# # Release the video writer and finalize the video file
# video_writer.release()
# print(f"Video created and saved as {output_video_name}")
