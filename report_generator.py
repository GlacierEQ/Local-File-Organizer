import json
import os
from datetime import datetime
import logging

def generate_report(stats: dict, output_dir: str):
    """
    Generates a JSON report summarizing file organization operations.
    """
    report = {
        "timestamp": datetime.now().isoformat(),
        "statistics": stats
    }
    report_path = os.path.join(output_dir, "Logs", f"sorting_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
    with open(report_path, "w") as f:
        json.dump(report, f, indent=2)
    logging.info(f"Report generated at: {report_path}")
