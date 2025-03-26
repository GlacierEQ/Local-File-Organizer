"""Utility functions for managing AI document processor configuration."""

import os
import json
import logging
from typing import Dict, List

logger = logging.getLogger(__name__)

def validate_config(config: Dict) -> Dict[str, List[str]]:
    """
    Validate the configuration settings.
    Returns a dictionary with lists of any missing or invalid settings.
    """
    results = {
        'missing_settings': [],
        'invalid_settings': [],
        'warnings': []
    }

    # Required settings
    required_settings = [
        'DOCUMENT_TYPES',
        'OCR_CONFIG',
        'OUTPUT_FORMAT',
        'PROCESSING_OPTIONS'
    ]

    # Check for required settings
    for setting in required_settings:
        if setting not in config:
            results['missing_settings'].append(setting)

    # Validate document types
    if 'DOCUMENT_TYPES' in config:
        for doc_type, settings in config['DOCUMENT_TYPES'].items():
            if not isinstance(settings, dict):
                results['invalid_settings'].append(f"Invalid document type config for {doc_type}")
                continue
            
            if 'keywords' not in settings:
                results['missing_settings'].append(f"Missing keywords in {doc_type} config")
            if 'weight' not in settings:
                results['missing_settings'].append(f"Missing weight in {doc_type} config")

    # Validate OCR config
    if 'OCR_CONFIG' in config:
        required_ocr = ['language', 'dpi', 'timeout']
        for field in required_ocr:
            if field not in config['OCR_CONFIG']:
                results['missing_settings'].append(f"Missing {field} in OCR config")

    # Validate output format
    if 'OUTPUT_FORMAT' in config:
        for doc_type, format_config in config['OUTPUT_FORMAT'].items():
            if 'title' not in format_config:
                results['warnings'].append(f"Missing title in output format for {doc_type}")

    # Validate processing options
    if 'PROCESSING_OPTIONS' in config:
        required_options = ['parallel_processing', 'max_workers', 'batch_size']
        for option in required_options:
            if option not in config['PROCESSING_OPTIONS']:
                results['missing_settings'].append(f"Missing {option} in processing options")

    return results

def generate_default_config(output_path: str) -> None:
    """Generate a default configuration file."""
    default_config = {
        'DOCUMENT_TYPES': {
            'case_law': {
                'keywords': ['court', 'opinion', 'held'],
                'weight': 1.0
            },
            'docket_entries': {
                'keywords': ['docket', 'filed', 'entry'],
                'weight': 1.0
            },
            'pleadings': {
                'keywords': ['complaint', 'answer', 'motion'],
                'weight': 1.0
            },
            'exhibits': {
                'keywords': ['exhibit', 'evidence', 'attachment'],
                'weight': 1.0
            }
        },
        'OCR_CONFIG': {
            'language': 'eng',
            'dpi': 300,
            'timeout': 30,
            'preprocessing': True
        },
        'OUTPUT_FORMAT': {
            'case_law': {
                'title': 'Consolidated Case Law',
                'sections': ['Case Information', 'Holdings', 'Analysis']
            },
            'docket_entries': {
                'title': 'Consolidated Docket Entries',
                'sort_by': 'date'
            },
            'pleadings': {
                'title': 'Consolidated Pleadings',
                'sections': ['Caption', 'Body', 'Prayer']
            },
            'exhibits': {
                'title': 'Consolidated Exhibits',
                'sort_by': 'exhibit_number'
            }
        },
        'PROCESSING_OPTIONS': {
            'parallel_processing': True,
            'max_workers': 4,
            'batch_size': 10,
            'preserve_formatting': True
        }
    }

    with open(output_path, 'w') as f:
        json.dump(default_config, f, indent=4)
        logger.info(f"Default configuration saved to {output_path}")

def load_config(config_path: str) -> Dict:
    """Load and validate a configuration file."""
    try:
        with open(config_path, 'r') as f:
            config = json.load(f)
        
        validation_results = validate_config(config)
        if any(validation_results.values()):
            logger.warning("Configuration validation issues found:")
            logger.warning(json.dumps(validation_results, indent=2))
        
        return config
    except Exception as e:
        logger.error(f"Error loading configuration: {str(e)}")
        raise

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    # Example usage
    config_path = "config_example.json"
    generate_default_config(config_path)
    config = load_config(config_path)
    print("Configuration loaded successfully")
