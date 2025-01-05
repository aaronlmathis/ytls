# ytls - YAML Tools
# Copyright (C) 2025 Aaron Mathis
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later
# version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of  MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# this program.  If not, see <http://www.gnu.org/licenses/>.

from ytls.utils.file_helpers import load_yaml
import json, sys, os
import xml.etree.ElementTree as ET
from xml.dom import minidom

def convert_command(args):
    """
    The function to handle the 'convert' subcommand.

    Args:
        args (argparse.Namespace): Parsed arguments from the CLI.
            Expects:
              - args.input_file: path to the YAML file to convert.
              - args.output_file: path to write the JSON output.
              - args.to: output file format
    """
    if args.to == "json":
        convert_to_json(args.input_file, args.output_file)
        print(f"Conversion successful! JSON written to '{args.output_file}'.")
    elif args.to == "xml":
        convert_to_xml(args.input_file, args.output_file, args.root_element_name)
        print(f"Conversion successful! XML written to '{args.output_file}'.")
    else:
        raise ValueError(f"Unsupported output format: {args.to}")

def convert_to_json(input_file, output_file):
    """
    Parses `input_file` as YAML and writes it out as json to `output_file`.
    
    Raises:
        PermissionError: If `output_file` cannot be written to (no permission).
        OSError: If there's a general OS error (e.g., invalid path).
        ValueError: If the data cannot be converted to JSON for some reason.
    """
    data = load_yaml(input_file)

    try:
        # Write the loaded data as JSON
        with open(output_file, 'w', encoding='utf-8') as json_file:
            json.dump(data, json_file, indent=2)
            
    except PermissionError:
        raise PermissionError(f"Error: You do not have permission to write to '{output_file}'.")
    except OSError as e:
        raise OSError(f"Error writing to file '{output_file}': {e}")
    except TypeError as e:
        raise TypeError(f"Data in '{input_file}' is not JSON-serializable: {e}")

def dict_to_xml(parent: ET.Element, data):
    """
    Recursively convert a Python dictionary/list/scalar to XML elements
    and attach them to the `parent` XML element.
    """
    if isinstance(data, dict):
        for key, value in data.items():
            # Ensure the key is a valid string for an XML tag
            tag_name = str(key)
            child_elem = ET.SubElement(parent, tag_name)
            dict_to_xml(child_elem, value)
    elif isinstance(data, list):
        # Use a generic "item" tag for each list entry
        for item in data:
            item_elem = ET.SubElement(parent, "item")
            dict_to_xml(item_elem, item)
    else:
        # If data is a scalar (str, int, float, bool, etc.), convert it to string
        parent.text = str(data)

def convert_to_xml(input_file, output_file, root_element_name=None):
    """
    Parses `input_file` as YAML and writes it out as XML to `output_file`.
    
    Raises:
        PermissionError: If `output_file` cannot be written to (no permission).
        OSError: If there's a general OS error (e.g., invalid path).
        ValueError: If the data cannot be converted to XML for some reason.
    """
    if root_element_name is None:
        root_element_name = os.path.splitext(os.path.basename(input_file))[0]

    data = load_yaml(input_file)

    root = ET.Element(root_element_name)
    try:
        dict_to_xml(root, data)
    except TypeError as e:
        # Catch unexpected data structures or issues converting to text
        raise ValueError(f"Encountered non-serializable data: {e}")
    
    rough_string = ET.tostring(root, encoding='utf-8')
    
    try:
        reparsed = minidom.parseString(rough_string)
        pretty_xml = reparsed.toprettyxml(indent="  ")
    except Exception as e:
        # Catch any minidom errors or unexpected data
        raise ValueError(f"Failed to pretty-print XML: {e}")
    
    try:
        with open(output_file, 'w', encoding='utf-8') as xml_file:
            xml_file.write(pretty_xml)
    except PermissionError as e:
        raise PermissionError(f"No permission to write to '{output_file}': {e}")
    except OSError as e:
        raise OSError(f"Could not write to '{output_file}': {e}")    