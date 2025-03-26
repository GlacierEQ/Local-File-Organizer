import os
import shutil
import datetime
import string
from scan_window import ScanWindow


def get_all_drives():
    """Get all available drives on Windows."""
    drives = []
    for letter in string.ascii_uppercase:
        drive = f"{letter}:\\"
        if os.path.exists(drive):
            drives.append(drive)
    return drives

def get_file_type_folder(filename):
    """Determine the folder based on file extension."""
    ext = os.path.splitext(filename)[1].lower()
    
    # Image files
    if ext in ['.jpg', '.jpeg', '.png', '.gif', '.bmp']:
        return 'Images'
    
    # Document files
    if ext in ['.doc', '.docx', '.pdf', '.txt', '.md']:
        return 'Documents'
    
    # Audio files
    if ext in ['.mp3', '.wav', '.flac', '.m4a']:
        return 'Audio'
    
    # Video files
    if ext in ['.mp4', '.avi', '.mkv', '.mov']:
        return 'Video'
    
    # Archive files
    if ext in ['.zip', '.rar', '.7z']:
        return 'Archives'
    
    # Spreadsheet files
    if ext in ['.xls', '.xlsx', '.csv']:
        return 'Spreadsheets'
    
    # Presentation files
    if ext in ['.ppt', '.pptx']:
        return 'Presentations'
    
    # Program files
    if ext in ['.exe', '.msi']:
        return 'Programs'
    
    return 'Other'

def get_size_category(file_path):
    """Get size category of file."""
    size = os.path.getsize(file_path)
    if size < 1024 * 1024:  # < 1MB
        return 'Small'
    elif size < 10 * 1024 * 1024:  # < 10MB
        return 'Medium'
    else:  # >= 10MB
        return 'Large'

def backup_files(file_path, backup_dir):
    """Create a backup of the specified file."""
    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)
    shutil.copy(file_path, backup_dir)

def organize_files():
    """Organize files from all drives."""
    
    print("\nChoose operation:")
    print("1. Organize files")
    print("2. Scan files")



def get_all_drives():
    """Get all available drives on Windows."""
    drives = []
    for letter in string.ascii_uppercase:
        drive = f"{letter}:\\"
        if os.path.exists(drive):
            drives.append(drive)
    return drives

def get_file_type_folder(filename):
    """Determine the folder based on file extension."""
    ext = os.path.splitext(filename)[1].lower()
    
    # Image files
    if ext in ['.jpg', '.jpeg', '.png', '.gif', '.bmp']:
        return 'Images'
    
    # Document files
    if ext in ['.doc', '.docx', '.pdf', '.txt', '.md']:
        return 'Documents'
    
    # Audio files
    if ext in ['.mp3', '.wav', '.flac', '.m4a']:
        return 'Audio'
    
    # Video files
    if ext in ['.mp4', '.avi', '.mkv', '.mov']:
        return 'Video'
    
    # Archive files
    if ext in ['.zip', '.rar', '.7z']:
        return 'Archives'
    
    # Spreadsheet files
    if ext in ['.xls', '.xlsx', '.csv']:
        return 'Spreadsheets'
    
    # Presentation files
    if ext in ['.ppt', '.pptx']:
        return 'Presentations'
    
    # Program files
    if ext in ['.exe', '.msi']:
        return 'Programs'
    
    return 'Other'

def get_size_category(file_path):
    """Get size category of file."""
    size = os.path.getsize(file_path)
    if size < 1024 * 1024:  # < 1MB
        return 'Small'
    elif size < 10 * 1024 * 1024:  # < 10MB
        return 'Medium'
    else:  # >= 10MB
        return 'Large'

def backup_files(file_path, backup_dir):
    """Create a backup of the specified file."""
    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)
    shutil.copy(file_path, backup_dir)

def organize_files(exhaustive=False):
    """Organize files from all drives."""

    # System directories and files to exclude
    exclude_dirs = {
        'Windows', 'Program Files', 'Program Files (x86)', 
        'ProgramData', '$Recycle.Bin', 'System Volume Information',
    'Recovery', 'Config.Msi'
    }
    
    exclude_files = {
        'pagefile.sys', 'hiberfil.sys', 'swapfile.sys'
    }
    
    # Create base directory in user's home
    base_dir = os.path.join(os.path.expanduser('~'), 'Organized_Files')
    
    print("WARNING: This script will MOVE your files to organize them.")
    print(f"Files will be organized in: {base_dir}")
    input("Press Enter to continue or Ctrl+C to cancel...")
    
    # Choose organization method
    print("\nChoose organization method:")
    print("1. By Type (images, documents, videos, etc.)")
    print("2. By Size (small, medium, large)")
    choice = input("Enter your choice (1-2) or 'scan' for exhaustive scan: ")

    
    if choice not in ['1', '2']:
        print("Invalid choice. Using organization by type as default.")
        choice = '1'
    
    # Create organization directory
    os.makedirs(base_dir, exist_ok=True)
    
    # Get all drives
    drives = get_all_drives()
    print("\nScanning drives:", ', '.join(drives))
    
    # Track statistics
    total_files = 0
    organized_files = 0
    errors = []
    
    if choice.lower() == 'scan':
        from scan_window import ScanWindow
        import tkinter as tk
        root = tk.Tk()
        app = ScanWindow(root)
        root.mainloop()
        return


    for drive in drives: 

        print(f"\nScanning drive {drive}")
        try:
            for root, dirs, files in os.walk(drive, topdown=True):
                # Remove excluded directories
                dirs[:] = [d for d in dirs if d not in exclude_dirs]
                
                for file in files:
                    if file not in exclude_files:
                        try:
                            total_files += 1
                            file_path = os.path.join(root, file)
                            
                            # Skip if we can't access the file
                            if not os.access(file_path, os.R_OK | os.W_OK):
                                continue
                            
                            # Determine destination folder
                            if choice == '1':
                                category = get_file_type_folder(file)
                            else:
                                category = get_size_category(file_path)
                            
                            dest_dir = os.path.join(base_dir, category)
                            os.makedirs(dest_dir, exist_ok=True)
                            
                            # Create destination path
                            dest_path = os.path.join(dest_dir, file)
                            
                            # If file already exists, add number to filename
                            base, ext = os.path.splitext(file)
                            counter = 1
                            while os.path.exists(dest_path):
                                dest_path = os.path.join(dest_dir, f"{base}_{counter}{ext}")
                                counter += 1
                            
                            # Move the file or log the result

                            shutil.move(file_path, dest_path)
                            organized_files += 1
                            
                            # Print progress
                            if organized_files % 100 == 0:
                                print(f"Organized {organized_files} files...")
                            
                        except (PermissionError, OSError) as e:
                            errors.append(f"Error with {file_path}: {str(e)}")
                            continue
                        
        except (PermissionError, OSError) as e:
            print(f"Error accessing {drive}: {str(e)}")
            continue
    
    # Print summary
    print("\n=== Organization Complete ===")
    print(f"Total files found: {total_files}")
    print(f"Files organized: {organized_files}")
    print(f"Errors encountered: {len(errors)}")
    
    # Print errors if any
    if errors:
        print("\nErrors:")
        for error in errors[:10]:  # Show first 10 errors
            print(error)
        if len(errors) > 10:
            print(f"...and {len(errors) - 10} more errors")
    
    print(f"\nFiles have been organized in: {base_dir}")

if __name__ == "__main__":
    organize_files()
