#!/usr/bin/env python3
import os
import sys
import subprocess
from pathlib import Path
from datetime import datetime
import json
from rich.console import Console
from rich.progress import Progress

class ReleasePreparation:
    """Prepares the system for release"""
    
    def __init__(self):
        self.console = Console()
        self.version = self._get_version()
        self.release_dir = Path("dist")
        self.release_dir.mkdir(exist_ok=True)

    def _get_version(self) -> str:
        """Get version from config or generate one"""
        if Path("config.json").exists():
            with open("config.json") as f:
                config = json.load(f)
                if "version" in config:
                    return config["version"]
        
        # Generate version based on date
        return datetime.now().strftime("%Y.%m.%d")

    def verify_dependencies(self):
        """Verify all dependencies are installed and up to date"""
        self.console.print("\n[bold blue]Verifying dependencies...[/]")
        
        try:
            # Check pip packages
            subprocess.run(
                [sys.executable, "-m", "pip", "install", "-r", "requirements_updated.txt"],
                check=True
            )
            self.console.print("[green]Dependencies verified successfully[/]")
            return True
        except subprocess.CalledProcessError as e:
            self.console.print(f"[red]Error verifying dependencies: {e}[/]")
            return False

    def run_tests(self):
        """Run all tests including benchmarks"""
        self.console.print("\n[bold blue]Running tests...[/]")
        
        try:
            # Run pytest with coverage
            subprocess.run(
                [sys.executable, "-m", "pytest", "--cov=.", "--cov-report=xml", "tests/"],
                check=True
            )
            
            # Run benchmarks
            subprocess.run(
                [sys.executable, "-m", "pytest", "benchmarks/test_benchmarks.py"],
                check=True
            )
            
            self.console.print("[green]All tests passed successfully[/]")
            return True
        except subprocess.CalledProcessError as e:
            self.console.print(f"[red]Error running tests: {e}[/]")
            return False

    def run_linting(self):
        """Run code quality checks"""
        self.console.print("\n[bold blue]Running code quality checks...[/]")
        
        try:
            # Run pylint
            subprocess.run(
                [sys.executable, "-m", "pylint", "**/*.py"],
                check=True
            )
            
            # Run black
            subprocess.run(
                [sys.executable, "-m", "black", "."],
                check=True
            )
            
            # Run mypy
            subprocess.run(
                [sys.executable, "-m", "mypy", "."],
                check=True
            )
            
            self.console.print("[green]Code quality checks passed[/]")
            return True
        except subprocess.CalledProcessError as e:
            self.console.print(f"[red]Error in code quality checks: {e}[/]")
            return False

    def generate_documentation(self):
        """Generate documentation"""
        self.console.print("\n[bold blue]Generating documentation...[/]")
        
        try:
            subprocess.run(
                [sys.executable, "docs/generate_docs.py"],
                check=True
            )
            self.console.print("[green]Documentation generated successfully[/]")
            return True
        except subprocess.CalledProcessError as e:
            self.console.print(f"[red]Error generating documentation: {e}[/]")
            return False

    def create_distribution(self):
        """Create distribution files"""
        self.console.print("\n[bold blue]Creating distribution...[/]")
        
        try:
            # Create source distribution
            subprocess.run(
                [sys.executable, "setup.py", "sdist", "bdist_wheel"],
                check=True
            )
            
            self.console.print("[green]Distribution created successfully[/]")
            return True
        except subprocess.CalledProcessError as e:
            self.console.print(f"[red]Error creating distribution: {e}[/]")
            return False

    def update_changelog(self):
        """Update CHANGELOG.md"""
        self.console.print("\n[bold blue]Updating changelog...[/]")
        
        changelog_path = Path("CHANGELOG.md")
        if not changelog_path.exists():
            changelog_content = f"""# Changelog

## [{self.version}] - {datetime.now().strftime("%Y-%m-%d")}

### Added
- Initial release
- Configuration management system
- Database with migrations
- Error handling system
- Performance optimization
- System management
- Logging system
- Benchmarking tools
- Test suite
- Documentation
- CI/CD pipeline

### Changed
- N/A

### Deprecated
- N/A

### Removed
- N/A

### Fixed
- N/A

### Security
- Initial security features implementation
"""
            changelog_path.write_text(changelog_content)
            self.console.print("[green]Changelog created successfully[/]")
        else:
            self.console.print("[yellow]Changelog already exists, please update manually[/]")

    def verify_git_status(self):
        """Verify Git repository status"""
        self.console.print("\n[bold blue]Checking Git status...[/]")
        
        try:
            # Check if there are uncommitted changes
            result = subprocess.run(
                ["git", "status", "--porcelain"],
                capture_output=True,
                text=True,
                check=True
            )
            
            if result.stdout.strip():
                self.console.print("[yellow]Warning: There are uncommitted changes[/]")
                return False
            
            self.console.print("[green]Git repository is clean[/]")
            return True
        except subprocess.CalledProcessError as e:
            self.console.print(f"[red]Error checking Git status: {e}[/]")
            return False

    def create_release_tag(self):
        """Create Git release tag"""
        self.console.print("\n[bold blue]Creating release tag...[/]")
        
        try:
            tag_name = f"v{self.version}"
            message = f"Release version {self.version}"
            
            # Create and push tag
            subprocess.run(
                ["git", "tag", "-a", tag_name, "-m", message],
                check=True
            )
            
            subprocess.run(
                ["git", "push", "origin", tag_name],
                check=True
            )
            
            self.console.print(f"[green]Release tag {tag_name} created successfully[/]")
            return True
        except subprocess.CalledProcessError as e:
            self.console.print(f"[red]Error creating release tag: {e}[/]")
            return False

    def prepare_release(self):
        """Run all release preparation steps"""
        with Progress() as progress:
            task = progress.add_task("Preparing release...", total=8)
            
            steps = [
                (self.verify_dependencies, "Verifying dependencies"),
                (self.run_tests, "Running tests"),
                (self.run_linting, "Running code quality checks"),
                (self.generate_documentation, "Generating documentation"),
                (self.create_distribution, "Creating distribution"),
                (self.update_changelog, "Updating changelog"),
                (self.verify_git_status, "Verifying Git status"),
                (self.create_release_tag, "Creating release tag")
            ]
            
            success = True
            for step_func, description in steps:
                progress.update(task, description=description)
                if not step_func():
                    success = False
                    break
                progress.advance(task)
            
            if success:
                self.console.print("\n[bold green]Release preparation completed successfully![/]")
                self.console.print(f"\nVersion: {self.version}")
                self.console.print("\nNext steps:")
                self.console.print("1. Review the generated documentation")
                self.console.print("2. Push the release tag")
                self.console.print("3. Create GitHub release")
                self.console.print("4. Upload distribution to PyPI")
            else:
                self.console.print("\n[bold red]Release preparation failed![/]")
                self.console.print("Please fix the issues and try again")

if __name__ == "__main__":
    preparation = ReleasePreparation()
    preparation.prepare_release()
