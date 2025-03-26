from PIL import Image
import PyPDF2
import os
import shutil

BASE_DIR = "Sorting_Area"
RECOVERED_DIR = os.path.join(BASE_DIR, "Recovered_Files")

def check_image_integrity(file_path):
    """Check if the image file is valid."""
    try:
        with Image.open(file_path) as img:
            img.verify()  # Verify the image
        return True
    except Exception as e:
        print(f"Corrupted image file: {file_path} - {e}")
        return False

def check_pdf_integrity(file_path):
    """Check if the PDF file is valid."""
    try:
        with open(file_path, "rb") as f:
            reader = PyPDF2.PdfReader(f)
            if len(reader.pages) == 0:
                raise Exception("PDF is empty")
        return True
    except Exception as e:
        print(f"Corrupted PDF file: {file_path} - {e}")
        return False

def scan_for_repairs():
    """Scan the Recovered_Files directory for files that need repairs."""
    print(f"🔍 Scanning '{RECOVERED_DIR}' for files that need repairs...")
    
    if not os.path.exists(RECOVERED_DIR):
        print("No recovered files found.")
        return

    files = os.listdir(RECOVERED_DIR)
    if not files:
        print("No files to repair.")
        return

    for file in files:
        file_path = os.path.join(RECOVERED_DIR, file)
        if file.lower().endswith(('.png', '.jpg', '.jpeg')):
            if not check_image_integrity(file_path):
                shutil.move(file_path, os.path.join(BASE_DIR, "Recovered_Files", file))
        elif file.lower().endswith('.pdf'):
            if not check_pdf_integrity(file_path):
                shutil.move(file_path, os.path.join(BASE_DIR, "Recovered_Files", file))
