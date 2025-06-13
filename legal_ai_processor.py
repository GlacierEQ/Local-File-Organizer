from typing import Dict, Any, List
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
        """Updated main processing pipeline to include case timeline and gap analysis if multiple docs are provided"""
        try:
            text = self._extract_text(file_path)

            # Process text with AI models
            processed_data = self.media_processor.analyze_text(text)
            
            # Extract legal entities
            entities = self.data_source.extract_entities(text)
            
            # Generate summary
            summary = self._generate_summary(text)
            
            # Add case-specific analysis if context allows
            if 'case_id' in self.config:  # Assume config has case context; add if needed
                timeline_entry = self.build_case_timeline([FileMetadata(
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
                )])
                gaps = self.identify_evidence_gaps({'entities': entities})
                return FileMetadata(
                    file_path=str(file_path),
                    file_type=file_path.suffix[1:].upper(),
                    size=file_path.stat().st_size,
                    modified_at=datetime.fromtimestamp(file_path.stat().st_mtime),
                    metadata={
                        'entities': entities,
                        'summary': summary,
                        'ai_analysis': processed_data,
                        'timeline_entry': timeline_entry,
                        'evidence_gaps': gaps
                    },
                    hash=self._generate_file_hash(file_path)
                )
            else:
                return FileMetadata(  # Fallback for single doc processing
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

    def build_case_timeline(self, documents: List[FileMetadata]) -> Dict:
        """Generate a chronological timeline of case events from multiple documents"""
        timeline = []
        for doc in documents:
            entities = doc.metadata.get('entities', {})
            dates = [entity for entity in entities if 'date' in entity.lower()]
            for date_str in dates:
                # Simple date parsing; consider adding dateutil for robustness
                try:
                    date_obj = datetime.strptime(date_str, '%Y-%m-%d')  # Assumes date format; make configurable
                    timeline.append({'date': date_obj, 'description': doc.metadata.get('summary', 'No summary'), 'doc_path': doc.file_path})
                except ValueError:
                    continue  # Skip invalid dates
        return sorted(timeline, key=lambda x: x['date'])

    def identify_evidence_gaps(self, case_data: Dict) -> List[str]:
        """Detect gaps in evidence based on case data and legal requirements"""
        gaps = []
        # Example logic: check for missing document types or entities
        required_entities = ['plaintiff', 'defendant', 'evidence']  # Expand based on config
        for entity in required_entities:
            if not any(ent.lower().contains(entity) for ent in case_data.get('entities', [])):
                gaps.append(f"Missing information for {entity}")
        return gaps

    def synthesize_sigma_core(self, files: List[Path], case_id: str) -> Dict:
        '''Synthesize SIGMA_FILE_2 unified document from multiple files. Includes intro, timeline, violation table, witness dossiers, evidentiary strike zones, motion indexing, systemic failures, next actions, and contradiction sweeps. Tags sections with memory-linked identifiers and prepares for export.'''
        unified_doc = {
            'INTRO': self._build_intro(case_id),
            'TIMELINE': self.build_case_timeline([self.process_document(file) for file in files]),
            'VIOLATION_TABLE': self._detect_violations(),
            'WITNESS_ACTOR_DOSSIERS': self._build_actor_dossiers(),
            'EVIDENTIARY_STRIKE_ZONES': self._build_evidence_zones(files),
            'MOTION_THREADING_INDEX': self._build_motion_index(),
            'SYSTEMIC_FAILURES': self._detect_systemic_failures(),
            'NEXT_ACTIONS': self._generate_next_actions(),
        }
        
        # Run contradiction and suppression sweep
        unified_doc = self._run_contradiction_sweep(unified_doc)
        
        # Apply tagging with memory-linked identifiers
        tagged_doc = self._tag_sections(unified_doc)
        
        # Prepare for recursion and export
        return tagged_doc  # Can be exported to JSON, MD, etc.

    def _build_intro(self, case_id: str) -> str:
        return f'Case Scope and Mission Summary for {case_id}: Unifying all files into a single Sigma Core Document.'

    def _detect_violations(self) -> Dict:
        # Placeholder for violation detection; expand with legal data sources
        return {'Statutory': [], 'Procedural': [], 'Constitutional': []}  # To be populated based on analysis

    def _build_actor_dossiers(self) -> Dict:
        # Build dossiers from entities; enhance with more data
        return {'actors': []}  # Example structure

    def _build_evidence_zones(self, files: List[Path]) -> Dict:
        evidence = {}
        for file in files:
            metadata = self.process_document(file).metadata
            evidence[file.name] = metadata.get('ai_analysis', {})
        return evidence

    def _build_motion_index(self) -> Dict:
        # Index motions by stage; integrate with existing data
        return {'Filed': [], 'To-File': [], 'Drafts': []}

    def _detect_systemic_failures(self) -> List[str]:
        # Detect patterns like missing filings or inconsistencies
        return []

    def _generate_next_actions(self) -> Dict:
        # Strategic map based on analysis
        return {'actions': []}

    def _run_contradiction_sweep(self, doc: Dict) -> Dict:
        # Detect internal inconsistencies and suppressions
        contradictions = self.identify_contradictions(doc)
        for section in doc:
            doc[section] = self._annotate_for_contradictions(doc[section], contradictions)
        return doc

    def identify_contradictions(self, doc: Dict) -> List[str]:
        # Simple contradiction detection; expand with AI models
        contradictions = []
        # Example logic: check timeline for date conflicts
        if 'TIMELINE' in doc:
            dates = [event['date'] for event in doc['TIMELINE'] if 'date' in event]
            if len(set(dates)) != len(dates):  # Duplicate dates could indicate issues
                contradictions.append('Duplicate dates in timeline')
        return contradictions

    def _annotate_for_contradictions(self, section_data, contradictions) -> Any:
        # Annotate data with contradiction flags
        return section_data  # Add flags as needed

    def _tag_sections(self, doc: Dict) -> Dict:
        # Tag sections with memory-linked identifiers
        tagged = {}
        for key, value in doc.items():
            if key == 'TIMELINE':
                tagged[key] = [{**item, 'tags': ['#event/' + item.get('description', 'unknown')]} for item in value]
            # Add tagging for other sections similarly
        return tagged

    def export_sigma_core(self, doc: Dict, format_type: str = 'json') -> str:
        '''Export unified document in specified format.'''
        if format_type == 'json':
            return json.dumps(doc, indent=4)
        elif format_type == 'md':
            return self._to_markdown(doc)
        # Add support for PDF, DOCX, LaTeX if needed
        return ''

    def _to_markdown(self, doc: Dict) -> str:
        md_content = '# SIGMA_FILE_2 Unified Document\n'
        for section, content in doc.items():
            md_content += f'## {section}\n{json.dumps(content, indent=4)}\n'  # Simple MD conversion; enhance as needed
        return md_content

class LegalProcessingError(Exception):
    """Custom exception for legal document processing errors"""
    pass
