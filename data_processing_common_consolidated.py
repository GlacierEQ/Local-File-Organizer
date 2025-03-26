import os
import re
import datetime
from rich.progress import Progress, TextColumn, BarColumn, TimeElapsedColumn

def load_document_text(file_path: str) -> str:
    """Load and return the text content of a document."""
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()

def sanitize_filename(name, max_length=50, max_words=5):
    """Sanitize the filename by removing unwanted words and characters."""
    # Implementation remains the same as in both original files
    # ... [sanitize_filename implementation] ...

def get_file_size_category(file_path):
    """Determine file size category."""
    size = os.path.getsize(file_path)
    if size < 1024 * 1024:  # Less than 1MB
        return 'small'
    elif size < 10 * 1024 * 1024:  # Less than 10MB
        return 'medium'
    else:  # 10MB or larger
        return 'large'

def process_files_by_date(file_paths, output_path, dry_run=False, silent=False, log_file=None, legal_files=None):
    """Process files to organize them by date."""
    # Implementation from NewAyge version
    # ... [process_files_by_date implementation] ...

def process_files_by_type(file_paths, output_path, dry_run=False, silent=False, log_file=None, legal_files=None):
    """Process files to organize them by type, first separating into text-based and image-based files."""
    # Implementation from NewAyge version, including ebook support
    # ... [process_files_by_type implementation] ...

def compute_operations(data_list, new_path, renamed_files, processed_files, legal_files=None):
    """Compute the file operations based on generated metadata."""
    # Implementation from NewAyge version, including legal files handling
    # ... [compute_operations implementation] ...

def execute_operations(operations, dry_run=False, silent=False, log_file=None):
    """Execute the file operations."""
    # Implementation remains the same as in both original files
    # ... [execute_operations implementation] ...

# Add any additional helper functions or constants as needed
