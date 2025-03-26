import os
import magic

def fix_file_extension(file_path: str) -> str:
    """
    Detects the correct file extension using file signatures and renames the file.
    Returns the new file name.
    """
    mime = magic.Magic(mime=True)
    detected_type = mime.from_file(file_path)
    
    extensions_map = {
        "image/jpeg": ".jpg",
        "image/png": ".png",
        "application/pdf": ".pdf",
        "video/mp4": ".mp4",
        "audio/mpeg": ".mp3"
    }
    
    correct_ext = extensions_map.get(detected_type)
    if correct_ext:
        new_name = os.path.splitext(file_path)[0] + correct_ext
        os.rename(file_path, new_name)
        return new_name
    return file_path
