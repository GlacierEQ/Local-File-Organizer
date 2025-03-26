#!/usr/bin/env python3
"""Script to set up the AI document processing environment."""

import os
import sys
import subprocess
import platform
import logging
from datetime import datetime

class EnvironmentSetup:
    """Handles the setup of the AI document processing environment."""

    def __init__(self):
        """Initialize the setup handler."""
        self.logger = logging.getLogger(__name__)
        self.system = platform.system().lower()
        self.python_version = platform.python_version()

    def setup_all(self):
        """Run all setup steps."""
        try:
            self.check_python_version()
            self.create_directories()
            self.install_dependencies()
            self.install_tesseract()
            self.verify_installation()
            print("\nSetup completed successfully!")
            
        except Exception as e:
            self.logger.error(f"Setup failed: {str(e)}")
            print(f"\nError during setup: {str(e)}")
            sys.exit(1)

    def check_python_version(self):
        """Check if Python version is compatible."""
        print("\nChecking Python version...")
        major, minor, _ = map(int, self.python_version.split('.'))
        
        if major < 3 or (major == 3 and minor < 7):
            raise Exception(
                f"Python 3.7+ required, but found {self.python_version}"
            )
        self.logger.info(f"Python version {self.python_version} is compatible")

    def create_directories(self):
        """Create necessary directories."""
        print("\nCreating directories...")
        directories = [
            'documents',
            'consolidated_documents',
            'benchmark_results',
            'logs'
        ]
        
        for directory in directories:
            os.makedirs(directory, exist_ok=True)
            self.logger.info(f"Created directory: {directory}")

    def install_dependencies(self):
        """Install Python package dependencies."""
        print("\nInstalling Python dependencies...")
        requirements_files = [
            'requirements-ai.txt',
            'requirements-test.txt',
            'requirements-benchmark.txt'
        ]
        
        for req_file in requirements_files:
            if not os.path.exists(req_file):
                self.logger.warning(f"Missing {req_file}, skipping...")
                continue
                
            print(f"\nInstalling dependencies from {req_file}...")
            try:
                subprocess.run(
                    [sys.executable, "-m", "pip", "install", "-r", req_file],
                    check=True
                )
                self.logger.info(f"Installed dependencies from {req_file}")
            except subprocess.CalledProcessError as e:
                self.logger.error(f"Error installing from {req_file}: {str(e)}")
                raise Exception(f"Failed to install dependencies from {req_file}")

    def install_tesseract(self):
        """Install Tesseract OCR based on the operating system."""
        print("\nInstalling Tesseract OCR...")
        
        if self.system == 'windows':
            print("Please install Tesseract OCR manually:")
            print("1. Download from: https://github.com/UB-Mannheim/tesseract/wiki")
            print("2. Run the installer")
            print("3. Add Tesseract to your system PATH")
            input("Press Enter once Tesseract is installed...")
            
        elif self.system == 'darwin':  # macOS
            try:
                subprocess.run(['brew', 'install', 'tesseract'], check=True)
                self.logger.info("Installed Tesseract via Homebrew")
            except subprocess.CalledProcessError:
                print("Please install Tesseract manually:")
                print("1. Install Homebrew from https://brew.sh")
                print("2. Run: brew install tesseract")
                raise Exception("Failed to install Tesseract")
                
        elif self.system == 'linux':
            try:
                subprocess.run(
                    ['sudo', 'apt-get', 'update'],
                    check=True
                )
                subprocess.run(
                    ['sudo', 'apt-get', 'install', '-y', 'tesseract-ocr'],
                    check=True
                )
                self.logger.info("Installed Tesseract via apt")
            except subprocess.CalledProcessError:
                print("Please install Tesseract manually:")
                print("Run: sudo apt-get install tesseract-ocr")
                raise Exception("Failed to install Tesseract")

    def verify_installation(self):
        """Verify the installation was successful."""
        print("\nVerifying installation...")
        
        # Verify Python packages
        try:
            import pytesseract
            import docx
            import PIL
            import numpy
            import matplotlib
            self.logger.info("All required Python packages are installed")
        except ImportError as e:
            self.logger.error(f"Missing Python package: {str(e)}")
            raise Exception(f"Missing required package: {str(e)}")
        
        # Verify Tesseract
        try:
            import pytesseract
            version = pytesseract.get_tesseract_version()
            self.logger.info(f"Tesseract version {version} is installed")
            print(f"Tesseract version {version} is installed")
        except Exception as e:
            self.logger.error(f"Tesseract verification failed: {str(e)}")
            raise Exception("Tesseract verification failed")

def main():
    """Main entry point for setup."""
    # Configure logging
    log_file = f"logs/setup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
    os.makedirs("logs", exist_ok=True)
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    )

    print("Setting up AI Document Processing Environment")
    print("===========================================")
    
    setup = EnvironmentSetup()
    setup.setup_all()
    
    print("\nSetup log saved to:", log_file)
    print("\nNext steps:")
    print("1. Run verify_setup.py to confirm everything is working")
    print("2. Try processing the sample documents")
    print("3. Check the documentation for usage examples")

if __name__ == "__main__":
    main()
