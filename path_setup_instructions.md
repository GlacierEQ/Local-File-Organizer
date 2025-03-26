# Windows PATH Setup Instructions

When installing packages like `torch`, `onnxruntime-gpu`, `transformers`, and `accelerate`, some scripts (e.g., `torchrun.exe`, `onnxruntime_test.exe`, `coloredlogs.exe`) are installed into your user Scripts directory. To use these commands from any command prompt or PowerShell session, add the directory to your PATH.

## Steps to Add to PATH in Windows

1. **Find Your Scripts Directory:**

   Typically, the Scripts directory is located at:

   ```
   C:\Users\casey\AppData\Roaming\Python\Python310\Scripts
   ```

   Confirm that the folder exists and contains the installed scripts.

2. **Using System Settings:**

   - Press `Win + R`, type `sysdm.cpl`, and press Enter.
   - Go to the **Advanced** tab and click **Environment Variables**.
   - Under **User variables for casey**, select `Path` and click **Edit**.
   - Click **New** and paste the full path:
     ```
     C:\Users\casey\AppData\Roaming\Python\Python310\Scripts
     ```
   - Click **OK** on all dialogs to save your changes.
   - Restart any command prompts or PowerShell sessions for the change to take effect.

3. **Using PowerShell (Temporary for Current Session):**

   Open PowerShell and run:

   ```powershell
   $env:PATH += ";C:\Users\casey\AppData\Roaming\Python\Python310\Scripts"
   ```

   This command appends the directory to your PATH for the current session.

4. **Using Command Prompt (Temporarily):**

   Open Command Prompt and run:

   ```cmd
   set PATH=%PATH%;C:\Users\casey\AppData\Roaming\Python\Python310\Scripts
   ```

   This change applies only for the duration of the session.

## Note on Running Commands with '&&'

In Windows PowerShell, the `&&` operator is not always available in older versions. Instead, you can run multiple commands by separating them with a semicolon `;` or use PowerShell's pipeline features. For example:

```powershell
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118; pip install onnxruntime-gpu; pip install transformers accelerate
```

Follow these instructions to ensure that your Python scripts and utilities are available from any terminal session.

Happy coding!
