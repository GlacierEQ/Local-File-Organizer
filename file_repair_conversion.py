import os
import subprocess
import shutil
import fitz  # PyMuPDF for PDF repairs

BASE_DIR = "Sorting_Area"
RECOVERED_DIR = os.path.join(BASE_DIR, "Recovered_Files")
INCOMING_DIR = os.path.join(BASE_DIR, "Incoming_Files")
BACKUP_DIR = os.path.join(BASE_DIR, "Backups")

def repair_corrupted_file(file_path: str) -> str:
    """
    Attempt to repair a file based on its extension.
    Returns the repaired file path or the original if repair fails.
    """
    ext = os.path.splitext(file_path)[1].lower()
    repaired_path = os.path.join(RECOVERED_DIR, os.path.basename(file_path))
    
    if ext in [".mp4", ".avi", ".mkv"]:
        subprocess.run(["ffmpeg", "-i", file_path, "-codec", "copy", repaired_path], shell=False)
    elif ext == ".pdf":
        try:
            doc = fitz.open(file_path)
            doc.save(repaired_path)
        except Exception as e:
            print(f"PDF repair failed: {file_path} - {e}")
            return file_path
    elif ext in [".jpg", ".png"]:
        subprocess.run(["exiftool", "-all=", file_path, "-o", repaired_path], shell=False)
    else:
        # Additional repair logic for text or other formats can be added.
        return file_path
    return repaired_path

def convert_file(file_path: str, target_ext: str) -> str:
    """
    Convert file to target_ext if needed.
    Examples: MKV ➝ MP4, TIFF ➝ PNG, DOC ➝ DOCX, CSV ➝ XLSX.
    Back up original, and output converted file to INCOMING_DIR for sorting.
    """
    base = os.path.splitext(os.path.basename(file_path))[0]
    converted_path = os.path.join(INCOMING_DIR, f"{base}{target_ext}")
    
    if target_ext == ".mp4":
        subprocess.run(["ffmpeg", "-i", file_path, "-codec", "copy", converted_path], shell=False)
    elif target_ext == ".png":
        subprocess.run(["convert", file_path, converted_path], shell=False)
    elif target_ext == ".docx":
        subprocess.run(["libreoffice", "--headless", "--convert-to", "docx", file_path, "--outdir", INCOMING_DIR], shell=False)
    elif target_ext == ".xlsx":
        subprocess.run(["libreoffice", "--headless", "--convert-to", "xlsx", file_path, "--outdir", INCOMING_DIR], shell=False)
    else:
        return file_path

    shutil.copy(file_path, os.path.join(BACKUP_DIR, os.path.basename(file_path)))
    return converted_path

def auto_convert_file(file_path: str) -> str:
    """
    Auto-detect file format and convert to a modern format if needed.
    """
    ext = os.path.splitext(file_path)[1].lower()
    if ext in [".tiff", ".tif"]:
        return convert_file(file_path, ".png")
    elif ext == ".mkv":
        return convert_file(file_path, ".mp4")
    elif ext == ".doc":
        return convert_file(file_path, ".docx")
    elif ext == ".csv":
        return convert_file(file_path, ".xlsx")
    return file_path
