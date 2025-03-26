# Dependency Troubleshooting Guide

It looks like your Python environment is missing the `huggingface-hub` package or it's not installed correctly. Try these steps to fix it:

## 1. Reinstall `huggingface-hub`

Run this command in PowerShell:

```powershell
pip uninstall huggingface-hub -y
pip install huggingface-hub
```

Then, try running your script again:

```powershell
python run_benchmark.py
```

---

## 2. Upgrade `transformers` and Dependencies

If reinstalling `huggingface-hub` doesn't work, upgrade `transformers` and related dependencies:

```powershell
pip install --upgrade transformers huggingface-hub
```

---

## 3. Check Python Environment

Make sure you're using the correct Python version and environment:

```powershell
python -m pip list | Select-String "huggingface-hub"
```

If it says "Not Found," then the package isn’t installed in your environment.

---

## 4. Check `pip` and Virtual Environment

Make sure `pip` is up-to-date and installed in the right environment:

```powershell
python -m ensurepip --default-pip
python -m pip install --upgrade pip
```

If you are using a virtual environment, activate it before installing dependencies:

```powershell
venv\Scripts\activate
pip install transformers huggingface-hub
```

---

## 5. Try a Fresh Installation

If all else fails, reinstall `transformers` and `huggingface-hub` completely:

```powershell
pip uninstall transformers huggingface-hub -y
pip install transformers huggingface-hub
```

Then retry running your script:

```powershell
python run_benchmark.py
```

Let me know if any errors persist! 🚀
