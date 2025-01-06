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
import base64


def base64_command(args):
    """
    The function to handle the 'base64' subcommand.

    Args:
        args (argparse.Namespace): Parsed arguments from the CLI.
            Expects:
              - args.input_file: path to the YAML file to convert.
              - args.split: Whether to split base64 into chunks, if so, how many symbol per chunk (optional).
              - args.output_file: path to the YAML file to convert.
              
    """
    if args.action == "encode":
        encode_base64(args.input_file, args.output_file, args.split)
        print(f"Encoding successful! base64 written to '{args.output_file}'.")
    elif args.action == "decode":
        decode_base64(args.input_file, args.output_file)
        print(f"Decoding successful! base64 written to '{args.output_file}'.")
    else:
        raise ValueError(f"Unsupported action: {args.action}")    

def encode_base64(input_file: str, output_file: str, split: int = None):
    """
    Parses `input_file` as YAML and writes it out as base64
    
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

    if isinstance(raw_yaml, str):
        data = raw_yaml.encode('utf-8')  # Convert string to bytes if necessary
    
    if split is None:
        encoded_data = [base64.b64encode(data).decode('utf-8')] 
    else:
        encoded_data = []
        for i in range(0, len(data), split):
            chunk = data[i:i+split]
            encoded_chunk = base64.b64encode(chunk).decode('utf-8')
            encoded_data.append(encoded_chunk)
    
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            for data in encoded_data:
                f.write(data + "\n")
    
    except PermissionError as e:
        raise PermissionError(f"No permission to write to '{output_file}': {e}")
    except OSError as e:
        raise OSError(f"Could not write to '{output_file}': {e}")   
    
def decode_base64(input_file: str, output_file: str):
    """
    Parses `input_file` as YAML and writes it out as base64
    
    Raises:
        PermissionError: If `output_file` cannot be written to (no permission).
        OSError: If there's a general OS error (e.g., invalid path).
        ValueError: If the data cannot be converted to encoded URL for some reason.
    """
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
           encoded_yaml = f.read()
    except FileNotFoundError:
        raise FileNotFoundError(f"Error: File not found - {input_file}")

    if isinstance(encoded_yaml, str):
        data = encoded_yaml.encode('utf-8') 

    decoded_yaml = base64.b64decode(data).decode('utf-8')
    
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(decoded_yaml)
            
    except PermissionError as e:
        raise PermissionError(f"No permission to write to '{output_file}': {e}")
    except OSError as e:
        raise OSError(f"Could not write to '{output_file}': {e}")           