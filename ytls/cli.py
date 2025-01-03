# ytls/cli.py

import argparse
import sys

# Import the subcommand function
from ytls.commands.compare import compare_command


def main():
    """
    Main entry point for the ytls CLI.
    """
    parser = argparse.ArgumentParser(
        description="ytls: A one-stop shop of YAML-related CLI tools."
    )

    # Subparsers for each subcommand
    subparsers = parser.add_subparsers(
        title="subcommands",
        dest="command",
        help="Available subcommands"
    )

    # ---- Compare Subcommand ----
    compare_parser = subparsers.add_parser(
        "compare",
        help="Compare two YAML files and report differences."
    )
    compare_parser.add_argument("file1", help="Path to the first YAML file.")
    compare_parser.add_argument("file2", help="Path to the second YAML file.")
    compare_parser.add_argument(
        "-i", 
        "--ignore-order", 
        action="store_true", 
        help="Ignore the order of list items in YAML."
    )
    compare_parser.set_defaults(func=compare_command)

    # ---- Example for future subcommands (commented out) ----
    # convert_parser = subparsers.add_parser("convert", help="Convert YAML to JSON or other formats.")
    # convert_parser.add_argument("input_file", help="Path to the YAML file.")
    # convert_parser.add_argument("-to", choices=["json", "xml"], help="Target format.", required=True)
    # convert_parser.set_defaults(func=convert_command)  # you'd define convert_command in commands/convert.py

    # Parse the user's CLI input
    args = parser.parse_args()

    # If no subcommand provided, show help and exit
    if not args.command:
        parser.print_help()
        sys.exit(1)

    # Dispatch to the chosen subcommand's function
    try:
        args.func(args)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
