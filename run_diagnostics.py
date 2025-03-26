#!/usr/bin/env python3
"""Wrapper script to run system diagnostics with proper dependencies."""

import os
import sys
import subprocess
import logging
from datetime import datetime

def setup_diagnostic_environment():
    """Ensure all diagnostic dependencies are installed."""
    print("Setting up diagnostic environment...")
    
    # Install diagnostic requirements
    try:
        subprocess.run(
            [sys.executable, "-m", "pip", "install", "-r", "requirements-diagnostic.txt"],
            check=True,
            capture_output=True,
            text=True
        )
        print("Dependencies installed successfully")
    except subprocess.CalledProcessError as e:
        print(f"Error installing dependencies: {e.stderr}")
        sys.exit(1)

def run_diagnostics():
    """Run the diagnostic report generator."""
    print("\nRunning diagnostics...")
    
    try:
        from generate_diagnostic_report import main as generate_report
        generate_report()
    except ImportError as e:
        print(f"Error importing diagnostic module: {str(e)}")
        print("Please ensure all dependencies are installed.")
        sys.exit(1)
    except Exception as e:
        print(f"Error running diagnostics: {str(e)}")
        logging.error("Diagnostic run failed", exc_info=True)
        sys.exit(1)

def setup_logging():
    """Configure logging for diagnostic run."""
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    log_dir = "logs"
    os.makedirs(log_dir, exist_ok=True)
    
    log_file = os.path.join(log_dir, f"diagnostic_run_{timestamp}.log")
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    )
    
    return log_file

def print_system_check():
    """Print basic system information before running diagnostics."""
    import platform
    
    print("\nSystem Check:")
    print(f"Python version: {sys.version.split()[0]}")
    print(f"Operating system: {platform.system()} {platform.version()}")
    print(f"Machine: {platform.machine()}")
    print(f"Processor: {platform.processor()}")

def main():
    """Main entry point for running diagnostics."""
    print("AI Document Processor Diagnostics")
    print("================================")
    
    # Setup logging
    log_file = setup_logging()
    logging.info("Starting diagnostic run")
    
    try:
        # Print system information
        print_system_check()
        
        # Setup environment and run diagnostics
        setup_diagnostic_environment()
        run_diagnostics()
        
        print(f"\nDiagnostic run completed successfully!")
        print(f"Log file: {log_file}")
        
    except KeyboardInterrupt:
        print("\nDiagnostic run interrupted by user")
        logging.warning("Diagnostic run interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\nError during diagnostic run: {str(e)}")
        logging.error("Diagnostic run failed", exc_info=True)
        print(f"\nCheck the log file for details: {log_file}")
        sys.exit(1)

if __name__ == "__main__":
    main()
