import os
from datetime import datetime

def generate_smart_filename(original_name: str, category: str, text_snippet: str) -> str:
    """
    Generate a human-readable filename using the category, a short text snippet (from OCR),
    and a timestamp. The snippet is sanitized to remove spaces.
    """
    timestamp = datetime.now().strftime("%Y-%m-%d_%H%M%S")
    # Use first 20 characters of snippet without spaces
    short_text = text_snippet[:20].replace(" ", "_")
    ext = os.path.splitext(original_name)[1]
    return f"{category}_{short_text}_{timestamp}{ext}"
