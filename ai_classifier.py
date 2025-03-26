from transformers import pipeline

# Load the zero-shot classification model.
classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

def classify_document(text: str) -> str:
    """
    Classify document using OCR text and contextual keywords.
    Uses an expanded candidate list.
    """
    candidate_labels = [
        "Legal", "Finance", "Medical", "Personal", "Work", 
        "Education", "Technology", "Photography", "Marketing"
    ]
    result = classifier(text, candidate_labels=candidate_labels)
    return result['labels'][0] if result['scores'][0] > 0.5 else "Uncategorized"

# ...existing code can be integrated if needed...
