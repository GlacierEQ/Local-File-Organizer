# Local File Organizer: AI File Management Run Entirely on Your Device, Privacy Assured

Tired of digital clutter? Overwhelmed by disorganized files scattered across your computer? Let AI do the heavy lifting! The Local File Organizer is your personal organizing assistant, using cutting-edge AI to bring order to your file chaos - all while respecting your privacy.

## How It Works 💡

Before:

```
/home/user/messy_documents/
├── IMG_20230515_140322.jpg
├── IMG_20230516_083045.jpg
├── IMG_20230517_192130.jpg
├── budget_2023.xlsx
├── meeting_notes_05152023.txt
├── project_proposal_draft.docx
├── random_thoughts.txt
├── recipe_chocolate_cake.pdf
├── scan0001.pdf
├── vacation_itinerary.docx
└── work_presentation.pptx

0 directories, 11 files
```

After:

```
/home/user/organized_documents/
├── Financial
│   └── 2023_Budget_Spreadsheet.xlsx
├── Food_and_Recipes
│   └── Chocolate_Cake_Recipe.pdf
├── Meetings_and_Notes
│   └── Team_Meeting_Notes_May_15_2023.txt
├── Personal
│   └── Random_Thoughts_and_Ideas.txt
├── Photos
│   ├── Cityscape_Sunset_May_17_2023.jpg
│   ├── Morning_Coffee_Shop_May_16_2023.jpg
│   └── Office_Team_Lunch_May_15_2023.jpg
├── Travel
│   └── Summer_Vacation_Itinerary_2023.docx
└── Work
    ├── Project_X_Proposal_Draft.docx
    ├── Quarterly_Sales_Report.pdf
    └── Marketing_Strategy_Presentation.pptx

7 directories, 11 files
```

## Updates 🚀

**[2024/09] v0.0.2**:

