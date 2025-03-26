import os
import random
import string
from PIL import Image
import numpy as np

def create_random_file(directory, file_type, size_kb):
    filename = ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))
    filepath = os.path.join(directory, f"{filename}.{file_type}")
    
    if file_type in ['txt', 'md', 'docx']:
        with open(filepath, 'w') as f:
            f.write(''.join(random.choices(string.ascii_letters + string.whitespace, k=size_kb * 1024)))
    elif file_type in ['jpg', 'png']:
        img_size = int((size_kb * 1024) ** 0.5)
        img = Image.fromarray(np.random.randint(0, 256, (img_size, img_size, 3), dtype=np.uint8))
        img.save(filepath)
    elif file_type == 'pdf':
        # For simplicity, we'll create a text file with .pdf extension
        with open(filepath, 'w') as f:
            f.write(''.join(random.choices(string.ascii_letters + string.whitespace, k=size_kb * 1024)))

def create_test_dataset(base_dir, num_files=100, max_size_kb=1024):
    os.makedirs(base_dir, exist_ok=True)
    file_types = ['txt', 'md', 'docx', 'jpg', 'png', 'pdf']
    
    for _ in range(num_files):
        file_type = random.choice(file_types)
        size_kb = random.randint(1, max_size_kb)
        create_random_file(base_dir, file_type, size_kb)

    print(f"Created {num_files} random files in {base_dir}")

if __name__ == "__main__":
    test_dir = "test_dataset"
    create_test_dataset(test_dir, num_files=1000, max_size_kb=2048)
    
    # Import and run main_optimized
    import main_optimized
    
    # Redirect input to use our test directory
    import io
    import sys
    
    sys.stdin = io.StringIO(f"{test_dir}\n\nn\n1\ny\nn\n")
    main_optimized.main()
    
    print("Test completed. Please check the organized files in the output directory.")
