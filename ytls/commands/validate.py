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

import yaml
import sys
from pykwalify.core import Core


def validate_syntax(filepath: str) -> bool:
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            yaml.safe_load(f)
        return True
    except yaml.YAMLError as e:
        print(f"YAML syntax error in {filepath}:\n{e}", file=sys.stderr)
        return False
    except FileNotFoundError:
        print(f"File not found: {filepath}", file=sys.stderr)
        return False
    except Exception as e:
        print(f"Unexpected error reading {filepath}: {e}", file=sys.stderr)
        return False

def validate_schema(input_file: str, schema_file:str) -> True:
    try:
        c = Core(source_file=input_file, schema_files=[schema_file])
        c.validate()
        return True
    except Exception as e:
        print(f"Schema validation error:\n{e}", file=sys.stderr)
        return False

def validate_command(args):
    if args.schema is None:
        if validate_syntax(args.input_file):
            print(f"'{args.input_file}' is valid YAML syntax.")
            sys.exit(0)  # success
        else:
            print(f"'{args.input_file}' is invalid YAML.")
    else:
        if validate_schema(args.input_file, args.schema):
            print(f"'{args.input_file}' conforms to the schema found in '{args.schema}'")
