import os
import shutil

SORTED_DIR = os.path.join("Sorting_Area", "Sorted_Files")

def merge_small_folders(threshold: int = 5) -> None:
    """
    Merge folders with fewer than 'threshold' files into a "Misc" folder.
    """
    misc_folder = os.path.join(SORTED_DIR, "Misc")
    os.makedirs(misc_folder, exist_ok=True)
    for category in os.listdir(SORTED_DIR):
        category_path = os.path.join(SORTED_DIR, category)
        if os.path.isdir(category_path) and category != "Misc":
            if len(os.listdir(category_path)) < threshold:
                # Move files into Misc folder
                for file in os.listdir(category_path):
                    shutil.move(os.path.join(category_path, file), misc_folder)
                # Optionally remove empty folder:
                os.rmdir(category_path)
