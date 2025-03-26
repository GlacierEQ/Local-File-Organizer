import os
import json
import torch
from PIL import Image
from transformers import AutoImageProcessor, AutoModelForImageClassification
import pytesseract
from pdf2image import convert_from_path
import docx
import magic
import spacy
from pathlib import Path

def setup_image_model():
    """Setup the image recognition model."""
    processor = AutoImageProcessor.from_pretrained("microsoft/resnet-50")
    model = AutoModelForImageClassification.from_pretrained("microsoft/resnet-50")
    return processor, model

def analyze_image(image_path, processor, model):
    """Analyze image content and return descriptive name."""
    try:
        image = Image.open(image_path)
        inputs = processor(image, return_tensors="pt")
        outputs = model(**inputs)
        predicted_label = outputs.logits.argmax(-1).item()
        return model.config.id2label[predicted_label]
    except Exception as e:
        print(f"Error analyzing image {image_path}: {str(e)}")
        return None

def analyze_document(doc_path):
    """Analyze document content and return descriptive name."""
    try:
        mime = magic.Magic(mime=True)
        file_type = mime.from_file(doc_path)
        
        if file_type == "application/pdf":
            # Convert PDF to images and extract text
            pages = convert_from_path(doc_path, 500)
            text = ""
            for page in pages:
                text += pytesseract.image_to_string(page)
        elif file_type == "application/msword" or file_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            # Extract text from Word documents
            doc = docx.Document(doc_path)
            text = " ".join([paragraph.text for paragraph in doc.paragraphs])
        else:
            # Try to read as text file
            with open(doc_path, 'r', encoding='utf-8') as f:
                text = f.read()
        
        # Use spaCy for keyword extraction
        nlp = spacy.load("en_core_web_sm")
        doc = nlp(text[:1000])  # Analyze first 1000 characters
        
        # Extract key phrases
        key_phrases = []
        for ent in doc.ents:
            if ent.label_ in ['ORG', 'PERSON', 'GPE', 'EVENT']:
                key_phrases.append(ent.text)
        
        if key_phrases:
            return "_".join(key_phrases[:3])  # Use first 3 key phrases
        else:
            # Fallback to most common nouns
            nouns = [token.text for token in doc if token.pos_ == 'NOUN']
            return "_".join(nouns[:3]) if nouns else None
            
    except Exception as e:
        print(f"Error analyzing document {doc_path}: {str(e)}")
        return None

def smart_rename_file(file_path, processor=None, model=None):
    """Generate a smart name based on file content."""
    try:
        mime = magic.Magic(mime=True)
        file_type = mime.from_file(file_path)
        
        # Get original extension
        ext = os.path.splitext(file_path)[1].lower()
        
        # Initialize descriptive name
        descriptive_name = None
        
        # Images
        if file_type.startswith('image/'):
            if processor and model:
                descriptive_name = analyze_image(file_path, processor, model)
        
        # Documents
        elif file_type.startswith(('application/', 'text/')):
            descriptive_name = analyze_document(file_path)
        
        # If we got a descriptive name, use it
        if descriptive_name:
            # Clean the name
            descriptive_name = "".join(c if c.isalnum() or c in ['-', '_'] else '_' for c in descriptive_name)
            descriptive_name = descriptive_name.lower()
            
            # Add type prefix
            if file_type.startswith('image/'):
                return f"image_{descriptive_name}{ext}"
            elif file_type.startswith(('application/pdf', 'application/msword')):
                return f"document_{descriptive_name}{ext}"
            elif file_type.startswith('text/'):
                return f"text_{descriptive_name}{ext}"
            else:
                return f"file_{descriptive_name}{ext}"
        
        return None
    except Exception as e:
        print(f"Error processing {file_path}: {str(e)}")
        return None

def process_directory(directory):
    """Process all files in a directory with smart renaming."""
    # Setup image recognition model
    processor, model = setup_image_model()
    
    # Walk through directory
    for root, _, files in os.walk(directory):
        for filename in files:
            file_path = os.path.join(root, filename)
            
            # Get smart name
            new_name = smart_rename_file(file_path, processor, model)
            
            if new_name:
                # Create new path
                new_path = os.path.join(root, new_name)
                
                # Rename file
                try:
                    os.rename(file_path, new_path)
                    print(f"Renamed: {filename} -> {new_name}")
                except Exception as e:
                    print(f"Error renaming {filename}: {str(e)}")

if __name__ == "__main__":
    # Directory to process
    target_dir = os.path.join(os.path.expanduser('~'), 'Organized_Files')
    
    # Process the directory
    process_directory(target_dir)
