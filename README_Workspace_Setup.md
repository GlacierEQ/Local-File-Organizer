# **🔹 Expanded Guide: Creating a Dedicated Folder for File Organization & Manual Placement**

## **🔷 Goal:**
Design a **dedicated workspace** where users can **manually place files** for sorting, ensuring all operations (sorting, renaming, repairing, dependency regeneration) happen **only within the workspace** without affecting the rest of the system.

---

## **📂 Folder Structure: How It Works**

The system will operate inside a **single directory** called `Sorting_Area/`. The user **manually** places files inside the `Incoming_Files/` folder, and the system processes them, moving them to `Sorted_Files/` while keeping backups and logs.

```
📂 Sorting_Area/  
   ├── 📂 Incoming_Files/        # 📌 User manually places files here  
   ├── 📂 Sorted_Files/          # 📂 AI-organized files are moved here  
   │    ├── 📂 Documents/  
   │    ├── 📂 Images/  
   │    ├── 📂 Videos/  
   │    ├── 📂 PDFs/  
   │    └── 📂 Uncategorized/  
   ├── 📂 Logs/                  # 📜 Stores logs of all operations  
   ├── 📂 Backups/               # 🔄 Keeps original files before changes  
   ├── 📂 Dependencies/          # 🔗 Stores metadata & missing dependencies  
   ├── 📂 Recovered_Files/       # ♻️ Restores & repairs broken files  
   ├── config.json               # ⚙️ User-defined rules & settings  
```

- **Only files inside `Incoming_Files/` are processed.**
- The system never alters files outside the workspace.
- Missing dependencies are restored from Backups or reconstructed in `Dependencies/`.

---

## **🛠 Step 1: Setting Up the Dedicated Folder in Python**
We will **automatically create the `Sorting_Area/` folder and all subdirectories** if they don’t already exist.

### **📌 Create Folders Automatically**
```python
import os

# Define the workspace directory
BASE_DIR = "Sorting_Area"

# Define all necessary subdirectories
FOLDERS = [
    "Incoming_Files", "Sorted_Files/Documents", "Sorted_Files/Images",
    "Sorted_Files/Videos", "Sorted_Files/PDFs", "Sorted_Files/Uncategorized",
    "Logs", "Backups", "Dependencies", "Recovered_Files"
]

# Create the directories if they don’t exist
for folder in FOLDERS:
    os.makedirs(os.path.join(BASE_DIR, folder), exist_ok=True)

print(f"✅ Workspace '{BASE_DIR}' and subdirectories created successfully.")
```
🔹 **This ensures that all required directories are set up before the sorting process begins.**  
🔹 If the user **accidentally deletes any folder**, the system **recreates them automatically.**

---

## **🛠 Step 2: Detecting User-Placed Files for Processing**
Since the **user must manually place files** in `Incoming_Files/`, the program should detect when new files appear and start processing them.

### **📌 Monitor `Incoming_Files/` for New Files**
```python
import time

INCOMING_DIR = os.path.join(BASE_DIR, "Incoming_Files")

def detect_new_files():
    """Continuously check for new files in the Incoming_Files directory."""
    print(f"📂 Monitoring '{INCOMING_DIR}' for new files...")
    
    while True:
        files = os.listdir(INCOMING_DIR)
        if files:
            print(f"🟢 New files detected: {files}")
            process_files(files)
        time.sleep(10)  # Wait 10 seconds before checking again

def process_files(files):
    """Move files to the sorting function."""
    for file in files:
        file_path = os.path.join(INCOMING_DIR, file)
        sort_and_categorize(file_path)  # Call sorting function
```
🔹 The system **checks every 10 seconds** for new files inside `Incoming_Files/`.  
🔹 If new files appear, it **automatically triggers the sorting process.**  
🔹 Keeps things **simple**—the user **only** needs to place files in `Incoming_Files/`.

---

## **🛠 Step 3: Sorting & Moving Files to the Right Folder**
Each file is analyzed, categorized, and moved inside `Sorted_Files/` under an appropriate category.

