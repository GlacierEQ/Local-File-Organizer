from pathlib import Path
from typing import Dict, Any, TypedDict, Optional
from legal_ai_processor import LegalAIProcessor

class CaseAnalysis(TypedDict):
    documents: list[Dict[str, Any]]
    timeline: list[Dict[str, str]]
    legal_issues: set[str]


class CaseAnalyzer:
    """Analyzes legal case documents and maintains context."""
    
    def __init__(self, laws_file: str):
        self.processor = LegalAIProcessor(laws_file)
        self.case_memory = {}

    def analyze_case_file(self, file_path: str) -> Optional[CaseAnalysis]:
        """Process a case document and maintain analysis context."""
        try:
            analysis = self.processor.process_document(file_path)
            if not analysis or 'metadata' not in analysis:
                return None
                
            case_id = analysis['metadata'].get('case_number')
            if not case_id:
                return None

            if case_id not in self.case_memory:
                self.case_memory[case_id] = CaseAnalysis(
                    documents=[],
                    timeline=[],
                    legal_issues=set()
                )
                
            self.case_memory[case_id]['documents'].append(analysis)
            self._update_timeline(case_id, analysis)
            self._extract_legal_issues(case_id, analysis)
            
            return self.case_memory[case_id]
        except (KeyError, ValueError, FileNotFoundError) as e:
            print(f"Case analysis failed: {str(e)}")
            return None


    def _update_timeline(self, case_id: str, analysis: Dict[str, Any]):
        """Track document filing dates in timeline."""
        filing_date = analysis['metadata']['filing_date']
        self.case_memory[case_id]['timeline'].append({
            'date': filing_date,
            'document_type': analysis['metadata']['document_type'],
            'file_path': analysis['file_path']
        })
        self.case_memory[case_id]['timeline'].sort(key=lambda x: x['date'])

    def _extract_legal_issues(self, case_id: str, analysis: Dict[str, Any]):
        """Extract and categorize legal issues from analysis."""
        for issue in analysis.get('legal_issues', []):
            self.case_memory[case_id]['legal_issues'].add(issue)
