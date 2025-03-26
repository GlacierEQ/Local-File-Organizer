import os
import shutil
import json
import logging
from typing import List, Dict
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# List of protected system directories
PROTECTED_PATHS = [
    'C:\\Windows',
    'C:\\Program Files',
    'C:\\Program Files (x86)',
    'C:\\ProgramData',
    'C:\\Users\\All Users',
    'C:\\Users\\Default',
    'C:\\Users\\Public'
]

def load_config() -> Dict:
    """Load configuration for document sorting from a JSON file."""
    with open('config.json') as config_file:
        return json.load(config_file)

def is_protected_path(path: str) -> bool:
    """Check if a path is in a protected system directory."""
    try:
        path = os.path.abspath(path)
        return any(path.startswith(protected) for protected in PROTECTED_PATHS)
    except Exception as e:
        logger.error(f"Error checking protected path: {e}")
        return True

def get_file_type_folder(file: str, output_root: str) -> str:
    """
    Determine the output directory based on the file type.

    Args:
        file (str): The name of the file.
        output_root (str): The root directory for output.

    Returns:
        str: The output directory path.
    """
    try:
        file_ext = os.path.splitext(file)[1][1:].lower()
        # Map common extensions to more descriptive folder names
        extension_map = {
            'doc': 'word',
            'docx': 'word',
            'pdf': 'pdf',
            'xls': 'excel',
            'xlsx': 'excel',
            'ppt': 'powerpoint',
            'pptx': 'powerpoint',
            'txt': 'text',
            'csv': 'data'
        }
        folder_name = extension_map.get(file_ext, file_ext)
        return os.path.join(output_root, folder_name)
    except Exception as e:
        logger.error(f"Error determining file type folder: {e}")
        return os.path.join(output_root, 'unknown')

def sort_documents() -> None:
    """Sort documents based on specified criteria."""
    try:
        config = load_config()
        scan_paths = config['scan_paths']
        output_root = config['output_root']
        file_types = config['file_types']['documents']

        for path in scan_paths:
            if is_protected_path(path):
                logger.warning(f"Skipping protected path: {path}")
                continue

            for root, dirs, files in os.walk(path):
                # Skip hidden directories
                dirs[:] = [d for d in dirs if not d.startswith('.')]

                for file in files:
                    if any(file.endswith(ext) for ext in file_types):
                        file_path = os.path.join(root, file)
                        
                        if is_protected_path(file_path):
                            logger.warning(f"Skipping protected file: {file_path}")
                            continue

                        output_dir = get_file_type_folder(file, output_root)
                        os.makedirs(output_dir, exist_ok=True)
                        
                        try:
                            dest_path = os.path.join(output_dir, file)
                            if os.path.exists(dest_path):
                                # Handle duplicate files
                                base, ext = os.path.splitext(file)
                                counter = 1
                                while os.path.exists(dest_path):
                                    new_name = f"{base}_{counter}{ext}"
                                    dest_path = os.path.join(output_dir, new_name)
                                    counter += 1
                            
                            shutil.move(file_path, dest_path)
                            logger.info(f"Moved {file_path} to {dest_path}")
                        except Exception as e:
                            logger.error(f"Error moving file {file_path} to {output_dir}: {e}")
    except Exception as e:
        logger.error(f"Error in sort_documents: {e}")

def auto_sort_documents(interval: int = 300) -> None:
    """Automatically sort documents at specified intervals.

    Args:
        interval (int): The interval in seconds between sorting operations.
    """
    import time
    while True:
        sort_documents()
        time.sleep(interval)

if __name__ == "__main__":
    sort_documents()
