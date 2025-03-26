import os
import shutil
import json
import datetime
import hashlib
import webbrowser
import string
import chevron  # For mustache templating
from path_manager import PathManager
from data_processing_common import (
    process_files_by_type, 
    process_files_by_date, 
    execute_operations,
    sanitize_filename,
    get_file_size_category
)
from file_utils import collect_file_paths

def get_all_drives():
    """Get all available drives on Windows."""
    drives = []
    for letter in string.ascii_uppercase:
        drive = f"{letter}:\\"
        if os.path.exists(drive):
            drives.append(drive)
    return drives

def collect_all_files():
    """Collect files from all available drives."""
    all_files = []
    drives = get_all_drives()
    
    # System directories and files to exclude
    exclude_dirs = {
        'Windows', 'Program Files', 'Program Files (x86)', 
        'ProgramData', '$Recycle.Bin', 'System Volume Information',
        'Recovery'
    }
    
    exclude_files = {
        'pagefile.sys', 'hiberfil.sys', 'swapfile.sys'
    }
    
    print("Scanning drives:", ', '.join(drives))
    
    for drive in drives:
        print(f"\nScanning drive {drive}")
        try:
            for root, dirs, files in os.walk(drive, topdown=True):
                # Remove excluded directories
                dirs[:] = [d for d in dirs if d not in exclude_dirs]
                
                for file in files:
                    if file not in exclude_files:
                        try:
                            file_path = os.path.join(root, file)
                            # Only include if we can access the file
                            if os.access(file_path, os.R_OK):
                                all_files.append(file_path)
                        except (PermissionError, OSError):
                            continue
        except (PermissionError, OSError) as e:
            print(f"Error accessing {drive}: {str(e)}")
            continue
            
    return all_files

def improve_filename(filepath):
    """Improve a filename by sanitizing it and adding context."""
    base_name = os.path.basename(filepath)
    name, ext = os.path.splitext(base_name)
    
    # Sanitize the name
    clean_name = sanitize_filename(name)
    
    # Add context based on file type
    if ext.lower() in ['.jpg', '.jpeg', '.png', '.gif', '.bmp']:
        clean_name = f"image_{clean_name}"
    elif ext.lower() in ['.doc', '.docx']:
        clean_name = f"document_{clean_name}"
    elif ext.lower() == '.pdf':
        clean_name = f"pdf_{clean_name}"
    elif ext.lower() in ['.xls', '.xlsx']:
        clean_name = f"spreadsheet_{clean_name}"
    elif ext.lower() == '.txt':
        clean_name = f"text_{clean_name}"
    elif ext.lower() == '.md':
        clean_name = f"markdown_{clean_name}"
    elif ext.lower() in ['.ppt', '.pptx']:
        clean_name = f"presentation_{clean_name}"
    elif ext.lower() == '.csv':
        clean_name = f"data_{clean_name}"
    elif ext.lower() in ['.mp3', '.wav', '.flac', '.m4a']:
        clean_name = f"audio_{clean_name}"
    elif ext.lower() in ['.mp4', '.avi', '.mkv', '.mov']:
        clean_name = f"video_{clean_name}"
    elif ext.lower() in ['.zip', '.rar', '.7z']:
        clean_name = f"archive_{clean_name}"
    elif ext.lower() in ['.exe', '.msi']:
        clean_name = f"program_{clean_name}"
    
    return clean_name + ext.lower()

def clean_directory(directory):
    """Remove a directory and its contents if it exists."""
    if os.path.exists(directory):
        shutil.rmtree(directory)

def organize_by_size(file_paths, base_output_dir):
    """Organize files by size category with improved names"""
    output_path = os.path.join(base_output_dir, 'organized_by_size')
    
    # Clean existing directory
    clean_directory(output_path)
    
    # Create output directory
    os.makedirs(output_path, exist_ok=True)
    
    print("\nOrganizing by size...")
    print(f"Output directory: {output_path}")
    
    # Create operations based on file size
    operations = []
    for file_path in file_paths:
        try:
            size_category = get_file_size_category(file_path)
            dest_dir = os.path.join(output_path, f"{size_category}_files")
            improved_name = improve_filename(file_path)
            new_dest = os.path.join(dest_dir, improved_name)
            operations.append({
                'source': file_path,
                'destination': new_dest,
                'link_type': 'copy'  # Use copy instead of hardlink for cross-drive operations
            })
        except (PermissionError, OSError):
            continue
    
    print(f"Generated {len(operations)} operations")
    
    # Execute operations
    execute_operations(operations, dry_run=False, silent=False)
    
    print("Size-based organization complete!")

