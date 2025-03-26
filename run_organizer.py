import os
import shutil
import json
import datetime
import hashlib
import webbrowser
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
    
    return clean_name + ext.lower()

def clean_directory(directory):
    """Remove a directory and its contents if it exists."""
    if os.path.exists(directory):
        shutil.rmtree(directory)

def organize_by_size():
    """Organize files by size category with improved names"""
    input_path = "sample_data"
    output_path = os.path.join(os.path.dirname(input_path), 'organized_by_size')
    
    # Clean existing directory
    clean_directory(output_path)
    
    # Create output directory
    os.makedirs(output_path, exist_ok=True)
    
    print("\nOrganizing by size...")
    print(f"Input directory: {input_path}")
    print(f"Output directory: {output_path}")
    
    # Collect file paths
    file_paths = collect_file_paths(input_path)
    print(f"Found {len(file_paths)} files to organize")
    
    # Create operations based on file size
    operations = []
    for file_path in file_paths:
        size_category = get_file_size_category(file_path)
        dest_dir = os.path.join(output_path, f"{size_category}_files")
        improved_name = improve_filename(file_path)
        new_dest = os.path.join(dest_dir, improved_name)
        operations.append({
            'source': file_path,
            'destination': new_dest,
            'link_type': 'hardlink'
        })
    
    print(f"Generated {len(operations)} operations")
    
    # Execute operations
    execute_operations(operations, dry_run=False, silent=False)
    
    print("Size-based organization complete!")

def organize_by_type():
    """Organize files by type with improved names"""
    input_path = "sample_data"
    output_path = os.path.join(os.path.dirname(input_path), 'organized_by_type')
    
    # Clean existing directory
    clean_directory(output_path)
    
    # Create output directory
    os.makedirs(output_path, exist_ok=True)
    
    print("\nOrganizing by type...")
    print(f"Input directory: {input_path}")
    print(f"Output directory: {output_path}")
    
    # Collect file paths
    file_paths = collect_file_paths(input_path)
    print(f"Found {len(file_paths)} files to organize")
    
    # Process files by type
    operations = process_files_by_type(file_paths, output_path)
    
    # Improve filenames in operations
    improved_operations = []
    for op in operations:
        dest_dir = os.path.dirname(op['destination'])
        improved_name = improve_filename(op['source'])
        new_dest = os.path.join(dest_dir, improved_name)
        improved_operations.append({
            'source': op['source'],
            'destination': new_dest,
            'link_type': op['link_type']
        })
    
    print(f"Generated {len(improved_operations)} operations")
    
    # Execute operations
    execute_operations(improved_operations, dry_run=False, silent=False)
    
    print("Type-based organization complete!")

def organize_by_date():
    """Organize files by date with improved names"""
    input_path = "sample_data"
    output_path = os.path.join(os.path.dirname(input_path), 'organized_by_date')
    
    # Clean existing directory
    clean_directory(output_path)
    
    # Create output directory
    os.makedirs(output_path, exist_ok=True)
    
    print("\nOrganizing by date...")
    print(f"Input directory: {input_path}")
    print(f"Output directory: {output_path}")
    
    # Collect file paths
    file_paths = collect_file_paths(input_path)
    print(f"Found {len(file_paths)} files to organize")
    
    # Process files by date
    operations = process_files_by_date(file_paths, output_path)
    
    # Improve filenames in operations
    improved_operations = []
    for op in operations:
        dest_dir = os.path.dirname(op['destination'])
        improved_name = improve_filename(op['source'])
        new_dest = os.path.join(dest_dir, improved_name)
        improved_operations.append({
            'source': op['source'],
            'destination': new_dest,
            'link_type': op['link_type']
        })
    
    print(f"Generated {len(improved_operations)} operations")
    
    # Execute operations
    execute_operations(improved_operations, dry_run=False, silent=False)
    
    print("Date-based organization complete!")

def organize_by_type_and_date():
    """Organize files by type and date with improved names"""
    input_path = "sample_data"
    output_path = os.path.join(os.path.dirname(input_path), 'organized_by_type_and_date')
    
    # Clean existing directory
    clean_directory(output_path)
    
    # Create output directory
    os.makedirs(output_path, exist_ok=True)
    
    print("\nOrganizing by type and date...")
    print(f"Input directory: {input_path}")
    print(f"Output directory: {output_path}")
    
    # Collect file paths
    file_paths = collect_file_paths(input_path)
    print(f"Found {len(file_paths)} files to organize")
    
    # Process files by type first
    type_operations = process_files_by_type(file_paths, output_path)
    
    # Then organize by date within each type
    final_operations = []
    for op in type_operations:
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
            'link_type': 'hardlink'
        })
    
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
    
    return stats

def generate_file_hash(file_path):
    """Generate a hash of file contents for change detection."""
    import hashlib
    with open(file_path, 'rb') as f:
        return hashlib.md5(f.read()).hexdigest()

def save_file_state(base_paths, state_file='file_state.json'):
    """Save current state of all organized files."""
    state = {}
    for base_path in base_paths:
        for root, _, files in os.walk(base_path):
            for file in files:
                file_path = os.path.join(root, file)
                state[file_path] = {
                    'hash': generate_file_hash(file_path),
                    'size': os.path.getsize(file_path),
                    'modified': os.path.getmtime(file_path)
                }
    
    with open(state_file, 'w') as f:
        json.dump(state, f, indent=2)
    return state

