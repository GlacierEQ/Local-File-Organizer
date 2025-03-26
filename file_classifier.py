import torch
from transformers import pipeline

# Detect multiple GPUs or fallback to CPU
device = "cuda" if torch.cuda.is_available() else "cpu"
gpu_id = 0  # Set manually if needed (e.g., 0, 1 for multi-GPU systems)

# Use Half-Precision (FP16) for Faster GPU Inference
torch_dtype = torch.float16 if device == "cuda" else torch.float32

# Load models on GPU
fast_classifier = pipeline(
    "zero-shot-classification",
    model="distilbert-base-uncased",
    device=gpu_id if device == "cuda" else -1,
    torch_dtype=torch_dtype
)

accurate_classifier = pipeline(
    "zero-shot-classification",
    model="facebook/bart-large-mnli",
    device=gpu_id if device == "cuda" else -1,
    torch_dtype=torch_dtype
)

classifier = fast_classifier  # Define classifier as fast_classifier

def classify_batch(batch_texts, labels):
    """Process text in batches with reduced memory load, using GPU."""
    results = []
    with torch.no_grad():  # Prevent unnecessary gradient computation
        for text in batch_texts:
            result = fast_classifier(text, candidate_labels=labels)
            results.append(result)
    return results