def organize_by_type(file_paths, base_output_dir):
    """Organize files by type with improved names"""
    output_path = os.path.join(base_output_dir, 'organized_by_type')
    
    # Clean existing directory
    clean_directory(output_path)
    
    # Create output directory
    os.makedirs(output_path, exist_ok=True)
    
    print("\nOrganizing by type...")
    print(f"Output directory: {output_path}")
    
    # Process files by type
    operations = process_files_by_type(file_paths, output_path)
    
    # Improve filenames in operations
    improved_operations = []
    for op in operations:
        try:
            dest_dir = os.path.dirname(op['destination'])
            improved_name = improve_filename(op['source'])
            new_dest = os.path.join(dest_dir, improved_name)
            improved_operations.append({
                'source': op['source'],
                'destination': new_dest,
                'link_type': 'copy'  # Use copy instead of hardlink for cross-drive operations
            })
        except (PermissionError, OSError):
            continue
    
    print(f"Generated {len(improved_operations)} operations")
    
    # Execute operations
    execute_operations(improved_operations, dry_run=False, silent=False)
    
    print("Type-based organization complete!")

def organize_by_date(file_paths, base_output_dir):
    """Organize files by date with improved names"""
    output_path = os.path.join(base_output_dir, 'organized_by_date')
    
    # Clean existing directory
    clean_directory(output_path)
    
    # Create output directory
    os.makedirs(output_path, exist_ok=True)
    
    print("\nOrganizing by date...")
    print(f"Output directory: {output_path}")
    
    # Process files by date
    operations = process_files_by_date(file_paths, output_path)
    
    # Improve filenames in operations
    improved_operations = []
    for op in operations:
        try:
            dest_dir = os.path.dirname(op['destination'])
            improved_name = improve_filename(op['source'])
            new_dest = os.path.join(dest_dir, improved_name)
            improved_operations.append({
                'source': op['source'],
                'destination': new_dest,
                'link_type': 'copy'  # Use copy instead of hardlink for cross-drive operations
            })
        except (PermissionError, OSError):
            continue
    
    print(f"Generated {len(improved_operations)} operations")
    
    # Execute operations
    execute_operations(improved_operations, dry_run=False, silent=False)
    
    print("Date-based organization complete!")

def organize_by_type_and_date(file_paths, base_output_dir):
    """Organize files by type and date with improved names"""
    output_path = os.path.join(base_output_dir, 'organized_by_type_and_date')
    
    # Clean existing directory
    clean_directory(output_path)
    
    # Create output directory
    os.makedirs(output_path, exist_ok=True)
    
    print("\nOrganizing by type and date...")
    print(f"Output directory: {output_path}")
    
    # Process files by type first
    type_operations = process_files_by_type(file_paths, output_path)
    
    # Then organize by date within each type
    final_operations = []
    for op in type_operations:
        try:
            source = op['source']
            type_dir = os.path.dirname(op['destination'])
            
            # Get date information
            mod_time = os.path.getmtime(source)
            mod_datetime = datetime.datetime.fromtimestamp(mod_time)
            year = mod_datetime.strftime('%Y')
            month = mod_datetime.strftime('%B')
            
            # Create final path combining type and date
            date_dir = os.path.join(type_dir, year, month)
            improved_name = improve_filename(source)
            new_dest = os.path.join(date_dir, improved_name)
            
            final_operations.append({
                'source': source,
                'destination': new_dest,
                'link_type': 'copy'  # Use copy instead of hardlink for cross-drive operations
            })
        except (PermissionError, OSError):
            continue
    
    print(f"Generated {len(final_operations)} operations")
    
    # Execute operations
    execute_operations(final_operations, dry_run=False, silent=False)
    
    print("Type and date-based organization complete!")

