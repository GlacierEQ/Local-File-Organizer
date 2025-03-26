import os
from organize_files import organize_files
from file_utils import read_file_data

def test_organize_files():
    print("Testing file organization...")
    result = organize_files()
    # Add assertions to verify the expected outcome
    assert result is not None, "Organize files function returned None"
    print("File organization test passed.")

def test_read_file_data():
    print("Testing file reading...")
    test_files = [
        "C:\\Users\\casey\\OneDrive\\Documents\\GitHub\\Local-File-Organizer\\sample_data\\legal_documents\\case_law_example.txt",  # Sample text file
        "C:\\Users\\casey\\OneDrive\\Documents\\GitHub\\Local-File-Organizer\\sample_data\\legal_documents\\docket_entry_example.txt"  # Another sample text file
    ]
    
    for file in test_files:
        try:
            content = read_file_data(file)
            if content is not None:
                print(f"Content of {file}:\n{content[:100]}...")  # Print first 100 characters
            else:
                print(f"Skipped reading {file}.")
        except Exception as e:
            print(f"Error reading {file}: {e}")

if __name__ == "__main__":
    test_organize_files()
    test_read_file_data()
