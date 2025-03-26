from typing import Dict, Any
from pathlib import Path
from database.models import FileMetadata
from core.legal_data_sources import LegalDataSource
from core.ai_media_processor import AIMediaProcessor
from datetime import datetime
import pytesseract

import nltk
from nltk.tokenize import sent_tokenize
import json

class LegalAIProcessor:
    """Processes legal documents using AI and NLP techniques"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.data_source = LegalDataSource(config['legal_sources'])
        self.media_processor = AIMediaProcessor(config['ai_models'])
        
        # Initialize NLP resources
        nltk.download('punkt', quiet=True)
        
    def process_document(self, file_path: Path) -> FileMetadata:
        """Main processing pipeline for legal documents"""
        try:
            text = self._extract_text(file_path)

            # Process text with AI models
            processed_data = self.media_processor.analyze_text(text)
            
            # Extract legal entities
            entities = self.data_source.extract_entities(text)
            
            # Generate summary
            summary = self._generate_summary(text)
            
            return FileMetadata(
                file_path=str(file_path),
                file_type=file_path.suffix[1:].upper(),
                size=file_path.stat().st_size,
                modified_at=datetime.fromtimestamp(file_path.stat().st_mtime),
                metadata={
                    'entities': entities,
                    'summary': summary,
                    'ai_analysis': processed_data
                },
                hash=self._generate_file_hash(file_path)
            )
            
        except Exception as e:
            raise LegalProcessingError(f"Error processing {file_path.name}: {str(e)}") from e

    def _extract_text(self, file_path: Path) -> str:
        """Extract text from supported document formats"""
        if file_path.suffix.lower() == '.pdf':
            return self.media_processor.extract_pdf_text(file_path)
        elif file_path.suffix.lower() in ['.jpg', '.png', '.jpeg']:
            return pytesseract.image_to_string(str(file_path))
        return file_path.read_text(encoding='utf-8')
    
    def _generate_summary(self, text: str) -> str:
        """Generate summary using NLP techniques"""
        sentences = sent_tokenize(text)
        return ' '.join(sentences[:3])  # Simple first 3 sentences summary
    
    def _generate_file_hash(self, file_path: Path) -> str:
        """Generate SHA-256 hash of file contents"""
        import hashlib
        sha256 = hashlib.sha256()
        with open(file_path, 'rb') as f:
            while chunk := f.read(4096):
                sha256.update(chunk)
        return sha256.hexdigest()

class LegalProcessingError(Exception):
    """Custom exception for legal document processing errors"""
    pass
