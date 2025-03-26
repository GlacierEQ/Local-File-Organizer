import whisper

# Load Whisper model (choose a variant based on speed/accuracy trade-off)
model = whisper.load_model("base")

def transcribe_audio(file_path: str) -> str:
    """
    Convert speech from an audio file (MP3, WAV, FLAC) into text.
    """
    result = model.transcribe(file_path)
    return result.get("text", "")
