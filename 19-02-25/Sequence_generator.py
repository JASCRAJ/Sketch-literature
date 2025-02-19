import os
import sys
import re
import xml.etree.ElementTree as ET
import pandas as pd
import matplotlib.pyplot as plt
from scipy.cluster.hierarchy import linkage, fcluster
from scipy.spatial.distance import pdist

# Precompile the regular expression for efficiency
NUMERIC_REGEX = re.compile(r'[-+]?\d*\.\d+|\d+')

def parse_dimension(value):
        return float(value.replace('px', '').strip()) if 'px' in value else float(value)

def extract_numeric_values(s):
    """Extract numeric values from a string using a precompiled regex."""
    return NUMERIC_REGEX.findall(s)

def parse_svg(svg_file):
    """Parse SVG file and extract relevant path data efficiently."""
    tree = ET.parse(svg_file)
    root = tree.getroot()
    
    # Extract viewBox and parse width and height
    view_box = root.get('viewBox')
    if view_box:
        _, _, svg_width, svg_height = map(float, view_box.split())
    else:
        # Fallback if viewBox is not present
        svg_width = parse_dimension(root.get('width', '1000'))
        svg_height = parse_dimension(root.get('height', '1000'))
        #svg_width = float(root.get('width', '1000'))
        #svg_height = float(root.get('height', '1000'))
    
    # Namespace handling to avoid repeated namespace strings
    namespaces = {'svg': 'http://www.w3.org/2000/svg'}
    
    # Initialize lists to collect path attributes
    path_datas = []
    fills = []
    x_values = []
    y_values = []
    path_lengths = []
    
    # Iterate through path elements using efficient list extraction
    for path_elem in root.findall('.//svg:path', namespaces):
        path_data = path_elem.get('d', '')
        fill = path_elem.get('fill', '')
        
        # Extract numeric values
        numeric_values = extract_numeric_values(path_data)
        
        # Safely extract X and Y values
        M_x = numeric_values[0] if len(numeric_values) >= 1 else None
        M_y = numeric_values[1] if len(numeric_values) >= 2 else None
        
        # Calculate the length of the path data
        path_length = len(path_data)
        
        # Append to lists
        path_datas.append(path_data)
        fills.append(fill)
        x_values.append(float(M_x) if M_x else None)
        y_values.append(float(M_y) if M_y else None)
        path_lengths.append(path_length)
    
    # Create DataFrame using collected lists
    df = pd.DataFrame({
        'path_data': path_datas,
        'fill': fills,
        'X_value': x_values,
        'Y_value': y_values,
        'path_length': path_lengths,
        'width': svg_width,
        'height': svg_height
    })
    
    # Sort DataFrame based on 'path_length' in descending order
    df.sort_values(by='path_length', ascending=False, inplace=True)
    df.reset_index(drop=True, inplace=True)
    
    return df

def hierarchical_clustering(df, max_distance=100):
    """Perform hierarchical clustering on the DataFrame and plot the results."""
    # Drop rows with missing X or Y values to avoid errors in clustering
    df_clean = df.dropna(subset=['X_value', 'Y_value'])
    
    # Compute pairwise distances and perform linkage
    distances = pdist(df_clean[['X_value', 'Y_value']])
    linkage_matrix = linkage(distances, method='ward')
    
    # Form clusters based on the maximum distance
    clusters = fcluster(linkage_matrix, t=max_distance, criterion='distance')
    df_clean['Cluster'] = clusters
    df_sorted = df_clean.sort_values(by='Cluster')
    num_clusters = df_sorted['Cluster'].nunique()
    print(f"Number of clusters: {num_clusters}")
    return df_sorted

def dataframe_to_svg(df, svg_file_path):
    """Generate an SVG file from the DataFrame containing path data."""
    if df.empty:
        print("DataFrame is empty. No SVG will be generated.")
        return
    
    # Get the width and height from the first row
    width = df['width'].iloc[0]
    height = df['height'].iloc[0]
    
    # Start building the SVG content
    svg_elements = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}">\n'
    ]
    
    # Efficiently concatenate path elements
    svg_elements.extend([
        f'  <path d="{path_data}" fill="{fill_color}" />\n'
        for path_data, fill_color in zip(df['path_data'], df['fill'])
    ])
    
    # Close the SVG tag
    svg_elements.append('</svg>')
    
    # Write the SVG content to the file
    with open(svg_file_path, 'w') as svg_file:
        svg_file.writelines(svg_elements)

def process_folder(input_folder, output_folder):
    """Process all SVG files in the input folder and save outputs in the output folder."""
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for file_name in os.listdir(input_folder):
        if file_name.endswith('.svg'):
            svg_file_path = os.path.join(input_folder, file_name)
            print(f"Processing file: {svg_file_path}")

            df = parse_svg(svg_file_path)
            df_combined = hierarchical_clustering(df, max_distance=100)
            # subset_gt = df.iloc[0:10]
            # subset_le = df.iloc[10:]

            # df_sorted_gt = hierarchical_clustering(subset_gt, max_distance=100)
            # df_sorted_le = hierarchical_clustering(subset_le, max_distance=100)

            # df_combined = pd.concat([df_sorted_gt, df_sorted_le], ignore_index=True)

            base_file_name = os.path.splitext(file_name)[0]
            output_svg_path = os.path.join(output_folder, f"sequence-{base_file_name}.svg")

            dataframe_to_svg(df_combined, output_svg_path)
            print(f"Saved output SVG to: {output_svg_path}")

if __name__ == '__main__':
    # Check if the right number of arguments are passed
    if len(sys.argv) != 3:
        print("Usage: python script.py <input_folder> <output_folder>")
        sys.exit(1)

    input_folder = sys.argv[1]
    output_folder = sys.argv[2]

    # Call the function to process all SVG files in the input folder
    process_folder(input_folder, output_folder)
