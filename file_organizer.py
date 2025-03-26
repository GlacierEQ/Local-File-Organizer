import logging
import json
import hashlib
from file_classifier import classifier  # Import the classifier

file_hashes = {}

def get_file_hash(file_path: str) -> str:
    """Calculate the hash of a file."""
    hasher = hashlib.sha256()
    with open(file_path, "rb") as f:
        while chunk := f.read(8192):
            hasher.update(chunk)
    return hasher.hexdigest()

def is_duplicate(file_path: str) -> bool:
    file_hash = get_file_hash(file_path)
    if file_hash is None:
        return False  # Treat as new if hash cannot be calculated
    if file_hash in file_hashes:
        logging.info(f"Duplicate detected for {file_path}")
        return True
    file_hashes[file_hash] = file_path
    return False

def load_sorting_rules(config_path="config.json") -> dict:
    with open(config_path, "r") as f:
        return json.load(f).get("sorting_rules", {})

def classify_document(text):
    """Classifies document using OCR text and configurable keywords."""
    rules = load_sorting_rules()
    for category, keywords in rules.items():
        for kw in keywords:
            if kw.lower() in text.lower():
                return category
    # Fallback to AI zero-shot classification if no rule applies
    default_categories = ["Legal", "Finance", "Medical", "Personal", "Work", "Misc"]
    response = classifier(text, candidate_labels=default_categories)
    return response['labels'][0] if response['scores'][0] > 0.5 else "Uncategorized"

# Other existing code...
