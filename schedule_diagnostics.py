#!/usr/bin/env python3
"""Script to manage scheduled diagnostic runs and cleanups."""

import os
import sys
import json
import logging
import subprocess
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import argparse
from pathlib import Path

class DiagnosticScheduler:
    """Manages scheduled diagnostic runs and cleanups."""

    def __init__(self):
        """Initialize the diagnostic scheduler."""
        self.config_dir = "diagnostic_config"
        self.schedule_file = os.path.join(self.config_dir, "schedule.json")
        self.logger = logging.getLogger(__name__)
        
        # Create config directory if it doesn't exist
        os.makedirs(self.config_dir, exist_ok=True)

    def load_schedule(self) -> Dict:
        """Load the diagnostic schedule configuration."""
        if not os.path.exists(self.schedule_file):
            return self._create_default_schedule()
            
        try:
            with open(self.schedule_file, 'r') as f:
                return json.load(f)
        except Exception as e:
            self.logger.error(f"Error loading schedule: {str(e)}")
            return self._create_default_schedule()

    def save_schedule(self, schedule: Dict):
        """Save the diagnostic schedule configuration."""
        try:
            with open(self.schedule_file, 'w') as f:
                json.dump(schedule, f, indent=2)
        except Exception as e:
            self.logger.error(f"Error saving schedule: {str(e)}")
            raise

    def _create_default_schedule(self) -> Dict:
        """Create a default schedule configuration."""
        schedule = {
            'diagnostic_runs': {
                'enabled': True,
                'frequency': 'daily',  # daily, weekly, monthly
                'time': '00:00',
                'last_run': None,
                'next_run': None
            },
            'cleanup_runs': {
                'enabled': True,
                'frequency': 'weekly',
                'time': '01:00',
                'last_run': None,
                'next_run': None
            },
            'notification': {
                'enabled': False,
                'email': None,
                'critical_only': True
            },
            'retention': {
                'critical': 90,
                'warning': 30,
                'healthy': 7,
                'logs': 30
            }
        }
        
        self.save_schedule(schedule)
        return schedule

    def run_scheduled_tasks(self):
        """Run any scheduled tasks that are due."""
        schedule = self.load_schedule()
        now = datetime.now()
        
        # Check diagnostic runs
        if self._is_task_due(schedule['diagnostic_runs'], now):
            self._run_diagnostics()
            schedule['diagnostic_runs']['last_run'] = now.isoformat()
            schedule['diagnostic_runs']['next_run'] = self._calculate_next_run(
                schedule['diagnostic_runs'], now
            ).isoformat()
        
        # Check cleanup runs
        if self._is_task_due(schedule['cleanup_runs'], now):
            self._run_cleanup()
            schedule['cleanup_runs']['last_run'] = now.isoformat()
            schedule['cleanup_runs']['next_run'] = self._calculate_next_run(
                schedule['cleanup_runs'], now
            ).isoformat()
        
        self.save_schedule(schedule)

    def _is_task_due(self, task_config: Dict, now: datetime) -> bool:
        """Check if a task is due to run."""
        if not task_config['enabled']:
            return False
            
        if task_config['next_run'] is None:
            return True
            
        next_run = datetime.fromisoformat(task_config['next_run'])
        return now >= next_run

    def _calculate_next_run(self, task_config: Dict, from_time: datetime) -> datetime:
        """Calculate the next run time for a task."""
        time_parts = [int(x) for x in task_config['time'].split(':')]
        next_run = from_time.replace(hour=time_parts[0], minute=time_parts[1], second=0)
        
        if next_run <= from_time:
            if task_config['frequency'] == 'daily':
                next_run += timedelta(days=1)
            elif task_config['frequency'] == 'weekly':
                next_run += timedelta(days=7)
            elif task_config['frequency'] == 'monthly':
                # Add roughly a month
                if next_run.month == 12:
                    next_run = next_run.replace(year=next_run.year + 1, month=1)
                else:
                    next_run = next_run.replace(month=next_run.month + 1)
        
        return next_run

    def _run_diagnostics(self):
        """Run the diagnostic process."""
        self.logger.info("Running scheduled diagnostics...")
        try:
            subprocess.run([sys.executable, "run_diagnostics.py"], check=True)
            self.logger.info("Scheduled diagnostics completed successfully")
        except subprocess.CalledProcessError as e:
            self.logger.error(f"Error running diagnostics: {str(e)}")

    def _run_cleanup(self):
        """Run the cleanup process."""
        self.logger.info("Running scheduled cleanup...")
        try:
            # Run cleanup without requiring confirmation
            subprocess.run(
                [sys.executable, "cleanup_diagnostics.py", "--auto"],
                check=True
            )
            self.logger.info("Scheduled cleanup completed successfully")
        except subprocess.CalledProcessError as e:
            self.logger.error(f"Error running cleanup: {str(e)}")

