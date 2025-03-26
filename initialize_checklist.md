# Project Initialization & Startup Checklist

Follow these steps to set up and initialize the Local File Organizer from scratch:

---

## 1. Repository Setup

- [ ] **Clone the Repository:**
  ```sh
  git clone https://github.com/QiuYannnn/Local-File-Organizer.git
  cd Local-File-Organizer
  ```
- [ ] **(Optional) Create a New Branch:**
  ```sh
  git checkout -b init-setup
  ```

---

## 2. Python Environment & Dependencies

- [ ] **Install Python 3.12:**  
       Ensure Python 3.12 is installed. Download if necessary from [Python.org](https://www.python.org/downloads/).

- [ ] **Create and Activate a Conda Environment:**

  ```sh
  conda create --name local_file_organizer python=3.12
  conda activate local_file_organizer
  ```

- [ ] **Install Project Dependencies:**

  ```sh
  pip install -r requirements.txt
  ```

  - If any issues occur, install packages individually:
    ```sh
    pip install nexa Pillow pytesseract PyMuPDF python-docx
    ```

- [ ] **Ensure Nexa SDK Installation:**
  - For CPU:
    ```sh
    pip install nexaai --prefer-binary --index-url https://nexaai.github.io/nexa-sdk/whl/cpu --extra-index-url https://pypi.org/simple --no-cache-dir
    ```
  - For GPU (if applicable), refer to the [Nexa SDK installation guide](https://github.com/NexaAI/nexa-sdk?tab=readme-ov-file#installation).

---

## 3. Configuration and Defaults

- [ ] **Reset Blackbox AI to Default:**  
       Run the provided reset script to restore default configuration:
  ```sh
  bash reset_blackbox_defaults.sh
  ```
- [ ] **Review and Update `config_ai.py`:**  
       Confirm any legal or chain-of-custody parameters are set as needed.
- [ ] **Verify Environment Variables/Paths:**  
       Ensure that the necessary paths (e.g., Python Scripts directory) are added to your PATH:
  ```powershell
  .\add_huggingface_to_path.ps1
  ```

---

## 4. Documentation and Validation

- [ ] **Review Documentation:**  
       Read through:

  - `README.md`
  - `ADMIN_GUIDE.md`
  - `ai_modules.md`
  - `gpu_npu_optimization.md`  
    to understand the project scope and configuration details.

- [ ] **Run the Diagnostic Report:**  
       Generate a diagnostic report to verify system status:
  ```sh
  python generate_diagnostic_report.py
  ```

---

## 5. Running the System

- [ ] **Start the File Organizer:**  
       Launch the main application:
  ```sh
  python main.py
  ```
- [ ] **Monitor Logs and Output:**  
       Check the `Logs` folder and console output for any errors or warnings.

- [ ] **Test Legal & Chain-of-Custody Features:**  
       Process several sample legal documents to confirm they are categorized and logged correctly.

---

## 6. Continuous Integration

- [ ] **Run CI/CD Tests:**  
       If modifications have been made, run the GitHub Actions workflows locally or check the CI/CD dashboard to ensure all tests pass.

---

Once all tasks are completed, your system should be fully initialized, configured to default settings, and ready for use. This checklist can be revisited after making further changes to the project.

Happy organizing!
