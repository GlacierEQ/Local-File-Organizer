#!/usr/bin/env python3
import os
import sys
import subprocess

def setup_test_environment():
    """Set up the test environment by installing required dependencies."""
    print("Setting up test environment...")
    
    # Install test requirements
    subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements-test.txt"])
    
    # Create test directories if they don't exist
    os.makedirs("test_documents", exist_ok=True)
    os.makedirs("test_output", exist_ok=True)

def run_tests():
    """Run the test suite."""
    print("\nRunning tests...")
    subprocess.run([sys.executable, "-m", "pytest", "tests/", "-v", "--cov=."])

def main():
    try:
        setup_test_environment()
        run_tests()
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
