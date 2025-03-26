#!/usr/bin/env python3
"""Script to verify the AI document processing system setup."""

import os
import sys
import subprocess
import logging
import importlib
from typing import Dict, List
import json

class SetupVerifier:
    """Verifies the setup of the AI document processing system."""

    def __init__(self):
        """Initialize the verifier."""
        self.logger = logging.getLogger(__name__)
        self.results = {
            'dependencies': {'status': False, 'details': []},
            'tesseract': {'status': False, 'details': []},
            'sample_files': {'status': False, 'details': []},
            'configuration': {'status': False, 'details': []},
            'directories': {'status': False, 'details': []}
        }

    def verify_all(self) -> Dict:
        """Run all verification checks."""
        self.verify_dependencies()
        self.verify_tesseract()
        self.verify_sample_files()
        self.verify_configuration()
        self.verify_directories()
        return self.results

    def verify_dependencies(self) -> None:
        """Verify Python package dependencies."""
        self.logger.info("Checking dependencies...")
        
        required_files = [
            'requirements-ai.txt',
            'requirements-test.txt',
            'requirements-benchmark.txt'
        ]
        
        for req_file in required_files:
            if not os.path.exists(req_file):
                self.results['dependencies']['details'].append(
                    f"Missing requirements file: {req_file}"
                )
                continue
                
            try:
                with open(req_file, 'r') as f:
                    requirements = [
                        line.strip() for line in f 
                        if line.strip() and not line.startswith('#') and not line.startswith('-r')
                    ]
                
                for req in requirements:
                    try:
                        importlib.import_module(req.split('>=')[0])
                        self.results['dependencies']['details'].append(
                            f"✓ {req} installed"
                        )
                    except ImportError:
                        self.results['dependencies']['details'].append(
                            f"✗ {req} not installed"
                        )
                        
            except Exception as e:
                self.results['dependencies']['details'].append(
                    f"Error checking {req_file}: {str(e)}"
                )
        
        self.results['dependencies']['status'] = not any(
            '✗' in detail for detail in self.results['dependencies']['details']
        )

    def verify_tesseract(self) -> None:
        """Verify Tesseract OCR installation."""
        self.logger.info("Checking Tesseract OCR...")
        
        try:
            import pytesseract
            tesseract_version = pytesseract.get_tesseract_version()
            self.results['tesseract']['details'].append(
                f"Tesseract version: {tesseract_version}"
            )
            self.results['tesseract']['status'] = True
        except Exception as e:
            self.results['tesseract']['details'].append(
                f"Error checking Tesseract: {str(e)}"
            )
            self.results['tesseract']['status'] = False

    def verify_sample_files(self) -> None:
        """Verify sample document files."""
        self.logger.info("Checking sample files...")
        
        sample_dir = "sample_data/legal_documents"
        required_samples = [
            'case_law_example.txt',
            'docket_entry_example.txt',
            'pleading_example.txt',
            'exhibit_example.txt'
        ]
        
        if not os.path.exists(sample_dir):
            self.results['sample_files']['details'].append(
                f"Missing sample directory: {sample_dir}"
            )
            return
            
        for sample in required_samples:
            path = os.path.join(sample_dir, sample)
            if os.path.exists(path):
                self.results['sample_files']['details'].append(
                    f"✓ Found {sample}"
                )
            else:
                self.results['sample_files']['details'].append(
                    f"✗ Missing {sample}"
                )
        
        self.results['sample_files']['status'] = not any(
            '✗' in detail for detail in self.results['sample_files']['details']
        )

    def verify_configuration(self) -> None:
        """Verify configuration files and settings."""
        self.logger.info("Checking configuration...")
        
        required_files = [
            'config_ai.py',
            'config_ai_utils.py'
        ]
        
        for config_file in required_files:
            if os.path.exists(config_file):
                self.results['configuration']['details'].append(
                    f"✓ Found {config_file}"
                )
            else:
                self.results['configuration']['details'].append(
                    f"✗ Missing {config_file}"
                )
        
        try:
            from config_ai_utils import validate_config_file
            config_validation = validate_config_file("config_ai.py")
            self.results['configuration']['details'].append(
                f"Configuration validation results: {json.dumps(config_validation, indent=2)}"
            )
        except Exception as e:
            self.results['configuration']['details'].append(
                f"Error validating configuration: {str(e)}"
            )
        
        self.results['configuration']['status'] = not any(
            '✗' in detail for detail in self.results['configuration']['details']
        )

    def verify_directories(self) -> None:
        """Verify required directories exist."""
        self.logger.info("Checking directories...")
        
        required_dirs = [
            'documents',
            'consolidated_documents',
            'benchmark_results',
            'tests',
            'benchmarks'
        ]
        
        for directory in required_dirs:
            if os.path.exists(directory):
                self.results['directories']['details'].append(
                    f"✓ Found {directory}"
                )
            else:
                os.makedirs(directory, exist_ok=True)
                self.results['directories']['details'].append(
                    f"Created {directory}"
                )
        
        self.results['directories']['status'] = True

def main():
    """Run the setup verification."""
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

    print("Verifying AI Document Processing System Setup...")
    print("=============================================")
    
    verifier = SetupVerifier()
    results = verifier.verify_all()
    
    print("\nVerification Results:")
    print("===================")
    
    for category, result in results.items():
        print(f"\n{category.upper()}:")
        print(f"Status: {'✓ PASS' if result['status'] else '✗ FAIL'}")
        print("Details:")
        for detail in result['details']:
            print(f"  {detail}")
    
    # Overall status
    all_passed = all(result['status'] for result in results.values())
    
    print("\nOVERALL STATUS:", "✓ PASS" if all_passed else "✗ FAIL")
    
    if not all_passed:
        print("\nRecommended Actions:")
        if not results['dependencies']['status']:
            print("- Run: pip install -r requirements-ai.txt")
        if not results['tesseract']['status']:
            print("- Install Tesseract OCR")
        if not results['sample_files']['status']:
            print("- Check sample_data/legal_documents directory")
        if not results['configuration']['status']:
            print("- Verify configuration files")

if __name__ == "__main__":
    main()
