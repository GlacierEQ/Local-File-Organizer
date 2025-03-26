#!/usr/bin/env python3
"""Script to clean up old diagnostic reports and logs."""

import os
import sys
import logging
import shutil
from datetime import datetime, timedelta
from typing import Dict, List, Tuple
import json

class DiagnosticCleaner:
    """Manages cleanup of diagnostic files."""

    def __init__(self):
        """Initialize the diagnostic cleaner."""
        self.diagnostic_dir = "diagnostic_reports"
        self.logs_dir = "logs"
        self.logger = logging.getLogger(__name__)
        
        # Default retention periods
        self.retention_periods = {
            'critical': 90,  # Keep critical reports for 90 days
            'warning': 30,   # Keep warning reports for 30 days
            'healthy': 7     # Keep healthy reports for 7 days
        }

    def cleanup(self, dry_run: bool = True) -> Dict[str, List[str]]:
        """Clean up old diagnostic files."""
        results = {
            'deleted_reports': [],
            'deleted_logs': [],
            'kept_reports': [],
            'kept_logs': []
        }

        # Clean up diagnostic reports
        self._cleanup_reports(results, dry_run)
        
        # Clean up log files
        self._cleanup_logs(results, dry_run)

        return results

    def _cleanup_reports(self, results: Dict[str, List[str]], dry_run: bool):
        """Clean up old diagnostic reports."""
        if not os.path.exists(self.diagnostic_dir):
            self.logger.info(f"Diagnostic directory {self.diagnostic_dir} not found")
            return

        for filename in os.listdir(self.diagnostic_dir):
            if not filename.endswith('.json'):
                continue

            filepath = os.path.join(self.diagnostic_dir, filename)
            status, age = self._analyze_report(filepath)
            
            # Determine if file should be kept based on status and age
            retention_days = self.retention_periods.get(status, 7)
            if age > retention_days:
                if not dry_run:
                    try:
                        os.remove(filepath)
                        # Remove corresponding HTML report if it exists
                        html_path = filepath.replace('.json', '.html')
                        if os.path.exists(html_path):
                            os.remove(html_path)
                    except Exception as e:
                        self.logger.error(f"Error deleting {filepath}: {str(e)}")
                        continue
                results['deleted_reports'].append(
                    f"{filename} (Status: {status}, Age: {age} days)"
                )
            else:
                results['kept_reports'].append(
                    f"{filename} (Status: {status}, Age: {age} days)"
                )

    def _cleanup_logs(self, results: Dict[str, List[str]], dry_run: bool):
        """Clean up old log files."""
        if not os.path.exists(self.logs_dir):
            self.logger.info(f"Logs directory {self.logs_dir} not found")
            return

        for filename in os.listdir(self.logs_dir):
            if not filename.endswith('.log'):
                continue

            filepath = os.path.join(self.logs_dir, filename)
            age = self._get_file_age(filepath)
            
            # Keep logs for 30 days
            if age > 30:
                if not dry_run:
                    try:
                        os.remove(filepath)
                    except Exception as e:
                        self.logger.error(f"Error deleting {filepath}: {str(e)}")
                        continue
                results['deleted_logs'].append(
                    f"{filename} (Age: {age} days)"
                )
            else:
                results['kept_logs'].append(
                    f"{filename} (Age: {age} days)"
                )

    def _analyze_report(self, filepath: str) -> Tuple[str, int]:
        """Analyze a report file to determine its status and age."""
        try:
            with open(filepath, 'r') as f:
                report = json.load(f)
            
            # Get report status
            if 'test_results' in report:
                if report['test_results'].get('status') != 'success':
                    status = 'critical'
                elif any(report.get('dependencies', {}).get('missing', [])):
                    status = 'warning'
                else:
                    status = 'healthy'
            else:
                status = 'unknown'
            
            # Get file age
            age = self._get_file_age(filepath)
            
            return status, age
            
        except Exception as e:
            self.logger.error(f"Error analyzing {filepath}: {str(e)}")
            return 'unknown', 999  # Old enough to be deleted

    def _get_file_age(self, filepath: str) -> int:
        """Get the age of a file in days."""
        mtime = datetime.fromtimestamp(os.path.getmtime(filepath))
        age = (datetime.now() - mtime).days
        return age

    def get_disk_usage(self) -> Dict[str, int]:
        """Get disk usage information for diagnostic files."""
        usage = {
            'reports_size': 0,
            'logs_size': 0,
            'total_size': 0
        }

        # Get size of diagnostic reports
        if os.path.exists(self.diagnostic_dir):
            for dirpath, _, filenames in os.walk(self.diagnostic_dir):
                for f in filenames:
                    fp = os.path.join(dirpath, f)
                    usage['reports_size'] += os.path.getsize(fp)

        # Get size of log files
        if os.path.exists(self.logs_dir):
            for dirpath, _, filenames in os.walk(self.logs_dir):
                for f in filenames:
                    fp = os.path.join(dirpath, f)
                    usage['logs_size'] += os.path.getsize(fp)

        usage['total_size'] = usage['reports_size'] + usage['logs_size']
        return usage

def format_size(size: int) -> str:
    """Format size in bytes to human readable format."""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size < 1024:
            return f"{size:.2f} {unit}"
        size /= 1024
    return f"{size:.2f} TB"

def main():
    """Run the diagnostic cleanup."""
    # Configure logging
    logging.basicConfig(level=logging.INFO)
    
    cleaner = DiagnosticCleaner()
    
    # Show current disk usage
    print("Current Disk Usage:")
    usage = cleaner.get_disk_usage()
    print(f"Diagnostic Reports: {format_size(usage['reports_size'])}")
    print(f"Log Files: {format_size(usage['logs_size'])}")
    print(f"Total: {format_size(usage['total_size'])}")
    
    # Ask for confirmation
    print("\nRetention Policy:")
    print("- Critical reports: 90 days")
    print("- Warning reports: 30 days")
    print("- Healthy reports: 7 days")
    print("- Log files: 30 days")
    
    # Dry run first
    print("\nAnalyzing files to clean up...")
    results = cleaner.cleanup(dry_run=True)
    
    if not any(results['deleted_reports'] + results['deleted_logs']):
        print("\nNo files need cleaning up!")
        return
    
    print("\nFiles to be deleted:")
    if results['deleted_reports']:
        print("\nDiagnostic Reports:")
        for report in results['deleted_reports']:
            print(f"- {report}")
    
    if results['deleted_logs']:
        print("\nLog Files:")
        for log in results['deleted_logs']:
            print(f"- {log}")
    
    # Ask for confirmation
    if input("\nProceed with cleanup? (y/N): ").lower().strip() != 'y':
        print("Cleanup cancelled")
        return
    
    # Perform actual cleanup
    print("\nPerforming cleanup...")
    results = cleaner.cleanup(dry_run=False)
    
    # Show new disk usage
    print("\nNew Disk Usage:")
    usage = cleaner.get_disk_usage()
    print(f"Diagnostic Reports: {format_size(usage['reports_size'])}")
    print(f"Log Files: {format_size(usage['logs_size'])}")
    print(f"Total: {format_size(usage['total_size'])}")
    
    print("\nCleanup complete!")

if __name__ == "__main__":
    main()
