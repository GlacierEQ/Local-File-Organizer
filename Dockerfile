# Use multi-stage build for smaller final image
FROM python:3.11-slim as builder

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Create and activate virtual environment
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Copy requirements files
COPY requirements*.txt ./

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements-ai.txt \
    && pip install --no-cache-dir -r requirements-test.txt \
    && pip install --no-cache-dir -r requirements-benchmark.txt \
    && pip install --no-cache-dir -r requirements-diagnostic.txt

# Final stage
FROM python:3.11-slim

# Install Tesseract and other runtime dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    tesseract-ocr \
    libtesseract-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy virtual environment from builder
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Set working directory
WORKDIR /app

# Copy application code
COPY . .

# Create necessary directories
RUN mkdir -p documents/input documents/output \
    consolidated_documents \
    diagnostic_reports \
    logs \
    benchmark_results

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    LANG=C.UTF-8 \
    LC_ALL=C.UTF-8

# Create non-root user
RUN useradd -m -s /bin/bash appuser \
    && chown -R appuser:appuser /app

# Switch to non-root user
USER appuser

# Expose port for potential web interface
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD python -c "import os, sys; sys.exit(0 if all([os.path.exists(d) for d in ['documents', 'logs']]) else 1)"

# Default command
CMD ["python", "manage_system.py"]
