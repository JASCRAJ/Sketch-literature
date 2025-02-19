# import xml.etree.ElementTree as ET

# def combine_svgs(svg_files, output_file):
#     # Parse the first SVG as the base
#     base_tree = ET.parse(svg_files[0])
#     base_root = base_tree.getroot()

#     # Ensure the namespace is handled
#     namespace = {'svg': 'http://www.w3.org/2000/svg'}
#     ET.register_namespace('', namespace['svg'])

#     # Iterate through the remaining SVG files
#     for svg_file in svg_files[1:]:
#         # Parse each SVG file
#         tree = ET.parse(svg_file)
#         root = tree.getroot()

#         # Add all child elements of the current SVG to the base SVG
#         for element in root:
#             base_root.append(element)

#     # Write the combined SVG to the output file
#     base_tree.write(output_file, xml_declaration=True, encoding='utf-8')

# # Input SVG files
# svg_files = ["output_svg/dog_unseg-sequence.svg", "output_svg/dog_1-sequence.svg", "output_svg/dog_2-sequence.svg"]

# # Output combined SVG file
# output_file = "output_svg/dog_combined-sequence.svg"

# combine_svgs(svg_files, output_file)

import os
import xml.etree.ElementTree as ET

def combine_svgs(input_folder, output_file):
    # Get all SVG files in the folder
    svg_files = sorted(
        [os.path.join(input_folder, f) for f in os.listdir(input_folder) if f.endswith('.svg')],
        key=lambda x: int(x.split('_')[-1].split('.')[0])  # Extract and sort by the numeric suffix
    )

    # Ensure there are SVG files to process
    if not svg_files:
        raise ValueError("No SVG files found in the specified folder.")

    # Parse the first SVG as the base
    base_tree = ET.parse(svg_files[0])
    base_root = base_tree.getroot()

    # Ensure the namespace is handled
    namespace = {'svg': 'http://www.w3.org/2000/svg'}
    ET.register_namespace('', namespace['svg'])

    # Iterate through the remaining SVG files
    for svg_file in svg_files[1:]:
        # Parse each SVG file
        tree = ET.parse(svg_file)
        root = tree.getroot()

        # Add all child elements of the current SVG to the base SVG
        for element in root:
            base_root.append(element)

    # Write the combined SVG to the output file
    base_tree.write(output_file, xml_declaration=True, encoding='utf-8')

# Input folder containing SVG files

os.makedirs("output_svg/combined/style", exist_ok=True)
file_name="2"
# Output combined SVG file
input_folder = f"output_svg/style/{file_name}"
output_file = f"output_svg/combined/style/{file_name}-combined-sequence.svg"

print(output_file)

combine_svgs(input_folder, output_file)
