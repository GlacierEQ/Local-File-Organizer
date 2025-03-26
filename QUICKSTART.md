# AI Legal Document Processor Quick Start Guide

This guide will help you get started with the AI-powered legal document processing system. The system can analyze, categorize, and consolidate legal documents while maintaining the integrity of original files.

## Installation

1. Install Python dependencies:
```bash
pip install -r requirements-ai.txt
```

2. Install Tesseract OCR (required for document scanning):
- Windows: Download from [UB-Mannheim/tesseract](https://github.com/UB-Mannheim/tesseract/wiki)
- Linux: `sudo apt-get install tesseract-ocr`
- macOS: `brew install tesseract`

## Quick Start with Sample Documents

1. Copy sample documents to your working directory:
```bash
cp -r sample_data/legal_documents/* documents/
```

2. Run the example script:
```bash
python example_ai_processing.py
```

3. Check the results in the `consolidated_documents` directory:
- `case_law_consolidated.docx`: Contains processed judicial opinions
- `docket_entries_consolidated.docx`: Contains chronological case histories
- `pleadings_consolidated.docx`: Contains complaints and other pleadings
- `exhibits_consolidated.docx`: Contains documentary evidence

## Sample Documents Overview

The system comes with example documents demonstrating different types of legal content:

### 1. Case Law Example
- Location: `sample_data/legal_documents/case_law_example.txt`
- Type: Supreme Court Opinion
- Features: Legal citations, holdings, judicial reasoning

### 2. Docket Entries Example
- Location: `sample_data/legal_documents/docket_entry_example.txt`
- Type: Court Docket
- Features: Chronological entries, document numbers, filing dates

### 3. Pleading Example
- Location: `sample_data/legal_documents/pleading_example.txt`
- Type: Civil Complaint
- Features: Legal formatting, causes of action, prayer for relief

### 4. Exhibit Example
- Location: `sample_data/legal_documents/exhibit_example.txt`
- Type: Documentary Evidence
- Features: Corporate policy, certification, metadata

## Processing Your Own Documents

1. Create a `documents` directory:
```bash
mkdir documents
```

2. Place your legal documents in the directory:
- Supported formats: PDF, DOCX, TXT, PNG, JPG
- Documents will be automatically classified
- Original files remain unchanged

3. Run the processing:
```bash
python example_ai_processing.py
```

4. Review the consolidated output in `consolidated_documents/`

## Features

- OCR scanning of documents
- Automatic document classification
- Metadata extraction
- Content consolidation by category
- Original document preservation
- Formatted output generation

## Testing

Run the test suite to verify functionality:
```bash
python run_tests.py
```

## Troubleshooting

1. OCR Issues:
   - Ensure Tesseract is properly installed
   - Check image quality and resolution
   - Verify file permissions

2. Processing Errors:
   - Check file formats are supported
   - Ensure sufficient disk space
   - Verify write permissions in output directory

3. Classification Issues:
   - Review document formatting
   - Check for clear document type indicators
   - Ensure text is properly extracted

## Next Steps

- Review the full documentation in `README_AI.md`
- Explore the API in `legal_ai_processor.py`
- Check out test cases in `tests/test_legal_ai_processor.py`
- Customize classification rules for your needs

## Support

For issues or questions:
1. Check the troubleshooting guide
2. Review test failures for clues
3. Examine processing logs
4. Open an issue on GitHub

## Contributing

Contributions are welcome! See `README_AI.md` for guidelines.
