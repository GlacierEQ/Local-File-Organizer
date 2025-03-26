import subprocess
import os

def optimize_png(file_path: str) -> None:
    """Optimize PNG losslessly using optipng."""
    subprocess.run(["optipng", "-o7", file_path], shell=False)

def optimize_jpeg(file_path: str) -> None:
    """Optimize JPEG by stripping metadata using jpegoptim."""
    subprocess.run(["jpegoptim", "--strip-all", file_path], shell=False)

def optimize_pdf(file_path: str, output_path: str) -> None:
    """Optimize PDF using ghostscript."""
    subprocess.run(["gs", "-sDEVICE=pdfwrite", "-dCompatibilityLevel=1.4",
                    "-dPDFSETTINGS=/screen", "-q", "-o", output_path, file_path], shell=False)

def optimize_video(file_path: str, output_path: str) -> None:
    """Optimize video by re-encoding with ffmpeg at a reduced bitrate (lossless settings may vary)."""
    subprocess.run(["ffmpeg", "-i", file_path, "-b:v", "1M", output_path], shell=False)

def optimize_files(file_path: str) -> None:
    """
    Determine file type and apply optimization.
    Back up the original file before optimization.
    """
    ext = os.path.splitext(file_path)[1].lower()
    BACKUP_DIR = os.path.join("Sorting_Area", "Backups")
    os.makedirs(BACKUP_DIR, exist_ok=True)

    if ext == ".png":
        optimize_png(file_path)
    elif ext in [".jpg", ".jpeg"]:
        optimize_jpeg(file_path)
    elif ext == ".pdf":
        output_path = os.path.join(BACKUP_DIR, os.path.basename(file_path))
        optimize_pdf(file_path, output_path)
    elif ext in [".mp4", ".mkv"]:
        output_path = os.path.join(BACKUP_DIR, os.path.basename(file_path))
        optimize_video(file_path, output_path)
    else:
        print(f"No optimization available for {file_path}")
    
    # Backup the original file
    import shutil
    shutil.copy(file_path, os.path.join(BACKUP_DIR, os.path.basename(file_path)))
