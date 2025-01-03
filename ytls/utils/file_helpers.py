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

import sys
import yaml
from pprint import pprint

def load_yaml(file_path):
    """
    Load a YAML file and return its contents as a Python dictionary.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = yaml.safe_load(file)
            print(f"\nLoaded '{file_path}':")
            pprint(data)
            return data
    except FileNotFoundError:
        print(f"Error: File not found - {file_path}")
        sys.exit(1)
    except yaml.YAMLError as exc:
        print(f"Error parsing YAML file {file_path}: {exc}")
        sys.exit(1)
