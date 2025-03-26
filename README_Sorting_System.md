# Professional File Organization & Hierarchical Sorting System

## Goal
Design a robust, professional-grade file sorting, renaming, and dependency-repair system within a designated workspace folder. In this system, the user manually places unsorted files into a defined folder (Incoming_Files), and the system operates solely within that workspace to:
- **Sort & Categorize** files (images, videos, documents, etc.)
- **Repair & Restore** damaged or corrupt files when possible
- **Regenerate Paths & Dependencies** for broken references
- **Rename & Standardize** file names with a consistent, traceable scheme
- **Maintain Logs & Allow User Overrides** for enhanced control and auditability

---

## System Design & Key Features

### 1. Dedicated Workspace Folder
- **Workspace Boundary:**  
  The entire system operates strictly within a single folder (`Sorting_Area`), ensuring that no files outside the workspace are affected.
  
- **Folder Structure:**
  ```
  Sorting_Area/
  ├── Incoming_Files/      # User places unsorted files here
  ├── Sorted_Files/        # Files sorted into categories
  │   ├── Documents/
  │   ├── Images/
  │   ├── Videos/
  │   ├── PDFs/
  │   └── Uncategorized/
  ├── Logs/                # Logs all operations
  ├── Backups/             # Stores original files before modifications
  ├── Dependencies/        # Metadata & dependency tracking
  └── Recovered_Files/     # Restores & repairs broken files
  ```
- **Operational Rule:**  
  Only files within `Incoming_Files/` are processed. Any missing dependencies are either restored from Backups or reconstructed and stored inside `Dependencies/`.

### 2. Smart File Renaming & Standardization
- **Naming Convention:**  
  Files are systematically renamed using the pattern:
  ```
  [Category]_[YYYY-MM-DD]_[Timestamp]_[Unique-ID].[ext]
  ```
- **Examples:**  
  - `Legal_2025-02-22_183245_ABC123.pdf`
  - `Images_2025-02-22_183300_XYZ789.jpg`
  
- **Benefits:**  
  This approach prevents duplicate filenames, maintains a consistent and professional naming scheme, and ensures files are easily traceable.

### 3. AI-Driven Categorization & Sorting
- **Documents & Images:**  
  - **OCR Extraction:** Uses Tesseract (with PIL for image management) to extract text from images and PDFs.
  - **AI Classification:** Applies a zero-shot NLP model (e.g., using transformers) to categorize files based on extracted text. If extraction fails, files are defaulted to `Uncategorized/`.
  
- **Videos & Audio Files:**  
  - **Speech-to-Text:** Employs Whisper or DeepSpeech models to transcribe audio content.
  - **Metadata Analysis:** Examines attributes (resolution, duration, codec, etc.) to assign a relevant category.
  
- **Sorting Rule:**  
  Files are moved based on detected types:
  - `.jpg, .png, .jpeg` → `Images/`
  - `.pdf, .docx, .txt` → `Documents/`
  - `.mp4, .avi, .mkv` → `Videos/`

### 4. File Repair & Restoration
- **Repair Mechanisms:**  
  The system integrates external tools to repair damaged files:
  - **FFmpeg:** Repairs broken video/audio files.
  - **ExifTool:** Recovers lost metadata in images.
  - **PDFTK/PyMuPDF:** Repairs corrupt PDF files.
  - **Additional Libraries (e.g., docx2txt, xlrd):** Extract residual content from broken documents.
- **Output:**  
  Successfully repaired files are stored in `Recovered_Files/`.

### 5. Dependency Regeneration & Path Repair
- **Scanning:**  
  The system scans for missing dependencies or broken internal links in files (such as PDFs, Word documents, Excel spreadsheets, or code files).
- **Reconstruction & Indexing:**  
  It regenerates missing references, stores metadata in the `Dependencies/` folder, and produces an `index.json` that maps original file paths to their new, correct locations.

### 6. Logging & Override System
- **Logging:**  
  All operations (sorting, renaming, repairs, dependency regeneration) are logged in the `Logs/` folder.
- **User Overrides:**  
  A configuration file (e.g., `config.json`) allows manual settings for:
  - Custom sorting rules (e.g., "Invoices always go to Finance")
  - File exclusions (to ignore specific files)
  - Custom renaming formats

---

