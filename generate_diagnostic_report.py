#!/usr/bin/env python3
"""Script to generate a diagnostic report for the AI document processing system."""

import os
import sys
import platform
import json
import logging
import subprocess
from datetime import datetime
import psutil
import pkg_resources
from typing import Dict, List, Any

class DiagnosticReport:
    """Generates comprehensive diagnostic reports."""

    def __init__(self):
        """Initialize the diagnostic reporter."""
        self.timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        self.report_dir = "diagnostic_reports"
        self.report_path = os.path.join(
            self.report_dir,
            f"diagnostic_report_{self.timestamp}.json"
        )
        os.makedirs(self.report_dir, exist_ok=True)
        self.logger = logging.getLogger(__name__)

    def generate_report(self) -> Dict[str, Any]:
        """Generate a complete diagnostic report."""
        report = {
            'timestamp': self.timestamp,
            'system_info': self._get_system_info(),
            'python_info': self._get_python_info(),
            'dependencies': self._get_dependency_info(),
            'configuration': self._get_configuration_info(),
            'directories': self._get_directory_info(),
            'resource_usage': self._get_resource_usage(),
            'recent_logs': self._get_recent_logs(),
            'test_results': self._run_quick_tests()
        }

        # Save report
        with open(self.report_path, 'w') as f:
            json.dump(report, f, indent=2)

        # Generate markdown summary
        self._generate_markdown_summary(report)

        return report

    def _get_system_info(self) -> Dict[str, str]:
        """Gather system information."""
        return {
            'os': platform.platform(),
            'architecture': platform.machine(),
            'processor': platform.processor(),
            'cpu_count': psutil.cpu_count(),
            'memory_total': psutil.virtual_memory().total,
            'disk_usage': self._get_disk_usage()
        }

    def _get_python_info(self) -> Dict[str, str]:
        """Gather Python environment information."""
        return {
            'version': sys.version,
            'executable': sys.executable,
            'path': sys.path,
            'pip_version': pkg_resources.get_distribution('pip').version
        }

    def _get_dependency_info(self) -> Dict[str, List[str]]:
        """Check installed dependencies."""
        dependencies = {
            'installed': [],
            'missing': [],
            'version_conflicts': []
        }

        requirement_files = [
            'requirements-ai.txt',
            'requirements-test.txt',
            'requirements-benchmark.txt'
        ]

        for req_file in requirement_files:
            if not os.path.exists(req_file):
                continue

            with open(req_file, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#') and not line.startswith('-r'):
                        try:
                            pkg_name = line.split('>=')[0]
                            pkg = pkg_resources.get_distribution(pkg_name)
                            dependencies['installed'].append(
                                f"{pkg.key}=={pkg.version}"
                            )
                        except pkg_resources.DistributionNotFound:
                            dependencies['missing'].append(pkg_name)
                        except Exception as e:
                            dependencies['version_conflicts'].append(
                                f"{pkg_name}: {str(e)}"
                            )

        return dependencies

    def _get_configuration_info(self) -> Dict[str, Any]:
        """Gather configuration information."""
        config_info = {
            'files_present': [],
            'files_missing': [],
            'validation_results': None
        }

        config_files = ['config_ai.py', 'config_ai_utils.py']
        for file in config_files:
            if os.path.exists(file):
                config_info['files_present'].append(file)
            else:
                config_info['files_missing'].append(file)

        try:
            from config_ai_utils import validate_config_file
            config_info['validation_results'] = validate_config_file("config_ai.py")
        except Exception as e:
            config_info['validation_results'] = f"Error validating config: {str(e)}"

        return config_info

    def _get_directory_info(self) -> Dict[str, List[str]]:
        """Check directory structure and contents."""
        directories = {
            'present': [],
            'missing': [],
            'empty': [],
            'file_counts': {}
        }

        required_dirs = [
            'documents',
            'consolidated_documents',
            'benchmark_results',
            'logs',
            'sample_data/legal_documents'
        ]

        for directory in required_dirs:
            if os.path.exists(directory):
                if os.listdir(directory):
                    directories['present'].append(directory)
                    directories['file_counts'][directory] = len(os.listdir(directory))
                else:
                    directories['empty'].append(directory)
            else:
                directories['missing'].append(directory)

        return directories

    def _get_resource_usage(self) -> Dict[str, Any]:
        """Gather system resource usage information."""
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        
        return {
            'cpu_percent': psutil.cpu_percent(interval=1),
            'memory': {
                'total': memory.total,
                'available': memory.available,
                'percent': memory.percent
            },
            'disk': {
                'total': disk.total,
                'free': disk.free,
                'percent': disk.percent
            }
        }

    def _get_recent_logs(self) -> List[Dict[str, Any]]:
        """Gather recent log entries."""
        logs = []
        log_dir = "logs"
        
        if os.path.exists(log_dir):
            log_files = sorted(
                [f for f in os.listdir(log_dir) if f.endswith('.log')],
                key=lambda x: os.path.getmtime(os.path.join(log_dir, x)),
                reverse=True
            )[:5]  # Get 5 most recent logs

            for log_file in log_files:
                path = os.path.join(log_dir, log_file)
                with open(path, 'r') as f:
                    logs.append({
                        'file': log_file,
                        'modified': datetime.fromtimestamp(
                            os.path.getmtime(path)
                        ).isoformat(),
                        'last_lines': f.readlines()[-50:]  # Last 50 lines
                    })

        return logs

    def _run_quick_tests(self) -> Dict[str, Any]:
        """Run a quick test suite."""
        test_results = {
            'status': 'unknown',
            'output': '',
            'error': None
        }

        try:
            result = subprocess.run(
                [sys.executable, 'run_tests.py', '--quick'],
                capture_output=True,
                text=True
            )
            test_results['status'] = 'success' if result.returncode == 0 else 'failure'
            test_results['output'] = result.stdout
            test_results['error'] = result.stderr if result.stderr else None
        except Exception as e:
            test_results['status'] = 'error'
            test_results['error'] = str(e)

        return test_results

    def _get_disk_usage(self) -> Dict[str, int]:
        """Get disk usage information."""
        usage = psutil.disk_usage('/')
        return {
            'total': usage.total,
            'used': usage.used,
            'free': usage.free,
            'percent': usage.percent
        }

    def _generate_markdown_summary(self, report: Dict[str, Any]) -> None:
        """Generate a markdown summary of the diagnostic report."""
        summary_path = os.path.join(
            self.report_dir,
            f"diagnostic_summary_{self.timestamp}.md"
        )

        with open(summary_path, 'w') as f:
            f.write("# AI Document Processor Diagnostic Report\n\n")
            f.write(f"Generated: {self.timestamp}\n\n")

            # System Information
            f.write("## System Information\n")
            for key, value in report['system_info'].items():
                f.write(f"- {key}: {value}\n")
            f.write("\n")

            # Dependencies
            f.write("## Dependencies\n")
            f.write(f"- Installed: {len(report['dependencies']['installed'])}\n")
            f.write(f"- Missing: {len(report['dependencies']['missing'])}\n")
            if report['dependencies']['missing']:
                f.write("### Missing Dependencies:\n")
                for dep in report['dependencies']['missing']:
                    f.write(f"- {dep}\n")
            f.write("\n")

            # Configuration
            f.write("## Configuration\n")
            f.write(f"- Present: {', '.join(report['configuration']['files_present'])}\n")
            f.write(f"- Missing: {', '.join(report['configuration']['files_missing'])}\n")
            f.write("\n")

            # Test Results
            f.write("## Test Results\n")
            f.write(f"Status: {report['test_results']['status']}\n")
            if report['test_results']['error']:
                f.write(f"Error: {report['test_results']['error']}\n")
            f.write("\n")

            # Resource Usage
            f.write("## Resource Usage\n")
            f.write(f"- CPU: {report['resource_usage']['cpu_percent']}%\n")
            f.write(f"- Memory: {report['resource_usage']['memory']['percent']}%\n")
            f.write(f"- Disk: {report['resource_usage']['disk']['percent']}%\n")

def main():
    """Generate diagnostic report."""
    print("Generating AI Document Processor Diagnostic Report...")
    
    # Configure logging
    logging.basicConfig(level=logging.INFO)
    
    # Generate report
    reporter = DiagnosticReport()
    report = reporter.generate_report()
    
    print(f"\nDiagnostic report generated:")
    print(f"- Full report: {reporter.report_path}")
    print(f"- Summary: {reporter.report_path.replace('.json', '.md')}")
    
    # Print quick summary
    print("\nQuick Summary:")
    print(f"- System: {report['system_info']['os']}")
    print(f"- Python: {report['python_info']['version'].split()[0]}")
    print(f"- Missing Dependencies: {len(report['dependencies']['missing'])}")
    print(f"- Test Status: {report['test_results']['status']}")
    
    if report['dependencies']['missing'] or report['test_results']['status'] != 'success':
        print("\nWarning: Issues detected. Please check the full report for details.")

if __name__ == "__main__":
    main()