def check_file_changes(base_paths, old_state, state_file='file_state.json'):
    """Check for changes in organized files."""
    current_state = {}
    changes = {
        'new_files': [],
        'modified_files': [],
        'deleted_files': [],
        'moved_files': []
    }
    
    # Build current state and detect changes
    for base_path in base_paths:
        for root, _, files in os.walk(base_path):
            for file in files:
                file_path = os.path.join(root, file)
                current_state[file_path] = {
                    'hash': generate_file_hash(file_path),
                    'size': os.path.getsize(file_path),
                    'modified': os.path.getmtime(file_path)
                }
                
                if file_path not in old_state:
                    changes['new_files'].append(file_path)
                elif current_state[file_path]['hash'] != old_state[file_path]['hash']:
                    changes['modified_files'].append(file_path)
    
    # Check for deleted and moved files
    for old_path in old_state:
        if old_path not in current_state:
            # Check if file was moved by looking for matching hash
            moved = False
            old_hash = old_state[old_path]['hash']
            for new_path, new_data in current_state.items():
                if new_data['hash'] == old_hash and new_path not in changes['new_files']:
                    changes['moved_files'].append((old_path, new_path))
                    moved = True
                    break
            if not moved:
                changes['deleted_files'].append(old_path)
    
    # Save new state
    save_file_state(base_paths, state_file)
    
    return changes

def print_stats(stats):
    """Print organization statistics in a nice format."""
    print("\n=== File Organization Statistics ===")
    print(f"\nTotal Files: {stats['total_files']}")
    print(f"Total Size: {stats['total_size'] / (1024*1024):.2f} MB")
    
    print("\nFiles by Type:")
    for ext, count in sorted(stats['by_type'].items(), key=lambda x: x[1], reverse=True):
        print(f"  {ext or 'no extension'}: {count}")
    
    print("\nFiles by Size:")
    for category, count in stats['by_size'].items():
        print(f"  {category}: {count}")
    
    print("\nFiles by Month:")
    for date, count in sorted(stats['by_date'].items(), reverse=True):
        print(f"  {date}: {count}")

def print_changes(changes):
    """Print detected changes in organized files."""
    print("\n=== File Change Report ===")
    
    if changes['new_files']:
        print("\nNew Files:")
        for file in changes['new_files']:
            print(f"  + {file}")
    
    if changes['modified_files']:
        print("\nModified Files:")
        for file in changes['modified_files']:
            print(f"  ~ {file}")
    
    if changes['deleted_files']:
        print("\nDeleted Files:")
        for file in changes['deleted_files']:
            print(f"  - {file}")
    
    if changes['moved_files']:
        print("\nMoved Files:")
        for old, new in changes['moved_files']:
            print(f"  > {old} -> {new}")
    
    if not any(changes.values()):
        print("\nNo changes detected since last organization.")

def generate_html_report(stats, changes=None):
    """Generate an HTML report with charts and statistics."""
    # Prepare data for the template
    template_data = {
        'total_files': stats['total_files'],
        'total_size_mb': f"{stats['total_size'] / (1024*1024):.1f}",
        'total_types': len(stats['by_type']),
        'type_labels': json.dumps(list(stats['by_type'].keys())),
        'type_data': json.dumps(list(stats['by_type'].values())),
        'size_data': json.dumps([
            stats['by_size']['small'],
            stats['by_size']['medium'],
            stats['by_size']['large']
        ])
    }
    
    if changes:
        template_data['changes'] = {
            'new_files': changes['new_files'],
            'modified_files': changes['modified_files'],
            'deleted_files': changes['deleted_files'],
            'moved_files': [{'from': old, 'to': new} for old, new in changes['moved_files']]
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
    # Initialize path manager
    path_manager = PathManager()
    path_manager.update_paths()
    print("Path configuration updated.")
    print(path_manager.generate_report())
    
    print("\nStarting file organization...")
    organize_by_type()
    organize_by_date()
    organize_by_size()
    organize_by_type_and_date()
    
    # Get monitored paths from path manager
    organized_paths = [
        os.path.join(os.path.dirname(path_manager.get_path('sample_data', 'input_paths')), 
                    path_manager.get_path(path, 'output_paths'))
        for path in ['organized_by_type', 'organized_by_date', 'organized_by_size', 'organized_by_type_and_date']
    ]
    
    # Generate and print statistics
    stats = generate_organization_stats(organized_paths)
    print_stats(stats)
    
    # Check for changes if previous state exists
    state_file = 'file_state.json'
    changes = None
    if os.path.exists(state_file):
        with open(state_file, 'r') as f:
            old_state = json.load(f)
        changes = check_file_changes(organized_paths, old_state, state_file)
        print_changes(changes)
    else:
        # First run, just save initial state
        save_file_state(organized_paths, state_file)
        print("\nInitial file state saved. Changes will be tracked on next run.")
    
    # Generate HTML report
    report_path = generate_html_report(stats, changes)
    print(f"\nHTML report generated: {report_path}")
    
    # Open report in browser
    webbrowser.open(f'file://{os.path.abspath(report_path)}')
    
    print("\nAll organization tasks completed!")

if __name__ == "__main__":
    main()
