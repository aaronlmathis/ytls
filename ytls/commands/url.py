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

# url.parse.quote
from urllib.parse import quote, unquote
import yaml

def url_command(args):
    """
    The function to handle the 'urlencode' subcommand.

    Args:
        args (argparse.Namespace): Parsed arguments from the CLI.
            Expects:
              - args.action: encode or decode
              - args.input_file: path to the YAML file to convert.
              - args.output_file: path to write the encoded url (optional).
              
    """
    if args.action == "encode":
        encode_url(args.input_file, args.output_file)
        print(f"Encoding successful! URL written to '{args.output_file}'.")
    elif args.action == "decode":
        decode_url(args.input_file, args.output_file)
        print(f"Decoding successful! URL written to '{args.output_file}'.")
    else:
        raise ValueError(f"Unsupported action: {args.action}")    

def encode_url(input_file, output_file):
    """
    Parses `input_file` as YAML and writes it out as an encoded URL
    
    Raises:
        PermissionError: If `output_file` cannot be written to (no permission).
        OSError: If there's a general OS error (e.g., invalid path).
        ValueError: If the data cannot be converted to encoded URL for some reason.
    """
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            raw_yaml = f.read()
    except FileNotFoundError:
        raise FileNotFoundError(f"Error: File not found - {input_file}")

    encoded = quote(raw_yaml, safe='')

    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(encoded)
    
    except PermissionError as e:
        raise PermissionError(f"No permission to write to '{output_file}': {e}")
    except OSError as e:
        raise OSError(f"Could not write to '{output_file}': {e}")   


def decode_url(input_file, output_file):
    """
    Parses `input_file` as a URL-encoded YAML string and writes it out as a YAML file.
    
    Raises:
        FileNotFoundError: If `input_file` cannot be found.
        PermissionError: If `output_file` cannot be written to (no permission).
        OSError: For other OS-level errors (e.g., invalid path).
        ValueError: If the decoded text is invalid YAML.
    """
    # Read the encoded string from input_file
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            encoded_url = f.read()
    except FileNotFoundError:
        raise FileNotFoundError(f"Error: File not found - {input_file}")
    except OSError as e:
        # Catches other I/O errors, like 'PermissionError' on read, but you can split them out if you like
        raise OSError(f"Error reading from '{input_file}': {e}")

    # Decode the URL-encoded text back to original YAML text
    decoded_yaml = unquote(encoded_url)

    # Parse the decoded text as YAML
    try:
        data = yaml.safe_load(decoded_yaml)
    except yaml.YAMLError as e:
        raise ValueError(f"Decoded text from '{input_file}' is not valid YAML: {e}")

    # 4. Write the Python data structure out as YAML
    try:
        with open(output_file, 'w', encoding='utf-8') as yaml_file:
            yaml.dump(data, yaml_file, sort_keys=False)
    except PermissionError:
        raise PermissionError(f"Error: You do not have permission to write to '{output_file}'.")
    except OSError as e:
        raise OSError(f"Error writing to '{output_file}': {e}")
    except TypeError as e:
        # This might happen if 'data' includes an object that PyYAML cannot serialize
        raise TypeError(f"Data from '{input_file}' includes non-serializable types: {e}")

