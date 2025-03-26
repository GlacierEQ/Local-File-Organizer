# Local File Organizer

An AI-powered file organization system that runs entirely on your local machine, ensuring privacy and security.

## Features

- Multiple organization modes:
  - Content-based organization using AI
  - Date-based organization
  - Type-based organization
  - Interactive checklist mode
- Robust error handling and recovery
- Performance optimization with caching
- Database-backed operation tracking
- Configuration management
- Silent mode with logging
- Preview changes before execution
- Supports various file types:
  - Images
  - Text documents
  - Legal documents
  - And more...

## System Architecture

The system is built with a modular architecture focusing on maintainability and extensibility:

### Core Components

1. **System Manager** (`system_manager_new.py`)
   - Manages system initialization
   - Handles dependency checks
   - Controls system lifecycle
   - Manages system resources

2. **Database** (`database_new.py`)
   - SQLite-based persistent storage
   - Tracks file operations
   - Caches AI processing results
   - Stores user preferences
   - Maintains operation history

3. **Configuration** (`config.py`)
   - Manages system settings
   - Handles model configurations
   - Stores file organization rules
   - Maintains extension mappings

4. **Error Handler** (`error_handler.py`)
   - Comprehensive error handling
   - Operation logging
   - Error recovery mechanisms
   - Debugging support

5. **Performance Optimizer** (`performance.py`)
   - Caching system
   - Memory management
   - Parallel processing
   - Resource optimization

### File Processing

- `file_utils.py`: Core file operations
- `data_processing_common.py`: Common processing functions
- `text_data_processing.py`: Text file processing
- `image_data_processing.py`: Image file processing
- `legal_data_processing.py`: Legal document processing

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/Local-File-Organizer.git
cd Local-File-Organizer
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Run the organizer:
```bash
python main_new.py
```

2. Choose organization mode:
   - Content-based: Uses AI to analyze file content
   - Date-based: Organizes by creation/modification date
   - Type-based: Organizes by file type
   - Checklist: Interactive mode for manual review

3. Select input directory and optional output location

4. Review proposed changes

5. Confirm to execute

## Configuration

The system can be configured through:

1. `config.json`: System-wide settings
2. Command-line arguments
3. Environment variables
4. User preferences in the database

Key configuration options:
```json
{
    "model_config": {
        "image_model_path": "llava-v1.6-vicuna-7b:q4_0",
        "text_model_path": "Llama3.2-3B-Instruct:q3_K_M",
        "temperature": 0.3,
        "max_new_tokens": 3000
    },
    "file_config": {
        "max_filename_length": 50,
        "max_filename_words": 5
    },
    "organization_config": {
        "folder_structure": {
            "image_files": ["photos", "graphics", "screenshots"],
            "text_files": ["documents", "spreadsheets", "presentations"],
            "legal_files": ["contracts", "agreements", "licenses"]
        }
    }
}
```

## Development

### Adding New Features

1. Create new processing modules in the appropriate directory
2. Update the configuration system if needed
3. Add database migrations for new features
4. Update the main FileOrganizer class

### Running Tests

```bash
pytest tests/
```

### Code Style

The project follows:
- PEP 8 for Python style guide
- Type hints for better code clarity
- Comprehensive documentation
- Error handling best practices

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
