import json
import re
from typing import Dict, Any, Optional, List


class HawaiiLaws:
    """Class to manage Hawaii laws, rules of procedure, and rules of evidence.
    
    Provides methods for:
    - Case number generation and validation
    - Document type classification
    - Legal document metadata validation
    - Accessing laws, rules, and deadlines
    """


    def __init__(self, filepath: str):
        """Initialize with the path to the laws JSON file."""
        self.filepath = filepath
        self.laws_data = self.load_laws()

    def load_laws(self) -> Dict[str, Any]:
        """Load laws from the JSON file."""
        with open(self.filepath, 'r') as f:
            return json.load(f)

    def get_law(self, law_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve a specific law by its ID."""
        return self.laws_data['laws'].get(law_id)

    def get_rule(self, rule_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve a specific rule of evidence by its ID."""
        return self.laws_data['rules_of_evidence'].get(rule_id)

    def get_procedure(self, procedure_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve a specific rule of procedure by its ID."""
        return self.laws_data['rules_of_procedure'].get(procedure_id)

    def get_deadline(self, deadline_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve a specific deadline by its ID."""
        return self.laws_data['deadlines'].get(deadline_id)

    def generate_case_number(self) -> str:
        """Generate a valid Hawaii case number with current year."""
        import datetime
        year = datetime.datetime.now().year
        sequence = len(self.laws_data['case_numbers']) + 1
        case_num = f"{year}-CA-{sequence:04d}"
        self.laws_data['case_numbers'].append(case_num)
        return case_num

    def validate_case_number(self, case_number: str) -> bool:
        """Validate a Hawaii case number format."""
        pattern = r"^\d{4}-[A-Z]{2}-\d{4}$|^HI-\d{4}-\d{3}$"
        return re.match(pattern, case_number) is not None

    def suggest_valid_case_number(self, invalid_number: str) -> str:
        """Suggest a valid case number from invalid input."""
        numbers = re.findall(r"\d+", invalid_number)
        if len(numbers) >= 2:
            return f"{numbers[0]}-CA-{numbers[1][-4:].zfill(4)}"
        return self.generate_case_number()

    def get_document_type_by_id(self, type_id: int) -> str:
        """Get document type name from classifier ID."""
        return self.laws_data['document_types'].get(str(type_id), "unknown")

    def list_laws(self) -> Dict[str, Any]:

        """List all laws available in the database."""
        return self.laws_data['laws']

    def list_rules(self) -> Dict[str, Any]:
        """List all rules of evidence available in the database."""
        return self.laws_data['rules_of_evidence']

    def list_procedures(self) -> Dict[str, Any]:
        """List all rules of procedure available in the database."""
        return self.laws_data['rules_of_procedure']

    def list_deadlines(self) -> Dict[str, Any]:
        """List all deadlines available in the database."""
        return self.laws_data['deadlines']

# Example usage
if __name__ == "__main__":
    hawaii_laws = HawaiiLaws('hawaii_laws.json')
    print("Laws:", hawaii_laws.list_laws())
    print("Rules of Evidence:", hawaii_laws.list_rules())
    print("Rules of Procedure:", hawaii_laws.list_procedures())
    print("Deadlines:", hawaii_laws.list_deadlines())
