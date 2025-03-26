"""Configuration settings for the AI Document Processor."""

# Directory settings
INPUT_DIR = "documents"
OUTPUT_DIR = "consolidated_documents"
TEMP_DIR = "temp_processing"

# Document classification settings
DOCUMENT_TYPES = {
    'case_law': {
        'keywords': [
            'court', 'opinion', 'held', 'judgment', 'ruling',
            'affirmed', 'reversed', 'remanded', 'certiorari'
        ],
        'required_phrases': [
            'delivered the opinion',
            'we hold',
            'it is so ordered'
        ],
        'weight': 1.5  # Higher weight for more specific document types
    },
    'docket_entries': {
        'keywords': [
            'docket', 'filed', 'entry', 'clerk', 'minute',
            'order', 'notice', 'motion', 'hearing'
        ],
        'date_pattern': r'\d{1,2}/\d{1,2}/\d{4}',
        'entry_pattern': r'\[\d+\]',
        'weight': 1.0
    },
    'pleadings': {
        'keywords': [
            'complaint', 'answer', 'motion', 'petition',
            'brief', 'memorandum', 'declaration'
        ],
        'sections': [
            'jurisdiction', 'venue', 'parties',
            'facts', 'claims', 'prayer for relief'
        ],
        'weight': 1.2
    },
    'exhibits': {
        'keywords': [
            'exhibit', 'evidence', 'attachment',
            'appendix', 'document'
        ],
        'markers': ['EXHIBIT', 'EX.', 'Exhibit'],
        'weight': 0.8
    }
}

# OCR settings
OCR_CONFIG = {
    'language': 'eng',  # Language for OCR
    'dpi': 300,  # DPI for image processing
    'psm': 3,  # Page segmentation mode
    'oem': 3,  # OCR Engine mode
    'timeout': 30,  # Timeout in seconds
    'preprocessing': True,  # Enable image preprocessing
}

# Output formatting
OUTPUT_FORMAT = {
    'case_law': {
        'title': 'Consolidated Case Law',
        'sections': [
            'Case Information',
            'Procedural History',
            'Holdings',
            'Analysis'
        ],
        'metadata_fields': [
            'court', 'date', 'judges',
            'citation', 'parties'
        ]
    },
    'docket_entries': {
        'title': 'Consolidated Docket Entries',
        'sort_by': 'date',
        'ascending': True,
        'group_by': 'case_number',
        'metadata_fields': [
            'date', 'entry_number',
            'document_type', 'filer'
        ]
    },
    'pleadings': {
        'title': 'Consolidated Pleadings',
        'sections': [
            'Caption',
            'Introduction',
            'Jurisdiction',
            'Facts',
            'Claims',
            'Relief'
        ],
        'metadata_fields': [
            'case_number', 'filing_date',
            'document_type', 'parties'
        ]
    },
    'exhibits': {
        'title': 'Consolidated Exhibits',
        'sort_by': 'exhibit_number',
        'ascending': True,
        'metadata_fields': [
            'exhibit_number', 'date',
            'type', 'description'
        ]
    }
}

# Processing options
PROCESSING_OPTIONS = {
    'parallel_processing': True,
    'max_workers': 4,
    'batch_size': 10,
    'preserve_formatting': True,
    'extract_metadata': True,
    'create_index': True,
    'generate_summaries': True,
    'backup_originals': True
}

# Error handling
ERROR_HANDLING = {
    'max_retries': 3,
    'retry_delay': 5,  # seconds
    'log_errors': True,
    'error_log_path': 'logs/processing_errors.log',
    'notify_on_error': False,
    'skip_problem_files': True
}

# Logging configuration
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
        },
    },
    'handlers': {
        'default': {
            'level': 'INFO',
            'formatter': 'standard',
            'class': 'logging.StreamHandler',
        },
        'file': {
            'level': 'DEBUG',
            'formatter': 'standard',
            'class': 'logging.FileHandler',
            'filename': 'logs/ai_processor.log',
            'mode': 'a',
        },
    },
    'loggers': {
        '': {
            'handlers': ['default', 'file'],
            'level': 'INFO',
            'propagate': True
        }
    }
}