def setup_logging():
    """Configure logging for the scheduler."""
    log_dir = "logs"
    os.makedirs(log_dir, exist_ok=True)
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(
                os.path.join(
                    log_dir,
                    f"scheduler_{datetime.now().strftime('%Y%m%d')}.log"
                )
            ),
            logging.StreamHandler()
        ]
    )

def main():
    """Main entry point for the scheduler."""
    parser = argparse.ArgumentParser(
        description="Manage scheduled diagnostic runs and cleanups"
    )
    parser.add_argument(
        '--configure',
        action='store_true',
        help='Configure schedule settings'
    )
    parser.add_argument(
        '--show',
        action='store_true',
        help='Show current schedule'
    )
    parser.add_argument(
        '--run',
        action='store_true',
        help='Run scheduled tasks that are due'
    )
    
    args = parser.parse_args()
    
    setup_logging()
    scheduler = DiagnosticScheduler()
    
    if args.configure:
        # Interactive configuration
        schedule = scheduler.load_schedule()
        
        print("\nConfigure Diagnostic Schedule")
        print("===========================")
        
        # Configure diagnostic runs
        print("\nDiagnostic Runs:")
        schedule['diagnostic_runs']['enabled'] = input(
            "Enable diagnostic runs? (y/N): "
        ).lower().strip() == 'y'
        if schedule['diagnostic_runs']['enabled']:
            freq = input(
                "Frequency (daily/weekly/monthly) [daily]: "
            ).lower().strip() or 'daily'
            schedule['diagnostic_runs']['frequency'] = freq
            schedule['diagnostic_runs']['time'] = input(
                "Time (HH:MM) [00:00]: "
            ).strip() or '00:00'
        
        # Configure cleanup runs
        print("\nCleanup Runs:")
        schedule['cleanup_runs']['enabled'] = input(
            "Enable cleanup runs? (y/N): "
        ).lower().strip() == 'y'
        if schedule['cleanup_runs']['enabled']:
            freq = input(
                "Frequency (daily/weekly/monthly) [weekly]: "
            ).lower().strip() or 'weekly'
            schedule['cleanup_runs']['frequency'] = freq
            schedule['cleanup_runs']['time'] = input(
                "Time (HH:MM) [01:00]: "
            ).strip() or '01:00'
        
        # Configure retention
        print("\nRetention Periods (days):")
        schedule['retention']['critical'] = int(input(
            "Critical reports [90]: "
        ) or "90")
        schedule['retention']['warning'] = int(input(
            "Warning reports [30]: "
        ) or "30")
        schedule['retention']['healthy'] = int(input(
            "Healthy reports [7]: "
        ) or "7")
        schedule['retention']['logs'] = int(input(
            "Log files [30]: "
        ) or "30")
        
        scheduler.save_schedule(schedule)
        print("\nSchedule configuration saved!")
        
    elif args.show:
        # Show current schedule
        schedule = scheduler.load_schedule()
        print("\nCurrent Schedule")
        print("===============")
        
        print("\nDiagnostic Runs:")
        if schedule['diagnostic_runs']['enabled']:
            print(f"Frequency: {schedule['diagnostic_runs']['frequency']}")
            print(f"Time: {schedule['diagnostic_runs']['time']}")
            if schedule['diagnostic_runs']['last_run']:
                print(f"Last run: {schedule['diagnostic_runs']['last_run']}")
            if schedule['diagnostic_runs']['next_run']:
                print(f"Next run: {schedule['diagnostic_runs']['next_run']}")
        else:
            print("Disabled")
        
        print("\nCleanup Runs:")
        if schedule['cleanup_runs']['enabled']:
            print(f"Frequency: {schedule['cleanup_runs']['frequency']}")
            print(f"Time: {schedule['cleanup_runs']['time']}")
            if schedule['cleanup_runs']['last_run']:
                print(f"Last run: {schedule['cleanup_runs']['last_run']}")
            if schedule['cleanup_runs']['next_run']:
                print(f"Next run: {schedule['cleanup_runs']['next_run']}")
        else:
            print("Disabled")
        
        print("\nRetention Periods (days):")
        print(f"Critical reports: {schedule['retention']['critical']}")
        print(f"Warning reports: {schedule['retention']['warning']}")
        print(f"Healthy reports: {schedule['retention']['healthy']}")
        print(f"Log files: {schedule['retention']['logs']}")
        
    elif args.run:
        # Run scheduled tasks
        scheduler.run_scheduled_tasks()
        
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
