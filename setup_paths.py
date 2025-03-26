import os
import sys

def add_all_paths(base_dir: str) -> None:
    """
    Recursively add all directories under base_dir to sys.path.
    """
    for root, dirs, _ in os.walk(base_dir):
        if root not in sys.path:
            sys.path.append(root)

if __name__ == "__main__":
    base_directory = os.path.dirname(os.path.abspath(__file__))
    add_all_paths(base_directory)
    print("All subdirectories added to sys.path.")
