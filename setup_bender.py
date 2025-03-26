"""
Setup script for Bender Rodriguez's AI capabilities.
Verifies and configures all required models and dependencies.
"""
import os
import sys
import subprocess
import logging
from pathlib import Path
import json
import torch
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn
from concurrent.futures import ThreadPoolExecutor
import requests
from typing import List, Dict, Any

# Initialize rich console for Bender's style
console = Console()

def print_bender_ascii():
    """Print Bender's ASCII art with style"""
    bender = """
    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣀⣤⣤⣤⣤⣤⣀⣀⠀⠀⠀⠀⠀⠀⠀⠀
    ⠀⠀⠀⠀⠀⠀⣠⣴⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣦⣄⠀⠀⠀⠀
    ⠀⠀⠀⠀⣠⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣄⠀⠀
    ⠀⠀⠀⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⠀
    ⠀⢀⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇
    ⠀⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷
    ⣸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
    ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
    ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
    ⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿
    ⠘⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠃
    ⠀⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟⠀
    ⠀⠀⠻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠟⠀⠀
    ⠀⠀⠀⠙⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠋⠀⠀⠀
    ⠀⠀⠀⠀⠀⠙⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⠋⠀⠀⠀⠀⠀
    ⠀⠀⠀⠀⠀⠀⠀⠈⠙⠛⠛⠿⠿⠿⠿⠛⠛⠋⠁⠀⠀⠀⠀⠀⠀⠀
    """
    console.print(bender, style="bold yellow")
    console.print("Bite my shiny metal ASCII!", style="bold cyan")
    console.print("\nInitializing Bender Rodriguez's AI capabilities...\n")

def check_system_requirements():
    """Check if system meets requirements"""
    with console.status("[bold yellow]Checking system requirements..."):
        # Check Python version
        python_version = sys.version_info
        if python_version < (3, 8):
            console.print("[red]Error: Python 3.8 or higher required!")
            return False
        
        # Check CUDA availability
        cuda_available = torch.cuda.is_available()
        if cuda_available:
            console.print(f"[green]CUDA available: {torch.cuda.get_device_name(0)}")
        else:
            console.print("[yellow]Warning: CUDA not available. CPU only mode.")
        
        # Check disk space
        import psutil
        disk = psutil.disk_usage('/')
        if disk.percent > 90:
            console.print("[yellow]Warning: Low disk space!")
        
        return True

def install_dependencies():
    """Install required packages"""
    requirements_file = "requirements_ai.txt"
    
    with console.status("[bold yellow]Installing dependencies..."):
        try:
            subprocess.check_call([
                sys.executable, 
                "-m", 
                "pip", 
                "install", 
                "-r", 
                requirements_file
            ])
            console.print("[green]Dependencies installed successfully!")
            return True
        except subprocess.CalledProcessError as e:
            console.print(f"[red]Error installing dependencies: {str(e)}")
            return False

def download_models(config: Dict[str, Any]):
    """Download and verify AI models"""
    from transformers import AutoTokenizer, AutoModel
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console
    ) as progress:
        for model_type, model_info in config["models"].items():
            task = progress.add_task(
                f"[cyan]Downloading {model_type} model...",
                total=None
            )
            
            try:
                # Download model and tokenizer
                model_name = model_info["name"]
                tokenizer = AutoTokenizer.from_pretrained(model_name)
                model = AutoModel.from_pretrained(model_name)
                
                # Verify model
                test_input = "Test input for verification"
                inputs = tokenizer(test_input, return_tensors="pt")
                with torch.no_grad():
                    outputs = model(**inputs)
                
                progress.update(task, completed=True)
                console.print(f"[green]✓ {model_type} model verified!")
                
            except Exception as e:
                progress.update(task, completed=True)
                console.print(f"[red]Error downloading {model_type} model: {str(e)}")
                return False
    
    return True

def setup_model_optimization():
    """Set up model optimization settings"""
    with console.status("[bold yellow]Configuring model optimization..."):
        try:
            # Set up hardware acceleration
            if torch.cuda.is_available():
                torch.backends.cudnn.benchmark = True
            
            # Set up mixed precision
            torch.set_float32_matmul_precision('high')
            
            console.print("[green]Model optimization configured!")
            return True
        except Exception as e:
            console.print(f"[red]Error configuring optimization: {str(e)}")
            return False

def verify_internet_connection():
    """Verify internet connection for model downloads"""
    try:
        requests.get("https://huggingface.co", timeout=5)
        return True
    except requests.RequestException:
        console.print("[red]Error: No internet connection!")
        return False

def main():
    """Main setup function"""
    print_bender_ascii()
    
    # Load configuration
    try:
        with open("core/ai_config.json", 'r') as f:
            config = json.load(f)
    except Exception as e:
        console.print(f"[red]Error loading configuration: {str(e)}")
        return False
    
    # Run setup steps
    steps = [
        ("System Requirements", check_system_requirements),
        ("Internet Connection", verify_internet_connection),
        ("Dependencies", install_dependencies),
        ("Model Download", lambda: download_models(config)),
        ("Optimization", setup_model_optimization)
    ]
    
    success = True
    for step_name, step_func in steps:
        console.print(f"\n[bold cyan]Setting up {step_name}...")
        if not step_func():
            success = False
            break
    
    if success:
        console.print("\n[bold green]Bender's AI capabilities are ready!")
        console.print("[yellow]I'm 40% AI, baby! Time to bend some code!")
    else:
        console.print("\n[bold red]Setup failed!")
        console.print("[yellow]Looks like I'll have to do this the old-fashioned way... with booze and violence!")
    
    return success

if __name__ == "__main__":
    sys.exit(0 if main() else 1)