def generate_organization_stats(base_paths):
    """Generate statistics about the organized files."""
    stats = {
        'total_files': 0,
        'by_type': {},
        'by_size': {
            'small': 0,  # < 1MB
            'medium': 0, # 1-10MB
            'large': 0   # > 10MB
        },
        'by_date': {},
        'total_size': 0
    }
    
    for base_path in base_paths:
        for root, _, files in os.walk(base_path):
            for file in files:
                file_path = os.path.join(root, file)
                try:
                    stats['total_files'] += 1
                    
                    # Get file extension
                    ext = os.path.splitext(file)[1].lower()
                    stats['by_type'][ext] = stats['by_type'].get(ext, 0) + 1
                    
                    # Get file size
                    size = os.path.getsize(file_path)
                    stats['total_size'] += size
                    if size < 1024 * 1024:  # < 1MB
                        stats['by_size']['small'] += 1
                    elif size < 10 * 1024 * 1024:  # < 10MB
                        stats['by_size']['medium'] += 1
                    else:
                        stats['by_size']['large'] += 1
                    
                    # Get file date
                    mod_time = os.path.getmtime(file_path)
                    date = datetime.datetime.fromtimestamp(mod_time).strftime('%Y-%m')
                    stats['by_date'][date] = stats['by_date'].get(date, 0) + 1
                except (PermissionError, OSError):
                    continue
    
    return stats

def print_stats(stats):
    """Print organization statistics in a nice format."""
    print("\n=== File Organization Statistics ===")
    print(f"\nTotal Files: {stats['total_files']}")
    print(f"Total Size: {stats['total_size'] / (1024*1024*1024):.2f} GB")
    
    print("\nFiles by Type:")
    for ext, count in sorted(stats['by_type'].items(), key=lambda x: x[1], reverse=True):
        print(f"  {ext or 'no extension'}: {count}")
    
    print("\nFiles by Size:")
    for category, count in stats['by_size'].items():
        print(f"  {category}: {count}")
    
    print("\nFiles by Month:")
    for date, count in sorted(stats['by_date'].items(), reverse=True):
        print(f"  {date}: {count}")

def generate_html_report(stats):
    """Generate an HTML report with charts and statistics."""
    # Prepare data for the template
    template_data = {
        'total_files': stats['total_files'],
        'total_size_gb': f"{stats['total_size'] / (1024*1024*1024):.1f}",
        'total_types': len(stats['by_type']),
        'type_labels': json.dumps(list(stats['by_type'].keys())),
        'type_data': json.dumps(list(stats['by_type'].values())),
        'size_data': json.dumps([
            stats['by_size']['small'],
            stats['by_size']['medium'],
            stats['by_size']['large']
        ])
    }
    
    # Read template and render
    with open('templates/report.html', 'r') as f:
        template = f.read()
    
    report = chevron.render(template, template_data)
    
    # Save report
    report_path = 'organization_report.html'
    with open(report_path, 'w') as f:
        f.write(report)
    
    return report_path

def main():
    # Set base output directory
    base_output_dir = os.path.join(os.path.expanduser('~'), 'Organized_Files')
    os.makedirs(base_output_dir, exist_ok=True)
    
    print("Starting file organization across all drives...")
    print(f"Files will be organized in: {base_output_dir}")
    
    # Collect all files from all drives
    print("\nCollecting files from all drives (this may take a while)...")
    all_files = collect_all_files()
    print(f"\nFound {len(all_files)} files to organize")
    
    # Organize files in different ways
    organize_by_type(all_files, base_output_dir)
    organize_by_date(all_files, base_output_dir)
    organize_by_size(all_files, base_output_dir)
    organize_by_type_and_date(all_files, base_output_dir)
    
    # Generate and print statistics
    organized_paths = [
        os.path.join(base_output_dir, path)
        for path in ['organized_by_type', 'organized_by_date', 'organized_by_size', 'organized_by_type_and_date']
    ]
    
    stats = generate_organization_stats(organized_paths)
    print_stats(stats)
    
    # Generate HTML report
    report_path = generate_html_report(stats)
    print(f"\nHTML report generated: {report_path}")
    
    # Open report in browser
    webbrowser.open(f'file://{os.path.abspath(report_path)}')
    
    print("\nAll organization tasks completed!")
    print(f"Organized files can be found in: {base_output_dir}")

if __name__ == "__main__":
    main()
