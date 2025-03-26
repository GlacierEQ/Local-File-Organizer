import shutil
from datetime import datetime
from PIL import Image
import pytesseract
import concurrent.futures
from transformers import pipeline
import os
import torch  # Import torch for GPU detection

# Import the hybrid classifier from our accelerated module
from ai_hybrid_classifier import classify_document, extract_text

BASE_DIR = "Sorting_Area"
INCOMING_DIR = os.path.join(BASE_DIR, "Incoming_Files")
SORTED_DIR = os.path.join(BASE_DIR, "Sorted_Files")

# Detect GPU
device = 0 if torch.cuda.is_available() else -1

# 🔹 Fast Model (Speed Optimized)
fast_classifier = pipeline(
    "zero-shot-classification",
    model="distilbert-base-uncased",
    device=device
)

# 🔹 Accurate Model (Higher Accuracy)
accurate_classifier = pipeline(
    "zero-shot-classification",
    model="facebook/bart-large-mnli",
    device=device
)

# 🔹 Categories for sorting
CATEGORIES = ["Legal", "Finance", "Medical", "Personal", "Work", "Technology"]

def sort_and_categorize(file_path: str) -> None:
    """Classify and move file to the appropriate folder using Hybrid AI."""
    text = extract_text(file_path)
    category = classify_document(text)
    # Generate destination folder (create folder if missing)
    dest_folder = os.path.join(SORTED_DIR, category)
    os.makedirs(dest_folder, exist_ok=True)
    # Optionally, rename file using smart conventions before moving
    new_name = os.path.basename(file_path)  # Alternatively: use smart_filename.generate_smart_filename(...)
    shutil.move(file_path, os.path.join(dest_folder, new_name))
    print(f"Sorted: {file_path} -> {dest_folder}")

def process_files():
    files = [os.path.join(INCOMING_DIR, file) for file in os.listdir(INCOMING_DIR)]
    for file in files:
        sort_and_categorize(file)

if __name__ == "__main__":
    process_files()
