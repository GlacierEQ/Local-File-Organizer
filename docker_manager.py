#!/usr/bin/env python3
"""Script to manage Docker environment for AI Document Processing System."""

import os
import sys
import subprocess
import argparse
import logging
from datetime import datetime
from typing import List, Optional

class DockerManager:
    """Manages Docker environment operations."""

    def __init__(self):
        """Initialize the Docker manager."""
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
                        f"docker_manager_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
                    )
                ),
                logging.StreamHandler()
            ]
        )

    def run_command(self, command: List[str], check: bool = True) -> subprocess.CompletedProcess:
        """Run a shell command."""
        try:
            self.logger.debug(f"Running command: {' '.join(command)}")
            return subprocess.run(command, check=check, capture_output=True, text=True)
        except subprocess.CalledProcessError as e:
            self.logger.error(f"Command failed: {e.stderr}")
            raise

    def start_services(self, dev_mode: bool = False, services: Optional[List[str]] = None):
        """Start Docker services."""
        command = ["docker-compose"]
        
        if dev_mode:
            command.extend(["-f", "docker-compose.yml", "-f", "docker-compose.dev.yml"])
        
        command.extend(["up", "-d"])
        
        if services:
            command.extend(services)
            
        self.run_command(command)
        self.logger.info(f"Started services: {services if services else 'all'}")

    def stop_services(self):
        """Stop Docker services."""
        self.run_command(["docker-compose", "down"])
        self.logger.info("Stopped all services")

    def rebuild_services(self, dev_mode: bool = False, no_cache: bool = False):
        """Rebuild Docker services."""
        command = ["docker-compose"]
        
        if dev_mode:
            command.extend(["-f", "docker-compose.yml", "-f", "docker-compose.dev.yml"])
            
        command.append("build")
        
        if no_cache:
            command.append("--no-cache")
            
        self.run_command(command)
        self.logger.info("Rebuilt services")

    def view_logs(self, service: Optional[str] = None, follow: bool = False):
        """View Docker logs."""
        command = ["docker-compose", "logs"]
        
        if follow:
            command.append("-f")
            
        if service:
            command.append(service)
            
        self.run_command(command, check=False)

    def check_status(self):
        """Check status of Docker services."""
        self.run_command(["docker-compose", "ps"])

    def run_tests(self):
        """Run tests in Docker environment."""
        command = ["docker-compose", "-f", "docker-compose.dev.yml", "run", "test-runner"]
        self.run_command(command)
        self.logger.info("Completed test run")

    def run_linting(self):
        """Run linting in Docker environment."""
        command = ["docker-compose", "-f", "docker-compose.dev.yml", "run", "linter"]
        self.run_command(command)
        self.logger.info("Completed linting")

    def build_docs(self):
        """Build documentation in Docker environment."""
        command = ["docker-compose", "-f", "docker-compose.dev.yml", "run", "docs-builder"]
        self.run_command(command)
        self.logger.info("Built documentation")

    def clean_environment(self):
        """Clean Docker environment."""
        # Stop containers
        self.run_command(["docker-compose", "down"], check=False)
        
        # Remove volumes
        self.run_command(
            ["docker-compose", "down", "-v"],
            check=False
        )
        
        # Remove images
        self.run_command(
            ["docker-compose", "down", "--rmi", "all"],
            check=False
        )
        
        # Prune system
        self.run_command(["docker", "system", "prune", "-f"], check=False)
        
        self.logger.info("Cleaned Docker environment")

    def check_resource_usage(self):
        """Check Docker resource usage."""
        # Check disk usage
        self.run_command(["docker", "system", "df"])
        
        # Check container stats
        self.run_command(["docker", "stats", "--no-stream"])

def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Manage Docker environment for AI Document Processing System"
    )
    
    # Command groups
    service_group = parser.add_argument_group('Service Management')
    dev_group = parser.add_argument_group('Development')
    maintenance_group = parser.add_argument_group('Maintenance')
    
    # Service management arguments
    service_group.add_argument(
        '--start',
        action='store_true',
        help='Start Docker services'
    )
    service_group.add_argument(
        '--stop',
        action='store_true',
        help='Stop Docker services'
    )
    service_group.add_argument(
        '--restart',
        action='store_true',
        help='Restart Docker services'
    )
    service_group.add_argument(
        '--status',
        action='store_true',
        help='Check service status'
    )
    service_group.add_argument(
        '--logs',
        metavar='SERVICE',
        nargs='?',
        const='all',
        help='View service logs'
    )
    
    # Development arguments
    dev_group.add_argument(
        '--dev',
        action='store_true',
        help='Use development configuration'
    )
    dev_group.add_argument(
        '--test',
        action='store_true',
        help='Run tests'
    )
    dev_group.add_argument(
        '--lint',
        action='store_true',
        help='Run linting'
    )
    dev_group.add_argument(
        '--docs',
        action='store_true',
        help='Build documentation'
    )
    
    # Maintenance arguments
    maintenance_group.add_argument(
        '--rebuild',
        action='store_true',
        help='Rebuild services'
    )
    maintenance_group.add_argument(
        '--clean',
        action='store_true',
        help='Clean Docker environment'
    )
    maintenance_group.add_argument(
        '--resources',
        action='store_true',
        help='Check resource usage'
    )
    
    args = parser.parse_args()
    
    manager = DockerManager()
    
    try:
        if args.start:
            manager.start_services(dev_mode=args.dev)
            
        if args.stop:
            manager.stop_services()
            
        if args.restart:
            manager.stop_services()
            manager.start_services(dev_mode=args.dev)
            
        if args.status:
            manager.check_status()
            
        if args.logs:
            manager.view_logs(
                service=None if args.logs == 'all' else args.logs,
                follow=True
            )
            
        if args.rebuild:
            manager.rebuild_services(dev_mode=args.dev)
            
        if args.test:
            manager.run_tests()
            
        if args.lint:
            manager.run_linting()
            
        if args.docs:
            manager.build_docs()
            
        if args.clean:
            manager.clean_environment()
            
        if args.resources:
            manager.check_resource_usage()
            
    except Exception as e:
        logging.error(f"Error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
