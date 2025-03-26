# AI Document Processor Troubleshooting Guide

This guide helps you diagnose and resolve common issues with the AI document processing system.

## Installation Issues

### Python Dependencies

#### Problem: Import Errors
```
ImportError: No module named 'pytesseract'
```

**Solutions:**
1. Reinstall dependencies:
```bash
pip install -r requirements-ai.txt
```

2. Check Python environment:
```bash
python --version
pip list
```

3. Run setup script:
```bash
python setup_environment.py
```

#### Problem: Version Conflicts
```
Dependencies have conflicting requirements
```

**Solutions:**
1. Create fresh virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

2. Install dependencies in order:
```bash
pip install -r requirements-ai.txt
pip install -r requirements-test.txt
pip install -r requirements-benchmark.txt
```

### Tesseract OCR

#### Problem: Tesseract Not Found
```
TesseractNotFound: tesseract is not installed or not in PATH
```

**Solutions:**

Windows:
1. Download installer from [UB-Mannheim/tesseract](https://github.com/UB-Mannheim/tesseract/wiki)
2. Run installer
3. Add to PATH:
   - Control Panel → System → Advanced → Environment Variables
   - Add Tesseract installation directory to PATH

Linux:
```bash
sudo apt-get update
sudo apt-get install tesseract-ocr
```

macOS:
```bash
brew install tesseract
```

## Processing Issues

### OCR Problems

#### Problem: Poor Text Recognition
```
Extracted text is garbled or inaccurate
```

**Solutions:**
1. Check image quality:
   - Resolution should be at least 300 DPI
   - Image should be properly oriented
   - Text should be clear and high contrast

2. Adjust OCR settings in `config_ai.py`:
```python
OCR_CONFIG = {
    'dpi': 300,
    'preprocessing': True,
    'language': 'eng'
}
```

3. Preprocess images:
   - Convert to grayscale
   - Increase contrast
   - Remove noise

### Memory Issues

#### Problem: Out of Memory
```
MemoryError: Unable to allocate memory
```

**Solutions:**
1. Reduce batch size in `config_ai.py`:
```python
PROCESSING_OPTIONS = {
    'batch_size': 5,  # Reduce from default
    'max_workers': 2  # Reduce parallel processing
}
```

2. Free system resources:
   - Close unnecessary applications
   - Clear temporary files
   - Restart the application

### Performance Issues

#### Problem: Slow Processing
```
Processing taking longer than expected
```

**Solutions:**
1. Run benchmarks to optimize settings:
```bash
python run_benchmarks.py
```

2. Adjust worker count based on CPU cores:
```python
PROCESSING_OPTIONS = {
    'max_workers': cpu_count() - 1
}
```

3. Enable parallel processing:
```python
PROCESSING_OPTIONS = {
    'parallel_processing': True
}
```

## Configuration Issues

### Invalid Configuration

#### Problem: Configuration Validation Errors
```
Missing required settings in configuration
```

**Solutions:**
1. Run configuration verification:
```bash
python verify_setup.py
```

2. Generate default configuration:
```python
from config_ai_utils import generate_default_config
generate_default_config('config_ai.py')
```

3. Check configuration template in documentation

### File Path Issues

#### Problem: File Not Found Errors
```
FileNotFoundError: [Errno 2] No such file or directory
```

**Solutions:**
1. Check directory structure:
```bash
ls -R  # Linux/Mac
dir /s  # Windows
```

2. Create missing directories:
```python
os.makedirs('documents', exist_ok=True)
os.makedirs('consolidated_documents', exist_ok=True)
```

3. Use absolute paths in configuration

## Testing Issues

### Test Failures

#### Problem: Failed Test Cases
```
FAILED tests/test_legal_ai_processor.py
```

**Solutions:**
1. Run tests with detailed output:
```bash
python run_tests.py -v
```

2. Check test requirements:
```bash
pip install -r requirements-test.txt
```

3. Review test logs in `logs` directory

### Benchmark Failures

#### Problem: Benchmark Errors
```
Error during benchmarking
```

**Solutions:**
1. Check benchmark dependencies:
```bash
pip install -r requirements-benchmark.txt
```

2. Clear benchmark results:
```bash
rm -rf benchmark_results/*
```

3. Run with reduced test set:
```python
BENCHMARK_OPTIONS = {
    'quick_test': True
}
```

## Logging and Debugging

### Enable Debug Logging

1. Set logging level in `logging_config.py`:
```python
LOGGING = {
    'level': 'DEBUG'
}
```

2. Check log files in `logs` directory:
```bash
tail -f logs/processing.log
```

3. Enable console output:
```python
logging.basicConfig(level=logging.DEBUG)
```

### Common Debug Steps

1. Verify environment:
```bash
python verify_setup.py
```

2. Check system resources:
```bash
top  # Linux/Mac
Task Manager  # Windows
```

3. Review recent log files:
```bash
ls -lt logs/
```

## Getting Help

1. Check documentation:
   - `README_AI.md`
   - `QUICKSTART.md`
   - `benchmarks/README.md`

2. Run diagnostics:
```bash
python verify_setup.py
python run_tests.py
```

3. Generate debug report:
```bash
python setup_environment.py --diagnostic
```

4. Open GitHub issue with:
   - Error messages
   - Log files
   - System information
   - Steps to reproduce
