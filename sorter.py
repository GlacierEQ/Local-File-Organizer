import os
import shutil
from pathlib import Path
from pytesseract import image_to_string
from PIL import Image
from ai.document_classifier import classify_document

# ...existing code if any...

def extract_text(file_path: str) -> str:
    ext = Path(file_path).suffix.lower()
    if ext in ['.jpg', '.jpeg', '.png']:
        try:
            img = Image.open(file_path)
            return image_to_string(img)
        except Exception as e:
            print(f"OCR error: {e}")
            return ""
    # For PDFs etc, add PDF extraction option
    return ""

def sort_document(file_path: str) -> None:
    text = extract_text(file_path)
    if text:
        # Use AI to decide category (default label if confidence too low)
        label = classify_document(text)
    else:
        label = "Uncategorized"
    
    dest_dir = Path("sorted_documents") / label
    dest_dir.mkdir(parents=True, exist_ok=True)
    shutil.move(file_path, dest_dir / Path(file_path).name)
    print(f"Moved {file_path} to {dest_dir}")

def main():
    # Sort all documents in the "documents" directory
    source = Path("documents")
    for file in source.glob("*"):
        if file.is_file():
            sort_document(str(file))

if __name__ == "__main__":
    main()
