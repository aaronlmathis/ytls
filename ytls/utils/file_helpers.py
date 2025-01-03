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