- Featured by [Nexa Gallery](https://nexaai.com/gallery) and [Nexa SDK Cookbook](https://github.com/NexaAI/nexa-sdk/tree/main/examples)!
- Dry Run Mode: check sorting results before committing changes
- Silent Mode: save all logs to a txt file for quieter operation
- Added file support: `.md`, .`excel`, `.ppt`, and `.csv`
- Three sorting options: by content, by date, and by type
- The default text model is now [Llama3.2 3B](https://nexaai.com/meta/Llama3.2-3B-Instruct/gguf-q3_K_M/file)
- Improved CLI interaction experience
- Added real-time progress bar for file analysis

Please update the project by deleting the original project folder and reinstalling the requirements. Refer to the installation guide from Step 4.

## Roadmap 📅

- [ ] Copilot Mode: chat with AI to tell AI how you want to sort the file (ie. read and rename all the PDFs)
- [ ] Change models with CLI
- [ ] ebook format support
- [ ] audio file support
- [ ] video file support
- [ ] Implement best practices like Johnny Decimal
- [ ] Check file duplication
- [ ] Dockerfile for easier installation
- [ ] People from [Nexa](https://github.com/NexaAI/nexa-sdk) is helping me to make executables for macOS, Linux and Windows

## Features and Capabilities 🚀

This intelligent file organizer harnesses the power of advanced AI models, including language models (LMs) and vision-language models (VLMs), to automate the process of organizing files. Here's what it can do:

### Core Features

- **Multiple Organization Modes**:
  - Content-based organization using AI
  - Date-based organization
  - Type-based organization
    - Semantic hierarchy mode for deep category/year organization with optional cross-references
  - Protocol Buffer schema for legal case management hierarchies
  - Interactive checklist mode for manual review
- **AI-Powered Content Understanding**:
  - **Textual Analysis**: Uses the [Llama3.2 3B](https://nexaai.com/meta/Llama3.2-3B-Instruct/gguf-q3_K_M/file) to analyze and summarize text-based content.
  - **Visual Content Analysis**: Uses the [LLaVA-v1.6](https://nexaai.com/liuhaotian/llava-v1.6-vicuna-7b/gguf-q4_0/file) to interpret visual files.
- **Privacy-First**: All AI processing happens 100% on your local device using the [Nexa SDK](https://github.com/NexaAI/nexa-sdk).
- **Preview Changes**: Review proposed changes before execution.
- **Silent Mode**: Operate with logging for quieter execution.
- **Performance Optimization**: Utilizes caching and parallel processing for improved speed.
- **Robust Error Handling**: Comprehensive error recovery and logging mechanisms.
- Operator Command Center GUI for monitoring and teaching AI

### AI Capabilities 🧠

- **Multi-Format Support**: Processes various file types including TXT, PDF, and images (JPG/PNG) through OCR capabilities.
- **Advanced Analysis**:
  - Document summarization
  - Entity recognition (especially useful for legal documents)
  - Question answering over documents
- **OCR Processing**: Text extraction from scanned documents and images.
- **Validation**: File type verification and content hashing for data integrity.

These capabilities make the system especially powerful for managing complex document sets like legal files, research papers, or mixed media collections.

## Supported File Types 📁

- **Images:** `.png`, `.jpg`, `.jpeg`, `.gif`, `.bmp`
- **Text Files:** `.txt`, `.docx`, `.md`
- **Spreadsheets:** `.xlsx`, `.csv`
- **Presentations:** `.ppt`, `.pptx`
- **PDFs:** `.pdf`
- **Legal Documents**: Various formats supported

## System Architecture

The Local File Organizer is built with a modular architecture focusing on maintainability and extensibility:

### Core Components

1. **System Manager** (`system_manager_new.py`): Manages system initialization, dependency checks, and system lifecycle.
2. **Database** (`database_new.py`): SQLite-based storage for operation tracking, AI result caching, and user preferences.
3. **Configuration** (`config.py`): Manages system settings, model configurations, and organization rules.
4. **Error Handler** (`error_handler.py`): Provides comprehensive error handling and logging.
5. **Performance Optimizer** (`performance.py`): Implements caching, memory management, and parallel processing.

### File Processing Modules

- `file_utils.py`: Core file operations
- `data_processing_common.py`: Common processing functions
- `text_data_processing.py`: Text file processing
- `image_data_processing.py`: Image file processing
- `legal_data_processing.py`: Legal document processing

## Prerequisites 💻

- **Operating System:** Compatible with Windows, macOS, and Linux.
- **Python Version:** Python 3.12
- **Conda:** Anaconda or Miniconda installed.
- **Git:** For cloning the repository (or you can download the code as a ZIP file).

## Installation 🛠

> For SDK installation and model-related issues, please post on [here](https://github.com/NexaAI/nexa-sdk/issues).

### 1. Install Python

Before installing the Local File Organizer, make sure you have Python installed on your system. We recommend using Python 3.12 or later.

You can download Python from [the official website](<(https://www.python.org/downloads/)>).

Follow the installation instructions for your operating system.

### 2. Clone the Repository

Clone this repository to your local machine using Git:

```zsh
git clone https://github.com/QiuYannnn/Local-File-Organizer.git
```

Or download the repository as a ZIP file and extract it to your desired location.

### 3. Set Up the Python Environment

Create a new Conda environment named `local_file_organizer` with Python 3.12:

```zsh
conda create --name local_file_organizer python=3.12
```

Activate the environment:

```zsh
conda activate local_file_organizer
```

### 4. Install Nexa SDK ️

#### CPU Installation

To install the CPU version of Nexa SDK, run:

```bash
pip install nexaai --prefer-binary --index-url https://nexaai.github.io/nexa-sdk/whl/cpu --extra-index-url https://pypi.org/simple --no-cache-dir
```

#### GPU Installation (Metal - macOS)

For the GPU version supporting Metal (macOS), run:

```bash
CMAKE_ARGS="-DGGML_METAL=ON -DSD_METAL=ON" pip install nexaai --prefer-binary --index-url https://nexaai.github.io/nexa-sdk/whl/metal --extra-index-url https://pypi.org/simple --no-cache-dir
```

For detailed installation instructions of Nexa SDK for **CUDA** and **AMD GPU** support, please refer to the [Installation section](https://github.com/NexaAI/nexa-sdk?tab=readme-ov-file#installation) in the main README.

### 5. Install Dependencies

1. Ensure you are in the project directory:

   ```zsh
   cd path/to/Local-File-Organizer
   ```

   Replace `path/to/Local-File-Organizer` with the actual path where you cloned or extracted the project.

2. Install the required dependencies:
   ```zsh
   pip install -r requirements.txt
   ```

**Note:** If you encounter issues with any packages, install them individually:

```zsh
pip install nexa Pillow pytesseract PyMuPDF python-docx
```

With the environment activated and dependencies installed, run the script using:

### 6. Running the Script🎉

```zsh
python main_optimized.py
```

Note: We've introduced an optimized version of the main script (`main_optimized.py`) that includes memory-efficient processing and batch operations. This version is recommended for large datasets or systems with limited memory.

Key optimizations in `main_optimized.py`:

- Uses generators for file path collection to reduce memory usage
- Processes files in batches to manage memory more effectively
- Implements lazy loading and caching of AI models
- Optimizes imports to reduce memory footprint

If you encounter any issues with the optimized version, you can still use the original `main.py` script.

## Notes

- **SDK Models:**

  - The script uses `NexaVLMInference` and `NexaTextInference` models [usage](https://docs.nexaai.com/sdk/python-interface/gguf).
  - Ensure you have access to these models and they are correctly set up.
  - You may need to download model files or configure paths.

- **Dependencies:**

  - **pytesseract:** Requires Tesseract OCR installed on your system.
    - **macOS:** `brew install tesseract`
    - **Ubuntu/Linux:** `sudo apt-get install tesseract-ocr`
    - **Windows:** Download from [Tesseract OCR Windows Installer](https://github.com/UB-Mannheim/tesseract/wiki)
  - **PyMuPDF (fitz):** Used for reading PDFs.

- **Processing Time:**

  - Processing may take time depending on the number and size of files.
  - The script uses multiprocessing to improve performance.

- **Customizing Prompts:**
  - You can adjust prompts in `data_processing.py` to change how metadata is generated.

## License

This project is dual-licensed under the MIT License and Apache 2.0 License. You may choose which license you prefer to use for this project.

- See the [MIT License](LICENSE-MIT) for more details.
