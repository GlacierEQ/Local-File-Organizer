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

    def organize_file(self, filepath: str) -> Dict:
        """Organize a single file with enhanced metadata tracking"""
        file_stats = get_file_stats(filepath)
        file_hash = self.calculate_file_hash(filepath)
        
        file_metadata = {
            'path': filepath,
            'hash': file_hash,
            'size': file_stats.st_size,
            'modified': file_stats.st_mtime,
            'category': self.classifier.predict_category(self.read_file_contents(filepath)).get('category', 'unknown')
        }

        # Rest of the file content remains unchanged...
        # [Previous implementation continues here]