## Execution Plan

### Step 1: Create the Workspace
Run the following command in your terminal:
```bash
mkdir -p Sorting_Area/{Incoming_Files,Sorted_Files/{Documents,Images,Videos,PDFs,Uncategorized},Logs,Backups,Dependencies,Recovered_Files}
```

### Step 2: Implement AI Categorization
Use the following Python snippet for OCR and classification:
```python
# ...existing code for AI Categorization...
from transformers import pipeline
import pytesseract
from PIL import Image

classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

def extract_text(image_path):
    return pytesseract.image_to_string(Image.open(image_path))

def classify_document(text):
    categories = ["Legal", "Finance", "Medical", "Personal", "Work", "Misc"]
    result = classifier(text, candidate_labels=categories)
    return result['labels'][0] if result['scores'][0] > 0.5 else "Uncategorized"
```

### Step 3: Implement Smart File Sorting
Automate file renaming and moving:
```python
# ...existing file sorting code...
import shutil
import os
from datetime import datetime

BASE_DIR = "Sorting_Area"
INCOMING = os.path.join(BASE_DIR, "Incoming_Files")
SORTED = os.path.join(BASE_DIR, "Sorted_Files")

def rename_file(original_name, category):
    timestamp = datetime.now().strftime("%Y-%m-%d_%H%M%S")
    unique_id = os.path.splitext(os.path.basename(original_name))[0]
    extension = os.path.splitext(original_name)[1]
    return f"{category}_{timestamp}_{unique_id}{extension}"

def move_file(file_path):
    category = classify_document(extract_text(file_path))
    new_name = rename_file(file_path, category)
    dest_folder = os.path.join(SORTED, category)
    os.makedirs(dest_folder, exist_ok=True)
    shutil.move(file_path, os.path.join(dest_folder, new_name))

for file in os.listdir(INCOMING):
    move_file(os.path.join(INCOMING, file))
```

### Step 4: Implement File Repair & Restoration
Integrate external tools to repair files:
```python
# ...existing file repair code...
import subprocess
import os

def repair_video(file_path):
    repaired_path = os.path.join("Sorting_Area/Recovered_Files", os.path.basename(file_path))
    subprocess.run(f"ffmpeg -i {file_path} -c copy {repaired_path}", shell=True)
    return repaired_path

def repair_pdf(file_path):
    import fitz  # PyMuPDF
    repaired_path = os.path.join("Sorting_Area/Recovered_Files", os.path.basename(file_path))
    doc = fitz.open(file_path)
    doc.save(repaired_path)
    return repaired_path

def repair_image(file_path):
    repaired_path = os.path.join("Sorting_Area/Recovered_Files", os.path.basename(file_path))
    subprocess.run(f"exiftool -all= {file_path} -o {repaired_path}", shell=True)
    return repaired_path
```

### Step 5: Implement Dependency Regeneration & Path Repair
Reconstruct and index paths:
```python
# ...existing dependency regeneration code...
import json
import os

def generate_index():
    index = {}
    for root, dirs, files in os.walk(SORTED):
        for file in files:
            original_path = os.path.join(root, file)
            # In a real scenario, link original dependency references to new paths.
            index[original_path] = original_path  
    with open(os.path.join(BASE_DIR, "index.json"), "w") as f:
        json.dump(index, f, indent=4)

generate_index()
```

### Step 6: Implement Logging & Override System
Log operations and support overrides:
```python
# ...existing logging code...
import logging
from datetime import datetime

LOG_FILE = os.path.join(BASE_DIR, "Logs", "operations.log")
logging.basicConfig(filename=LOG_FILE, level=logging.INFO)

def log_operation(operation, file_path):
    logging.info(f"{datetime.now()} - {operation} - {file_path}")

log_operation("Moved", "example/path/to/file")
```

---

## Next Steps
- **Finalize logging and error handling.**
- **Expand AI capabilities for videos and audio files.**
- **Enhance file recovery with redundancy checks.**
- **Consider adding a GUI for non-technical users.**

## Conclusion
This system enables professional, automated, AI-enhanced file organization with hierarchical sorting, systematic renaming, repair, and dependency regeneration—entirely confined within a dedicated workspace. Future enhancements may include advanced logging, improved repair algorithms, and a user interface.

---

*End of documentation.*
