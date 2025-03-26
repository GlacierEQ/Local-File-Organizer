import re
from typing import Dict, List, Optional, Tuple
import pytesseract
from PIL import Image
import os
import docx
from data_processing_common import sanitize_filename
from datetime import datetime

class LegalDocumentProcessor:
    """Specialized processor for legal documents with focus on specific case types."""
    
    CASE_TYPES = {
        'divorce': [
            'divorce', 'dissolution', 'marriage', 'separation', 'alimony', 'spousal support',
            'marital property', 'community property', 'settlement agreement'
        ],
        'custody': [
            'custody', 'visitation', 'child support', 'parenting time', 'guardian ad litem',
            'best interests', 'parental rights', 'joint custody', 'sole custody'
        ],
        'labor': [
            'employment', 'discrimination', 'workplace', 'compensation', 'harassment',
            'wrongful termination', 'retaliation', 'wage', 'overtime', 'FMLA', 'ADA',
            'reasonable accommodation', 'hostile work environment'
        ],
        'malpractice': [
            'negligence', 'medical', 'professional', 'standard of care', 'injury',
            'misdiagnosis', 'informed consent', 'breach of duty', 'damages',
            'expert witness', 'causation'
        ],
        'defamation': [
            'libel', 'slander', 'reputation', 'damages', 'malice', 'false statement',
            'public figure', 'actual malice', 'defamatory', 'publication'
        ]
    }

    LEGAL_ENTITIES = {
        'parties': r'(?:Plaintiff|Defendant|Petitioner|Respondent|Appellant|Appellee)(?:s)?\s*,?\s*([^,\.]+)',
        'case_numbers': r'(?:Case|Docket|File)\s*(?:No\.|Number|#)\s*[\w-]+',
        'dates': r'\b(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2},\s+\d{4}\b',
        'courts': r'(?:Supreme|District|Circuit|Federal|State|County|Appeals)\s+Court',
        'citations': r'\d+\s+(?:U\.S\.|F\.\d[d|th]|F\.Supp\.\d[d|th]|S\.Ct\.|L\.Ed\.\d[d|th])\s+\d+'
    }

    def __init__(self):
        self.metadata = {
            'case_type': None,
            'parties': [],
            'case_numbers': [],
            'filing_date': None,
            'court': None,
            'citations': [],
            'key_dates': [],
            'monetary_values': [],
            'key_terms': set()
        }

    def extract_metadata(self, text: str) -> Dict:
        """Extract comprehensive metadata from legal document."""
        # Identify case type
        self.metadata['case_type'] = self._identify_case_type(text)
        
        # Extract entities using patterns
        for entity_type, pattern in self.LEGAL_ENTITIES.items():
            matches = re.finditer(pattern, text)
            self.metadata[entity_type] = [match.group(0) for match in matches]

        # Extract monetary values
        monetary_pattern = r'\$\d{1,3}(?:,\d{3})*(?:\.\d{2})?'
        self.metadata['monetary_values'] = re.findall(monetary_pattern, text)

        # Extract key terms based on case type
        if self.metadata['case_type']:
            self.metadata['key_terms'] = self._extract_case_specific_terms(text)

        # Extract filing date
        self.metadata['filing_date'] = self._extract_filing_date(text)

        return self.metadata

    def _identify_case_type(self, text: str) -> str:
        """Identify the type of legal case based on key terminology."""
        scores = {case: 0 for case in self.CASE_TYPES.keys()}
        
        for case_type, keywords in self.CASE_TYPES.items():
            for keyword in keywords:
                matches = len(re.findall(rf'\b{keyword}\b', text.lower()))
                scores[case_type] += matches
        
        return max(scores.items(), key=lambda x: x[1])[0] if any(scores.values()) else None

    def _extract_case_specific_terms(self, text: str) -> set:
        """Extract terms specific to the identified case type."""
        case_type = self.metadata['case_type']
        if not case_type:
            return set()

        terms = set()
        keywords = self.CASE_TYPES[case_type]
        
        # Create context windows around keyword matches
        for keyword in keywords:
            matches = re.finditer(rf'\b{keyword}\b', text.lower())
            for match in matches:
                start = max(0, match.start() - 50)
                end = min(len(text), match.end() + 50)
                context = text[start:end]
                # Extract potential legal terms (capitalized words)
                legal_terms = re.findall(r'\b[A-Z][a-zA-Z]+\b', context)
                terms.update(legal_terms)

        return terms

    def _extract_filing_date(self, text: str) -> Optional[str]:
        """Extract the filing date from the document text."""
        date_pattern = r'\b(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2},\s+\d{4}\b'
        match = re.search(date_pattern, text)
        return match.group(0) if match else None

    def generate_summary(self) -> str:
        """Generate a structured summary of the legal document."""
        summary_parts = []
        
        if self.metadata['case_type']:
            summary_parts.append(f"Case Type: {self.metadata['case_type'].title()}")
        
        if self.metadata['parties']:
            summary_parts.append("Parties Involved:")
            for party in self.metadata['parties']:
                summary_parts.append(f"- {party}")
        
        if self.metadata['case_numbers']:
            summary_parts.append(f"Case Number: {self.metadata['case_numbers'][0]}")
        
        if self.metadata['court']:
            summary_parts.append(f"Court: {self.metadata['court']}")
        
        if self.metadata['key_dates']:
            summary_parts.append("Key Dates:")
            for date in self.metadata['key_dates']:
                summary_parts.append(f"- {date}")
        
        if self.metadata['monetary_values']:
            summary_parts.append("Monetary Values Mentioned:")
            for value in self.metadata['monetary_values']:
                summary_parts.append(f"- {value}")
        
        if self.metadata['key_terms']:
            summary_parts.append("Key Legal Terms:")
            for term in sorted(self.metadata['key_terms'])[:10]:  # Limit to top 10 terms
                summary_parts.append(f"- {term}")
        
        return "\n".join(summary_parts)

    def suggest_filename(self) -> str:
        """Generate a filename based on document metadata."""
        components = []
        
        # Add case type if available
        if self.metadata['case_type']:
            components.append(self.metadata['case_type'])
        
        # Add first party name if available
        if self.metadata['parties']:
            first_party = re.sub(r'(?:Plaintiff|Defendant|Petitioner|Respondent)(?:s)?,?\s*', '', 
                               self.metadata['parties'][0])
            components.append(first_party.strip())
        
        # Add case number if available
        if self.metadata['case_numbers']:
            case_num = re.sub(r'(?:Case|Docket|File)\s*(?:No\.|Number|#)\s*', '', 
                            self.metadata['case_numbers'][0])
            components.append(case_num.strip())
        
        # Add date if available
        if self.metadata['filing_date']:
            date_str = datetime.strptime(self.metadata['filing_date'], 
                                       '%B %d, %Y').strftime('%Y%m%d')
            components.append(date_str)
        
        filename = '_'.join(components) if components else 'legal_document'
        return sanitize_filename(filename)

    def suggest_folder_structure(self) -> str:
        """Suggest a folder structure based on document metadata."""
        if not self.metadata['case_type']:
            return 'legal_documents/uncategorized'
            
        base_path = f"legal_documents/{self.metadata['case_type']}"
        
        # Add year subfolder if filing date is available
        if self.metadata['filing_date']:
            year = datetime.strptime(self.metadata['filing_date'], 
                                   '%B %d, %Y').strftime('%Y')
            base_path = f"{base_path}/{year}"
            
        return base_path
