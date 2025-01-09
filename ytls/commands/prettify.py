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

import yaml
from ytls.utils.file_helpers import load_yaml

def prettify_command(args):
    prettify_yaml(args.input_file, args.output_file)


def prettify_yaml(input_file: str, output_file: str):
    data = load_yaml(input_file)
    
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            yaml.dump(data, f, default_flow_style=False)
            
    except PermissionError:
        raise PermissionError(f"Error: You do not have permission to write to '{output_file}'.")
    except OSError as e:
        raise OSError(f"Error writing to file '{output_file}': {e}")
    except TypeError as e:
        raise TypeError(f"Data in '{input_file}' is not YAML-serializable: {e}")

    
