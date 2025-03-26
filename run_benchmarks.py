#!/usr/bin/env python3
"""Script to run AI processor benchmarks."""

import os
import sys
import subprocess
import logging
from datetime import datetime

def setup_benchmark_environment():
    """Set up the environment for running benchmarks."""
    print("Setting up benchmark environment...")
    
    # Install benchmark requirements
    subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements-benchmark.txt"])
    
    # Create necessary directories
    os.makedirs("benchmark_results", exist_ok=True)
    os.makedirs("test_output", exist_ok=True)

def run_benchmarks():
    """Run the benchmark suite."""
    print("\nRunning benchmarks...")
    from benchmarks.benchmark_ai_processor import main
    main()

def main():
    """Main entry point."""
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler(
                f'benchmark_results/benchmark_log_{datetime.now().strftime("%Y%m%d_%H%M%S")}.txt'
            )
        ]
    )

    try:
        setup_benchmark_environment()
        run_benchmarks()
        
        print("\nBenchmark complete!")
        print("Check the benchmark_results directory for:")
        print("- JSON results file")
        print("- Performance plots")
        print("- Benchmark logs")
        
    except Exception as e:
        print(f"\nError during benchmarking: {str(e)}")
        logging.error(f"Benchmark failed: {str(e)}", exc_info=True)
        sys.exit(1)

if __name__ == "__main__":
    main()
