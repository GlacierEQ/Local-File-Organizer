#!/usr/bin/env python3
"""Unified management script for the AI Document Processing System."""

import os
import sys
import logging
import argparse
import subprocess
from datetime import datetime
from typing import Optional, List

class SystemManager:
    """Manages all system operations and maintenance tasks."""

    def __init__(self):
        """Initialize the system manager."""
        self.logger = logging.getLogger(__name__)
        self._setup_logging()

    def _setup_logging(self):
        """Configure logging."""
        log_dir = "logs"
        os.makedirs(log_dir, exist_ok=True)
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(
                    os.path.join(
                        log_dir,
                        f"system_manager_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
                    )
                ),
                logging.StreamHandler()
            ]
        )

    def run_command(self, script: str, args: List[str] = None) -> bool:
        """Run a Python script with arguments."""
        try:
            cmd = [sys.executable, script]
            if args:
                cmd.extend(args)
            
            self.logger.info(f"Running: {' '.join(cmd)}")
            subprocess.run(cmd, check=True)
            return True
            
        except subprocess.CalledProcessError as e:
            self.logger.error(f"Error running {script}: {str(e)}")
            return False
        except Exception as e:
            self.logger.error(f"Unexpected error running {script}: {str(e)}")
            return False

    def setup_environment(self):
        """Set up the system environment."""
        print("\nSetting up environment...")
        return self.run_command("setup_environment.py")

    def verify_setup(self):
        """Verify system setup."""
        print("\nVerifying setup...")
        return self.run_command("verify_setup.py")

    def run_diagnostics(self):
        """Run system diagnostics."""
        print("\nRunning diagnostics...")
        return self.run_command("run_diagnostics.py")

    def view_diagnostic_results(self):
        """View diagnostic results."""
        print("\nViewing diagnostic results...")
        return self.run_command("view_diagnostic_results.py")

    def cleanup_diagnostics(self):
        """Clean up old diagnostic files."""
        print("\nCleaning up diagnostic files...")
        return self.run_command("cleanup_diagnostics.py")

    def manage_schedule(self, action: str):
        """Manage diagnostic schedules."""
        print(f"\nManaging schedule: {action}")
        return self.run_command("schedule_diagnostics.py", [f"--{action}"])

    def run_benchmarks(self):
        """Run system benchmarks."""
        print("\nRunning benchmarks...")
        return self.run_command("run_benchmarks.py")

    def process_documents(self, input_dir: str, output_dir: str):
        """Process documents using the AI system."""
        print(f"\nProcessing documents from {input_dir}...")
        return self.run_command(
            "example_ai_processing.py",
            [input_dir, output_dir]
        )

def main():
    """Main entry point for system management."""
    parser = argparse.ArgumentParser(
        description="AI Document Processing System Management"
    )
    
    # Create command groups
    setup_group = parser.add_argument_group('Setup and Verification')
    diag_group = parser.add_argument_group('Diagnostics and Maintenance')
    proc_group = parser.add_argument_group('Document Processing')
    schedule_group = parser.add_argument_group('Schedule Management')
    
    # Setup and Verification arguments
    setup_group.add_argument(
        '--setup',
        action='store_true',
        help='Set up the system environment'
    )
    setup_group.add_argument(
        '--verify',
        action='store_true',
        help='Verify system setup'
    )
    
    # Diagnostics and Maintenance arguments
    diag_group.add_argument(
        '--diagnose',
        action='store_true',
        help='Run system diagnostics'
    )
    diag_group.add_argument(
        '--view-diagnostics',
        action='store_true',
        help='View diagnostic results'
    )
    diag_group.add_argument(
        '--cleanup',
        action='store_true',
        help='Clean up old diagnostic files'
    )
    diag_group.add_argument(
        '--benchmark',
        action='store_true',
        help='Run system benchmarks'
    )
    
    # Document Processing arguments
    proc_group.add_argument(
        '--process',
        nargs=2,
        metavar=('INPUT_DIR', 'OUTPUT_DIR'),
        help='Process documents from INPUT_DIR to OUTPUT_DIR'
    )
    
    # Schedule Management arguments
    schedule_group.add_argument(
        '--schedule',
        choices=['configure', 'show', 'run'],
        help='Manage diagnostic schedules'
    )
    
    args = parser.parse_args()
    
    # If no arguments provided, show help
    if len(sys.argv) == 1:
        parser.print_help()
        return
    
    manager = SystemManager()
    success = True
    
    # Handle setup and verification
    if args.setup:
        success &= manager.setup_environment()
    if args.verify:
        success &= manager.verify_setup()
    
    # Handle diagnostics and maintenance
    if args.diagnose:
        success &= manager.run_diagnostics()
    if args.view_diagnostics:
        success &= manager.view_diagnostic_results()
    if args.cleanup:
        success &= manager.cleanup_diagnostics()
    if args.benchmark:
        success &= manager.run_benchmarks()
    
    # Handle document processing
    if args.process:
        success &= manager.process_documents(*args.process)
    
    # Handle schedule management
    if args.schedule:
        success &= manager.manage_schedule(args.schedule)
    
    # Set exit code based on success
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
