import os

# Define the folder containing SVG files
svg_folder = "Drawing_line_svg" 
# Define the output folder for CSV files
output_folder = "Drawing_line_svg-csv"
os.makedirs(output_folder, exist_ok=True)


# List SVG files in the folder
svg_files = [f for f in os.listdir(svg_folder) if f.endswith('.svg')]
import xml.etree.ElementTree as ET
import pandas as pd
import re

def extract_numeric_values(s):
    # Use regular expression to extract numeric values
    return re.findall(r'[-+]?\d*\.\d+|\d+', s)

def parse_svg(svg_file):
    tree = ET.parse(svg_file)
    root = tree.getroot()
    view_box = root.get('viewBox')
    view_box_values = view_box.split()
    svg_width = float(view_box_values[2])  # width is the third value
    svg_height = float(view_box_values[3])  # height is the fourth value

    paths = []

    # Iterate through path elements
    for path_elem in root.findall('.//{http://www.w3.org/2000/svg}path'):
        path_data = path_elem.get('d')
        fill = path_elem.get('fill')

        # Check if fill color is not "#ffffff"
        if fill != "#ffffff":
            # Extract numeric values from path_data using the custom function
            numeric_values = extract_numeric_values(path_data)

            # Extract the second and third elements
            M_x = numeric_values[0] if len(numeric_values) > 1 else None
            M_y = numeric_values[1] if len(numeric_values) > 2 else None

            # Calculate the length of the path data
            path_length = len(path_data)

            paths.append({
                'path_data': path_data,
                'fill': fill,
                'X_value': M_x,
                'Y_value': M_y,
                'path_length': path_length  # Add path length to the dictionary
            })

    # Create DataFrame from paths list
    df = pd.DataFrame(paths)

    # Add width and height to the DataFrame
    df['width'] = svg_width
    df['height'] = svg_height

    # Sort DataFrame based on 'path_length' in descending order
    df.sort_values(by='path_length', ascending=False, inplace=True)

    return df
def save_to_csv(dataframe, csv_filename):
    dataframe.to_csv(csv_filename, index=False)
# Process each SVG file
for svg_file in svg_files:
    # Parse SVG paths and create a DataFrame
    df = parse_svg(os.path.join(svg_folder, svg_file))

    # Split DataFrame based on path_length condition
    subset_path_length_head = df.iloc[0:10]
    subset_path_length_rest = df.iloc[10:]

    # Define output filenames
    filename_head = os.path.splitext(svg_file)[0] + "_head.csv"
    filename_rest = os.path.splitext(svg_file)[0] + "_rest.csv"

    # Define output paths
    output_path_head = os.path.join(output_folder, filename_head)
    output_path_rest = os.path.join(output_folder, filename_rest)

    # Save CSV files to the output folder
    save_to_csv(subset_path_length_head, output_path_head)
    save_to_csv(subset_path_length_rest, output_path_rest)

    print(f"Processed SVG file: {svg_file}. Saved as: {filename_head} and {filename_rest} in {output_folder}")
