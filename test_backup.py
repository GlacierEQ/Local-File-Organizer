import os
import shutil

def test_backup():
    original_file = "test_file.txt"
    backup_dir = "backup"
    
    # Create a test file
    with open(original_file, "w") as f:
        f.write("This is a test file for backup.")

    # Backup function
    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)
    
    shutil.copy(original_file, backup_dir)

    # Check if the backup was successful
    assert os.path.exists(os.path.join(backup_dir, original_file)), "Backup failed!"

    # Clean up
    os.remove(original_file)
    os.remove(os.path.join(backup_dir, original_file))
    os.rmdir(backup_dir)

if __name__ == "__main__":
    test_backup()
    print("Backup test completed successfully.")
