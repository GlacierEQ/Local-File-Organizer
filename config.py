from dataclasses import dataclass
from typing import Dict, List, Optional
import json
import os
from config_ai_settings import DOCUMENT_TYPES, OCR_CONFIG, OUTPUT_FORMAT, PROCESSING_OPTIONS, ERROR_HANDLING, LOGGING

@dataclass
class ModelConfig:
    """Configuration for AI models"""
    image_model_path: str = "llava-v1.6-vicuna-7b:q4_0"
    text_model_path: str = "Llama3.2-3B-Instruct:q3_K_M"
    temperature: float = 0.3
    max_new_tokens: int = 3000
    top_k: int = 3
    top_p: float = 0.2
    n_ctx: int = 2048

@dataclass
class FileConfig:
    """Configuration for file organization"""
    image_extensions: List[str] = None
    text_extensions: List[str] = None
    legal_extensions: List[str] = None
    max_filename_length: int = 50
    max_filename_words: int = 5

    def __post_init__(self):
        if self.image_extensions is None:
            self.image_extensions = ['.png', '.jpg', '.jpeg', '.gif', '.bmp', '.tiff']
        if self.text_extensions is None:
            self.text_extensions = ['.txt', '.md', '.docx', '.doc', '.pdf', '.xls', '.xlsx']
        if self.legal_extensions is None:
            self.legal_extensions = ['.doc', '.docx', '.pdf', '.txt']

@dataclass
class OrganizationConfig:
    """Configuration for organization rules"""
    folder_structure: Dict[str, List[str]] = None
    link_type: str = "hardlink"
    organize_by_date_format: str = "%Y/%B"  # Year/Month

    def __post_init__(self):
        if self.folder_structure is None:
            self.folder_structure = {
                "image_files": ["photos", "graphics", "screenshots"],
                "text_files": ["documents", "spreadsheets", "presentations"],
                "legal_files": ["contracts", "agreements", "licenses"]
            }

class Config:
    """Main configuration class"""
    def __init__(self, config_path: str = "config.json"):
        self.config_path = config_path
        self.model_config = ModelConfig()
        self.file_config = FileConfig()
        self.organization_config = OrganizationConfig()
        self.ai_config = {
            'DOCUMENT_TYPES': DOCUMENT_TYPES,
            'OCR_CONFIG': OCR_CONFIG,
            'OUTPUT_FORMAT': OUTPUT_FORMAT,
            'PROCESSING_OPTIONS': PROCESSING_OPTIONS,
            'ERROR_HANDLING': ERROR_HANDLING,
            'LOGGING': LOGGING
        }
        self.load_config()

    def load_config(self):
        """Load configuration from JSON file"""
        if os.path.exists(self.config_path):
            with open(self.config_path, 'r') as f:
                data = json.load(f)
                self.model_config = ModelConfig(**data.get('model_config', {}))
                self.file_config = FileConfig(**data.get('file_config', {}))
                self.organization_config = OrganizationConfig(**data.get('organization_config', {}))
                self.ai_config.update(data.get('ai_config', {}))

    def save_config(self):
        """Save configuration to JSON file"""
        config_data = {
            'model_config': self.model_config.__dict__,
            'file_config': self.file_config.__dict__,
            'organization_config': self.organization_config.__dict__,
            'ai_config': self.ai_config
        }
        with open(self.config_path, 'w') as f:
            json.dump(config_data, f, indent=4)

    def update_config(self, section: str, **kwargs):
        """Update configuration parameters"""
        if section == 'model':
            for key, value in kwargs.items():
                if hasattr(self.model_config, key):
                    setattr(self.model_config, key, value)
        elif section == 'file':
            for key, value in kwargs.items():
                if hasattr(self.file_config, key):
                    setattr(self.file_config, key, value)
        elif section == 'organization':
            for key, value in kwargs.items():
                if hasattr(self.organization_config, key):
                    setattr(self.organization_config, key, value)
        elif section == 'ai':
            self.ai_config.update(kwargs)
        self.save_config()

# Initialize the configuration
config = Config()
