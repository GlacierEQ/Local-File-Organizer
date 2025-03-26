import subprocess
import sys
import os

# TARGET_DIR uses os.getcwd() which should be run from the project root.
TARGET_DIR = os.path.join(os.getcwd(), "lib")
# Confirm that os.getcwd() points to the expected project directory.

def install_aiofiles():
    # Create the target directory if it does not exist.
    os.makedirs(TARGET_DIR, exist_ok=True)
    # Install aiofiles into the 'lib' folder.
    subprocess.check_call([sys.executable, "-m", "pip", "install", "aiofiles", "--target", TARGET_DIR])
    print("aiofiles installed into:", TARGET_DIR)

def update_sys_path():
    if TARGET_DIR not in sys.path:
        sys.path.insert(0, TARGET_DIR)
    print("Updated sys.path with:", TARGET_DIR)

if __name__ == "__main__":
    install_aiofiles()
    update_sys_path()
    print("Installation complete. You can now import aiofiles in your project.")
