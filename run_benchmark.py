import torch
from transformers import pipeline
import time

# Detect GPU
device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"Running AI on: {device}")

# Initialize the fast classifier
fast_classifier = pipeline(
    "zero-shot-classification",
    model="distilbert-base-uncased",
    device=0 if device == "cuda" else -1
)

# Time a sample classification
text_sample = "This is a test document."
start = time.time()
result = fast_classifier(text_sample, candidate_labels=["Legal", "Finance", "Medical"])
end = time.time()
print(f"Execution time: {end - start:.2f} sec")

# Benchmark a simple matrix multiplication on the detected device.
A = torch.randn(1000, 1000, device=device)
B = torch.randn(1000, 1000, device=device)

start = time.time()
C = torch.mm(A, B)
end = time.time()

print(f"Matrix multiplication completed in {end - start:.6f} seconds on {device}")
