#!/usr/bin/env python3
import subprocess
import sys
import os
from pathlib import Path
import venv
import platform
import shutil

def print_step(message):
    """Print a step message"""
    print("\n" + "="*80)
    print(message)
    print("="*80)

def run_command(command, check=True):
    """Run a command and return its output"""
    try:
        result = subprocess.run(
            command,
            check=check,
            capture_output=True,
            text=True
        )
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Error running command {' '.join(command)}: {e}")
        print(f"Error output: {e.stderr}")
        if check:
            sys.exit(1)
        return None

def setup_virtual_environment():
    """Create and activate virtual environment"""
    print_step("Setting up virtual environment...")
    
    venv_path = Path(".venv")
    if venv_path.exists():
        print("Removing existing virtual environment...")
        shutil.rmtree(venv_path)
    
    print("Creating new virtual environment...")
    venv.create(venv_path, with_pip=True)
    
    # Get the path to the virtual environment's Python executable
    if platform.system() == "Windows":
        python_path = venv_path / "Scripts" / "python.exe"
        pip_path = venv_path / "Scripts" / "pip.exe"
    else:
        python_path = venv_path / "bin" / "python"
        pip_path = venv_path / "bin" / "pip"
    
    return str(python_path), str(pip_path)

def install_dependencies(pip_path):
    """Install project dependencies"""
    print_step("Installing dependencies...")
    
    # Upgrade pip
    run_command([pip_path, "install", "--upgrade", "pip"])
    
    # Install requirements
    if Path("requirements_updated.txt").exists():
        print("Installing from requirements_updated.txt...")
        run_command([pip_path, "install", "-r", "requirements_updated.txt"])
    else:
        print("requirements_updated.txt not found, installing from requirements.txt...")
        run_command([pip_path, "install", "-r", "requirements.txt"])
    
    # Install development requirements if they exist
    if Path("requirements-legal.txt").exists():
        print("Installing legal requirements...")
        run_command([pip_path, "install", "-r", "requirements-legal.txt"])

def setup_git_hooks(python_path):
    """Set up Git hooks for development"""
    print_step("Setting up Git hooks...")
    
    hooks_dir = Path(".git") / "hooks"
    if not hooks_dir.exists():
        print("Git hooks directory not found. Initializing Git repository...")
        run_command(["git", "init"])
    
    # Create pre-commit hook
    pre_commit = hooks_dir / "pre-commit"
    with open(pre_commit, "w") as f:
        f.write(f"""#!/bin/sh
{python_path} -m black .
{python_path} -m pylint **/*.py
{python_path} -m mypy .
{python_path} -m pytest tests/
""")
    
    # Make hook executable on Unix-like systems
    if platform.system() != "Windows":
        pre_commit.chmod(0o755)

def setup_nltk_data(python_path):
    """Download required NLTK data"""
    print_step("Downloading NLTK data...")
    
    nltk_script = """
import nltk
nltk.download('stopwords', quiet=True)
nltk.download('punkt', quiet=True)
nltk.download('wordnet', quiet=True)
"""
    run_command([python_path, "-c", nltk_script])

def create_directories():
    """Create necessary directories"""
    print_step("Creating project directories...")
    
    directories = [
        "logs",
        "data",
        "benchmark_results",
        "docs"
    ]
    
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
        
        # Create .gitkeep file
        gitkeep = Path(directory) / ".gitkeep"
        gitkeep.touch()
        
        # Create .gitignore for logs directory
        if directory == "logs":
            gitignore = Path(directory) / ".gitignore"
            gitignore.write_text("*\n!.gitignore\n!.gitkeep\n")

def verify_installation(python_path):
    """Verify the installation"""
    print_step("Verifying installation...")
    
    # Run tests
    print("Running tests...")
    run_command([python_path, "-m", "pytest", "tests/"], check=False)
    
    # Run linting
    print("\nRunning linting...")
    run_command([python_path, "-m", "pylint", "**/*.py"], check=False)
    
    # Check imports
    print("\nChecking imports...")
    check_imports = """
try:
    import rich
    import psutil
    import matplotlib
    import nltk
    import PIL
    import fitz
    import docx
    import pandas
    import pptx
    import pytesseract
    print("All core dependencies imported successfully!")
except ImportError as e:
    print(f"Error importing dependencies: {e}")
"""
    run_command([python_path, "-c", check_imports])

def main():
    """Main setup function"""
    print_step("Starting development environment setup")
    
    # Setup virtual environment
    python_path, pip_path = setup_virtual_environment()
    
    # Install dependencies
    install_dependencies(pip_path)
    
    # Create directories
    create_directories()
    
    # Setup Git hooks
    setup_git_hooks(python_path)
    
    # Download NLTK data
    setup_nltk_data(python_path)
    
    # Verify installation
    verify_installation(python_path)
    
    print_step("Setup complete!")
    print("\nTo activate the virtual environment:")
    if platform.system() == "Windows":
        print("    .venv\\Scripts\\activate")
    else:
        print("    source .venv/bin/activate")

if __name__ == "__main__":
    main()
