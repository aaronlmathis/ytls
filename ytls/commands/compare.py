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
from deepdiff import DeepDiff
from pprint import pprint

from ytls.utils.file_helpers import load_yaml


def compare_yamls(yaml1, yaml2, ignore_order=True):
    """
    Compare two Python dictionaries and return the differences.
    """
    differences = DeepDiff(yaml1, yaml2, ignore_order=ignore_order)
    return differences


def compare_command(args):
    """
    The function to handle the 'compare' subcommand.

    Args:
        args: Parsed arguments from the CLI (argparse.Namespace).
    """
    try:
        # Load the YAML files into Python dictionaries
        yaml1 = load_yaml(args.file1)
        yaml2 = load_yaml(args.file2)
    except Exception as e:
        print(f"Error loading YAML: {e}")
        sys.exit(1)

    differences = compare_yamls(yaml1, yaml2, args.ignore_order)

    if differences:
        print("\nDifferences found:")
        # Show different categories of differences
        if 'values_changed' in differences:
            print("\nValues Changed:")
            pprint(differences['values_changed'])

        if 'dictionary_item_added' in differences:
            print("\nItems Added:")
            pprint(differences['dictionary_item_added'])

        if 'dictionary_item_removed' in differences:
            print("\nItems Removed:")
            pprint(differences['dictionary_item_removed'])

        # Add more categories as needed
    else:
        print("\nThe YAML files are identical.")
