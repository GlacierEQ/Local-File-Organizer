import concurrent.futures
from transformers import pipeline
import pytesseract
from PIL import Image
import torch

# Set device: use GPU if available, otherwise CPU (-1)
device = 0 if torch.cuda.is_available() else -1

# Initialize fast and accurate models with GPU acceleration.
fast_classifier = pipeline(
    "zero-shot-classification",
    model="distilbert-base-uncased",
    device=device,
    batch_size=8
)
accurate_classifier = pipeline(
    "zero-shot-classification",
    model="facebook/bart-large-mnli",
    device=device,
    batch_size=8
)

# Candidate categories for classification
CATEGORIES = ["Legal", "Finance", "Medical", "Personal", "Work", "Technology"]

def extract_text(file_path: str) -> str:
    """Extracts text from an image using OCR."""
    try:
        return pytesseract.image_to_string(Image.open(file_path))
    except Exception:
        return ""

def fast_classification(text: str) -> (str, float):
    """Runs fast AI model and returns (category, confidence score)."""
    result = fast_classifier(text, candidate_labels=CATEGORIES)
    return result["labels"][0], result["scores"][0]

def accurate_classification(text: str) -> str:
    """Runs accurate AI model (with no gradients) and returns category."""
    with torch.no_grad():
        result = accurate_classifier(text, candidate_labels=CATEGORIES)
    return result["labels"][0]

def classify_document(text: str) -> str:
    """
    Hybrid classification:
      - Use fast model first.
      - If confidence < 0.6, fallback to accurate model.
    """
    category, confidence = fast_classification(text)
    if confidence < 0.6:
        return accurate_classification(text)
    return category

def process_file(file_path: str) -> None:
    """Extracts text and classifies a file using the hybrid approach."""
    text = extract_text(file_path)
    category = classify_document(text)
    print(f"📂 File: {file_path} → Category: {category}")

def batch_process_files(file_list: list) -> None:
    """Processes multiple files in parallel using ThreadPoolExecutor."""
    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(process_file, file_list)

if __name__ == "__main__":
    # Replace with actual list of files to process.
    files = ["path/to/file1.png", "path/to/file2.jpg"]
    batch_process_files(files)
