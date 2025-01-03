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
import json, sys

def convert_command(args):
    """
    The function to handle the 'convert' subcommand.

    Args:
        args (argparse.Namespace): Parsed arguments from the CLI.
            Expects:
              - args.input_file: path to the YAML file to convert.
              - args.output_file: path to write the JSON output.
    """
    try:
        # Load the YAML file into a Python dictionary
        data = load_yaml(args.input_file)
    except Exception as e:
        print(f"Error loading YAML: {e}")
        sys.exit(1)

    #  Decide where to write the output
    #  Use a default name (e.g., 'output.json') or check if user provided `args.output_file`
    output_file = getattr(args, "output_file", "output.json")

    try:
        # Write the loaded data as JSON
        with open(output_file, 'w', encoding='utf-8') as json_file:
            json.dump(data, json_file, indent=2)
        print(f"Conversion successful! JSON written to '{output_file}'.")
    except PermissionError:
        print(f"Error: You do not have permission to write to '{output_file}'.")
        sys.exit(1)
    except OSError as e:
        print(f"Error writing to file '{output_file}': {e}")
        sys.exit(1)
    except TypeError as e:
        # e.g., if 'data' contains something not JSON-serializable 
        print(f"Error serializing JSON: {e}")
        sys.exit(1)