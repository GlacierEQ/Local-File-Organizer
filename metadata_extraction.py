from PIL import Image
from PIL.ExifTags import TAGS

def extract_image_metadata(file_path: str) -> dict:
    """
    Extracts EXIF metadata from an image file.
    """
    try:
        image = Image.open(file_path)
        exif_data = image._getexif()
        if exif_data:
            return {TAGS.get(tag): value for tag, value in exif_data.items() if tag in TAGS}
    except Exception as e:
        print(f"Metadata extraction failed: {file_path} - {e}")
    return {}
