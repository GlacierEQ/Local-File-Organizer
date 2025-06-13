import os
import hashlib
from datetime import datetime
from pathlib import Path
from typing import Dict, Optional
from database.database import DatabaseManager
from core.legal_data_sources import LegalClassifier
from file_utils import get_file_stats, read_file_contents

class EnhancedFileOrganizer:
    def __init__(self, config: Dict):
        self.config = config
        self.db = DatabaseManager(self.config['database_path'])
        self.classifier = LegalClassifier()

    def calculate_file_hash(self, filepath: str) -> str:
        # Assuming this method is implemented elsewhere in the code
        pass

    def read_file_contents(self, filepath: str) -> str:
        # Assuming this method is implemented elsewhere in the code
        pass

    def intelligent_rename(self, filepath: str) -> str:
        """Generate a standardized filename based on file content and metadata"""
        content = self.read_file_contents(filepath)
        category = self.classifier.predict_category(content).get('category', 'unknown')
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        base_name = f"{category}_{timestamp}"
        extension = Path(filepath).suffix
        return f"{base_name}{extension}"

    def organize_file(self, filepath: str) -> Dict:
        """Updated organization logic with renaming and sorting into categories"""
        file_stats = get_file_stats(filepath)
        file_hash = self.calculate_file_hash(filepath)
        new_filename = self.intelligent_rename(filepath)
        category = self.classifier.predict_category(self.read_file_contents(filepath)).get('category', 'unknown')
        
        # Move file to category-based directory (e.g., Sorted_Files/Category)
        base_dir = self.config.get('sorted_dir', 'Sorted_Files')
        category_dir = os.path.join(base_dir, category)
        os.makedirs(category_dir, exist_ok=True)
        new_path = os.path.join(category_dir, new_filename)
        os.rename(filepath, new_path)  # Rename and move
        
        file_metadata = {
            'original_path': filepath,
            'new_path': new_path,
            'hash': file_hash,
            'size': file_stats.st_size,
            'modified': file_stats.st_mtime,
            'category': category
        }
        self.db.log_operation(file_metadata)  # Log the change
        return file_metadata
