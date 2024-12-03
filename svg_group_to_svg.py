import xml.etree.ElementTree as ET

def strip_namespace(tag):
    # Remove the namespace prefix from a tag
    return tag.split('}', 1)[-1] if '}' in tag else tag

def update_svg_fill_from_file(input_file, output_file):
    # Parse the SVG file
    tree = ET.parse(input_file)
    root = tree.getroot()

    # Remove namespace prefixes
    for elem in root.iter():
        elem.tag = strip_namespace(elem.tag)

    # Iterate over all <g> elements
    for g in root.findall('.//g'):
        fill = g.attrib.get('fill')  # Get the fill attribute from the group
        paths = g.findall('.//path')

        # Transfer the fill attribute to each <path>
        for path in paths:
            if fill and 'fill' not in path.attrib:
                path.attrib['fill'] = fill

        # Remove the <g> element but keep its children
        parent = root.find('./g/..')  # Find the parent of <g>
        if parent is not None:
            parent.extend(g.findall('./*'))  # Add children of <g> to parent
            parent.remove(g)  # Remove the <g> element

    # Save the updated SVG to the output file
    tree.write(output_file)


# Example usage
input_svg_file = 'stacked_vect_io_star_night.svg'  # Your input SVG file path
output_svg_file = 'stacked_vect_io_star_night-output.svg'  # Output file path after modification

update_svg_fill_from_file(input_svg_file, output_svg_file)
