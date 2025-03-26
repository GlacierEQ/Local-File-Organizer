# Local File Organizer: AI File Management Run Entirely on Your Device, Privacy Assured

Tired of digital clutter? Overwhelmed by disorganized files scattered across your computer? Let AI do the heavy lifting with our Local File Organizer, now with enhanced legal document processing capabilities!

## Features

- **Smart Content Analysis**: Uses AI to understand file contents and organize them meaningfully
- **Legal Document Processing**: Specialized handling for legal documents including:
  - Case type identification (divorce, custody, labor disputes, malpractice, defamation)
  - Legal entity extraction (parties, case numbers, courts, citations)
  - Metadata generation and structured summaries
  - Smart file naming and folder organization based on legal context
- **Privacy First**: All processing happens locally on your device
- **Multiple Organization Modes**:
  - Content-based (using AI analysis)
  - Date-based
  - Type-based
  - Checklist mode for manual review
- **Supports Multiple File Types**:
  - Legal documents (.aff, .dec, .motion, .order, .pleading, .subpoena, .complaint, .answer, .brief, .petition, .judgment)
  - Text documents (.txt, .md, .docx, .pdf)
  - Images (.png, .jpg, .jpeg, .gif, .bmp)
  - Spreadsheets (.xls, .xlsx, .csv)
  - Presentations (.ppt, .pptx)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/Local-File-Organizer.git
cd Local-File-Organizer
```

2. Install dependencies:
```bash
pip install -r requirements.txt
pip install -r requirements-legal.txt
```

## Usage

Run the main script:
```bash
python main.py
```

Follow the interactive prompts to:
1. Choose between silent mode or interactive mode
2. Select input directory containing files to organize
3. Choose organization mode (content, date, type, or checklist)
4. Review proposed organization structure
5. Confirm to proceed with file organization

## Legal Document Processing

The system now includes specialized processing for legal documents:

- **Case Type Detection**: Automatically identifies the type of legal case based on document content
- **Entity Extraction**: Identifies and extracts key legal entities such as:
  - Party names
  - Case numbers
  - Court information
  - Citation references
  - Key dates
  - Monetary values
- **Smart Organization**: Creates a logical folder structure based on:
  - Case type (divorce, custody, labor, malpractice, defamation)
  - Filing date
  - Case status
- **Metadata Generation**: Creates structured summaries including:
  - Case type classification
  - Involved parties
  - Key dates and deadlines
  - Monetary values
  - Important legal terms

## Privacy & Security

All processing is performed locally on your device. No data is sent to external servers, ensuring complete privacy of your legal documents and other sensitive files.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
