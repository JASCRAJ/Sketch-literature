import xml.etree.ElementTree as ET
import pandas as pd
import re
import os
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from scipy.cluster.hierarchy import linkage, fcluster
from scipy.spatial.distance import pdist
#import cairosvg

common_path = 'Drawing_line_svg-csv'
#File_name = 'Naked MalewithArmsRaised'

def extract_numeric_values(s):
    # Use regular expression to extract numeric values
    return re.findall(r'[-+]?\d*\.\d+|\d+', s)

def hierarchical_clustering(csv_file_path):
    df = pd.read_csv(csv_file_path)
    distances = pdist(df[['X_value', 'Y_value']])
    max_distance = df['width'].iloc[0]/4
    print(max_distance)
    linkage_matrix = linkage(distances, method='ward')
    clusters = fcluster(linkage_matrix, t=max_distance, criterion='distance')
    df['Cluster'] = clusters
    df_sorted = df.sort_values(by='Cluster')
    num_clusters = len(set(clusters))
    print("Number of clusters:", num_clusters)
    return df_sorted


def save_svg_and_png_files_head(df_sorted, output_dir_svg, output_dir_png, File_name):
    os.makedirs(output_dir_svg, exist_ok=True)
    #os.makedirs(output_dir_png, exist_ok=True)
    width = df_sorted['width'].iloc[0]
    height = df_sorted['height'].iloc[0]
    cumulative_svg_content = f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}">'
    #cumulative_svg_content += f'<rect width="{width}" height="{height}" fill="white"/>\n'
    grouped_clusters = df_sorted.groupby('Cluster')

    for cluster, group in grouped_clusters:
        paths_data = group['path_data'].tolist()
        stroke = group['fill'].tolist()
        #print(stroke)

        svg_content = ''

        for path_data, color in zip(paths_data, stroke):
            svg_content += f'<path d="{path_data}" fill="{color}" />\n'
            #svg_content += f'<path d="{path_data}" stroke="{color}" fill="{"none"}" stroke-width="{"1.00"}" vector-effect="{"non-scaling-stroke"}"/>\n'

        cumulative_svg_content += svg_content

        svg_file_path_cluster = os.path.join(output_dir_svg, f'{File_name}_accumulated_clusters_1_{cluster}.svg')
        with open(svg_file_path_cluster, 'w') as f:
            f.write(cumulative_svg_content + '</svg>')

        #png_file_path = os.path.join(output_dir_png, f'{File_name}_accumulated_clusters_1_{cluster}.png')
        #cairosvg.svg2png(url=svg_file_path_cluster, write_to=png_file_path)

    return cumulative_svg_content

def save_svg_and_png_files_rest(df_sorted, output_dir_svg, output_dir_png, File_name, p_data):
    os.makedirs(output_dir_svg, exist_ok=True)
    #os.makedirs(output_dir_png, exist_ok=True)
    width = df_sorted['width'].iloc[0]
    height = df_sorted['height'].iloc[0]
    #cumulative_svg_content = f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}">'
    cumulative_svg_content = p_data
    grouped_clusters = df_sorted.groupby('Cluster')

    for cluster, group in grouped_clusters:
        paths_data = group['path_data'].tolist()
        fill = group['fill'].tolist()


        svg_content = ''
        for path_data, color in zip(paths_data, fill):
            svg_content += f'<path d="{path_data}" fill="{color}" />\n'
            #svg_content += f'<path d="{path_data}" stroke="{color}" fill="{"none"}" stroke-width="{"1.00"}" vector-effect="{"non-scaling-stroke"}"/>\n'

        # for path_data, style in zip(paths_data, stroke):
        #     svg_content += f'<path d="{path_data}" style="{stroke}" />\n'
            #svg_content += f'<path d="{path_data}" style="fill: none; stroke: black;stroke-width: 2px;" />\n'

        cumulative_svg_content += svg_content
        f_content = cumulative_svg_content + '</svg>'

        svg_file_path = os.path.join(output_dir_svg, f'{File_name}_accumulated_clusters_2_{cluster}.svg')
        with open(svg_file_path, 'w') as f:
            f.write(f_content)

        #png_file_path = os.path.join(output_dir_png, f'{File_name}_accumulated_clusters_2_{cluster}.png')
        #cairosvg.svg2png(url=svg_file_path, write_to=png_file_path)

def process_files(File_name):
    print(File_name)
    #print(jp)
    csv_file_path_head = os.path.join(common_path, File_name + '_head.csv')
    csv_file_path_rest = os.path.join(common_path, File_name + '_rest.csv')
    svg_output_dir = os.path.join(common_path, File_name + 'svg_files')
    png_output_dir = os.path.join(common_path, File_name +'png_files')

    df_sorted_head = hierarchical_clustering(csv_file_path_head)
    df_sorted_rest = hierarchical_clustering(csv_file_path_rest)
    p_data = save_svg_and_png_files_head(df_sorted_head, svg_output_dir, png_output_dir, File_name)
    p_data = save_svg_and_png_files_rest(df_sorted_rest, svg_output_dir, png_output_dir, File_name, p_data)

# Main script to process all files in the directory

drawing_svg_path = 'Drawing_line_svg'
files = [f.split('.svg')[0] for f in os.listdir(drawing_svg_path)]
#print(files)
#print(jp)
for file_name in files:
    process_files(file_name)