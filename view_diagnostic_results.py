#!/usr/bin/env python3
"""Script to view and analyze diagnostic results."""

import os
import sys
import json
import logging
from datetime import datetime
from typing import Dict, List, Any
import webbrowser
from pathlib import Path
import html  # Added for HTML escaping

class DiagnosticViewer:
    """Viewer for diagnostic results with analysis capabilities."""

    def __init__(self, reports_dir: str = "diagnostic_reports"):
        """Initialize the diagnostic viewer with a custom reports directory."""
        self.reports_dir = reports_dir
        self.logger = logging.getLogger(__name__)

    def list_reports(self) -> List[str]:
        """List available diagnostic reports."""
        if not os.path.exists(self.reports_dir):
            return []
            
        return sorted(
            [f for f in os.listdir(self.reports_dir) if f.endswith('.json')],
            key=lambda x: os.path.getmtime(os.path.join(self.reports_dir, x)),
            reverse=True
        )

    def load_report(self, report_file: str) -> Dict[str, Any]:
        """Load a diagnostic report from file."""
        report_path = os.path.join(self.reports_dir, report_file)
        try:
            with open(report_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            self.logger.error(f"Error loading report {report_file}: {e}", exc_info=True)
            raise

    def analyze_report(self, report: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze a diagnostic report and identify issues."""
        analysis = {
            'status': 'healthy',
            'issues': [],
            'warnings': [],
            'recommendations': []
        }

        # Check dependencies with default empty lists if keys are missing
        deps = report.get('dependencies', {})
        missing_deps = deps.get('missing', [])
        if missing_deps:
            analysis['issues'].append(f"Missing dependencies: {', '.join(missing_deps)}")
            analysis['recommendations'].append(
                "Run 'pip install -r requirements-ai.txt' to install missing dependencies"
            )

        # Check resource usage with safe lookups
        resource_usage = report.get('resource_usage', {})
        cpu = resource_usage.get('cpu_percent', 0)
        memory = resource_usage.get('memory', {}).get('percent', 0)
        disk = resource_usage.get('disk', {}).get('percent', 0)
        if cpu > 80:
            analysis['warnings'].append("High CPU usage detected")
        if memory > 80:
            analysis['warnings'].append("High memory usage detected")
        if disk > 90:
            analysis['warnings'].append("Low disk space")

        # Check test results
        test_results = report.get('test_results', {})
        if test_results.get('status', '').lower() != 'success':
            analysis['issues'].append("Test failures detected")
            if test_results.get('error'):
                analysis['issues'].append(f"Test error: {test_results['error']}")

        # Set overall status
        if analysis['issues']:
            analysis['status'] = 'critical'
        elif analysis['warnings']:
            analysis['status'] = 'warning'

        return analysis

    def generate_html_report(self, report: Dict[str, Any], analysis: Dict[str, Any]) -> str:
        """Generate an HTML report with the diagnostic results."""
        html_path = os.path.join(
            self.reports_dir,
            f"diagnostic_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
        )

        status_colors = {
            'healthy': 'green',
            'warning': 'orange',
            'critical': 'red'
        }

        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(f"""
<!DOCTYPE html>
<html>
<head>
    <title>Diagnostic Report</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; }}
        .status {{ padding: 10px; border-radius: 5px; margin: 10px 0; }}
        .healthy {{ background-color: #dff0d8; color: #3c763d; }}
        .warning {{ background-color: #fcf8e3; color: #8a6d3b; }}
        .critical {{ background-color: #f2dede; color: #a94442; }}
        .section {{ margin: 20px 0; padding: 10px; border: 1px solid #ddd; }}
        .issue {{ color: #a94442; }}
        .warning-item {{ color: #8a6d3b; }}
        .recommendation {{ color: #3c763d; }}
    </style>
</head>
<body>
    <h1>AI Document Processor Diagnostic Report</h1>
    <div class="status {html.escape(analysis['status'])}">
        System Status: {html.escape(analysis['status'].upper())}
    </div>

    <div class="section">
        <h2>System Information</h2>
        <ul>
            <li>OS: {html.escape(report.get('system_info', {}).get('os', 'N/A'))}</li>
            <li>Python: {html.escape(report.get('python_info', {}).get('version', 'N/A').split()[0] if report.get('python_info', {}).get('version') else 'N/A')}</li>
            <li>CPU Usage: {html.escape(str(report.get('resource_usage', {}).get('cpu_percent', 0)))}%</li>
            <li>Memory Usage: {html.escape(str(report.get('resource_usage', {}).get('memory', {}).get('percent', 0)))}%</li>
            <li>Disk Usage: {html.escape(str(report.get('resource_usage', {}).get('disk', {}).get('percent', 0)))}%</li>
        </ul>
    </div>

    <div class="section">
        <h2>Issues and Warnings</h2>
        {self._format_list(analysis['issues'], 'issue')}
        {self._format_list(analysis['warnings'], 'warning-item')}
    </div>

    <div class="section">
        <h2>Recommendations</h2>
        {self._format_list(analysis['recommendations'], 'recommendation')}
    </div>

    <div class="section">
        <h2>Dependencies</h2>
        <h3>Installed ({len(report.get('dependencies', {}).get('installed', []))})</h3>
        {self._format_list(report.get('dependencies', {}).get('installed', []))}
        <h3>Missing ({len(report.get('dependencies', {}).get('missing', []))})</h3>
        {self._format_list(report.get('dependencies', {}).get('missing', []), 'issue')}
    </div>

    <div class="section">
        <h2>Test Results</h2>
        <p>Status: {html.escape(report.get('test_results', {}).get('status', 'N/A'))}</p>
        {f"<p class='issue'>Error: {html.escape(report.get('test_results', {}).get('error'))}</p>" if report.get('test_results', {}).get('error') else ""}
    </div>

    <div class="section">
        <h2>Recent Logs</h2>
        <pre>{self._format_logs(report.get('recent_logs', []))}</pre>
    </div>
</body>
</html>
            """)

        return html_path

    def _format_list(self, items: List[str], class_name: str = '') -> str:
        """Format a list of items as HTML."""
        if not items:
            return "<p>None</p>"
        
        class_attr = f' class="{class_name}"' if class_name else ''
        # Optionally escape each item here for extra safety.
        return "<ul>" + "".join(
            f"<li{class_attr}>{html.escape(str(item))}</li>" for item in items
        ) + "</ul>"

    def _format_logs(self, logs: List[Dict[str, Any]]) -> str:
        """Format log entries as text."""
        if not logs:
            return "No recent logs"
            
        formatted = []
        for log in logs:
            formatted.append(f"=== {html.escape(str(log.get('file', '')))} ===")
            formatted.append(f"Modified: {html.escape(str(log.get('modified', '')))}")
            formatted.extend(html.escape(line) for line in log.get('last_lines', []))
            formatted.append("\n")
            
        return "\n".join(formatted)

def main():
    """View and analyze diagnostic results."""
    logging.basicConfig(level=logging.INFO)
    
    viewer = DiagnosticViewer()
    reports = viewer.list_reports()
    
    if not reports:
        print("No diagnostic reports found.")
        print("Run 'python run_diagnostics.py' to generate a report.")
        return

    print("Available diagnostic reports:")
    for i, report in enumerate(reports):
        print(f"{i + 1}. {report}")

    try:
        selection = 0
        if len(reports) > 1:
            selection = int(input("\nSelect a report number (or press Enter for latest): ").strip() or "1") - 1
            if not 0 <= selection < len(reports):
                print("Invalid selection")
                return
            
        report_file = reports[selection]
        print(f"\nLoading report: {report_file}")
        
        report = viewer.load_report(report_file)
        analysis = viewer.analyze_report(report)
        html_path = viewer.generate_html_report(report, analysis)
        
        print(f"\nReport analysis complete!")
        print(f"Status: {analysis['status'].upper()}")
        
        if analysis['issues']:
            print("\nIssues Found:")
            for issue in analysis['issues']:
                print(f"- {issue}")
        
        if analysis['warnings']:
            print("\nWarnings:")
            for warning in analysis['warnings']:
                print(f"- {warning}")
        
        if analysis['recommendations']:
            print("\nRecommendations:")
            for rec in analysis['recommendations']:
                print(f"- {rec}")
        
        print(f"\nDetailed HTML report generated: {html_path}")
        
        # Open in browser
        if input("\nOpen report in browser? (y/N): ").lower().strip() == 'y':
            webbrowser.open(f"file://{os.path.abspath(html_path)}")
            
    except (ValueError, IndexError):
        print("Invalid input")
    except Exception as e:
        print(f"Error viewing report: {e}")
        logging.error("Error viewing diagnostic report", exc_info=True)

if __name__ == "__main__":
    main()