### **📌 Smart Sorting Function**
```python
import shutil
from datetime import datetime
from PIL import Image
import pytesseract
from transformers import pipeline

SORTED_DIR = os.path.join(BASE_DIR, "Sorted_Files")

# Load AI Model
classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

def extract_text(image_path):
    """Extracts text from an image using OCR."""
    try:
        return pytesseract.image_to_string(Image.open(image_path))
    except Exception:
        return ""

def classify_document(text):
    """Classifies document based on extracted text."""
    categories = ["Legal", "Finance", "Medical", "Personal", "Work", "Misc"]
    result = classifier(text, candidate_labels=categories)
    return result['labels'][0] if result['scores'][0] > 0.5 else "Uncategorized"

def rename_file(original_name, category):
    """Renames file to a standardized format."""
    timestamp = datetime.now().strftime("%Y-%m-%d_%H%M%S")
    return f"{category}_{timestamp}_{original_name}"

def sort_and_categorize(file_path):
    """Sorts file into the appropriate category folder."""
    category = classify_document(extract_text(file_path))
    new_name = rename_file(os.path.basename(file_path), category)
    
    dest_folder = os.path.join(SORTED_DIR, category)
    os.makedirs(dest_folder, exist_ok=True)  # Ensure the category folder exists

    shutil.move(file_path, os.path.join(dest_folder, new_name))
    print(f"✅ Moved {file_path} ➡️ {dest_folder}/{new_name}")
```
🔹 **Extracts text from images using OCR.**  
🔹 **Uses AI to classify documents.**  
🔹 **Renames and moves files** into `Sorted_Files/` under the correct category.

---

## **🛠 Step 4: Keeping Track of Files with Logs**
We should log every action taken on files, in case users need to undo an operation.

### **📌 Save Logs for Every Action**
```python
import logging

LOG_FILE = os.path.join(BASE_DIR, "Logs", "file_operations.log")

# Configure logging
logging.basicConfig(filename=LOG_FILE, level=logging.INFO, format="%(asctime)s - %(message)s")

def log_action(action, details):
    """Logs actions performed on files."""
    logging.info(f"{action} - {details}")
    print(f"📝 Logged: {action} - {details}")

# Example usage inside `sort_and_categorize()`
log_action("Moved", f"{file_path} ➡️ {dest_folder}/{new_name}")
```
🔹 **Logs all file moves, renames, and sorting actions.**  
🔹 **Keeps track of file history for easy debugging or rollbacks.**

---

## **🛠 Step 5: Preventing File Loss (Backup System)**
Before renaming or moving a file, we **always create a backup** in case of errors.

### **📌 Backup Files Before Modification**
```python
import shutil

BACKUP_DIR = os.path.join(BASE_DIR, "Backups")

def backup_file(file_path):
    """Creates a backup copy of the file before processing."""
    os.makedirs(BACKUP_DIR, exist_ok=True)
    backup_path = os.path.join(BACKUP_DIR, os.path.basename(file_path))
    shutil.copy(file_path, backup_path)
    log_action("Backup", f"{file_path} ➡️ {backup_path}")
```
🔹 **Prevents accidental data loss.**  
🔹 **Allows users to restore original files if needed.**

---

## **🚀 Summary: How It All Works Together**
- **The user places files in `Incoming_Files/`.**
- **The system detects new files automatically.**
- **Each file is processed—scanned via OCR, categorized with AI, renamed, and moved into `Sorted_Files/`.**
- **A backup of the original file is stored in `Backups/` before modifications.**
- **All actions are logged in `Logs/` to facilitate rollbacks and debugging.**

---

## **🚀 What’s Next?**
- **GUI?** Would you like a simple UI (Tkinter/PyQt)?
- **Real-time Progress Bar?** For tracking sorting progress?
- **CLI Commands?** Custom commands to force sorting anytime?

Let me know how you’d like to refine it further! 🚀
