# Banking System Simulation

Simple desktop banking app built with Python (Tkinter) and SQLite.

## Quickstart 🔧

1. Create (already done) and activate the virtual environment:

- Windows (Command Prompt):

  ```cmd
  .\.venv\Scripts\activate.bat
  ```

- Windows (PowerShell):

  ```powershell
  .\.venv\Scripts\Activate.ps1
  # If PowerShell execution policy blocks activation, run:
  # Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
  ```

- macOS / Linux (bash/zsh):

  ```bash
  source .venv/bin/activate
  ```

2. Install dependencies (none required currently, but keep requirements updated):

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python main.py
```

## Dev tools (optional) 💡

To add developer tooling, you can install formatters/test runners:

```bash
pip install black flake8 pytest
```

You can also add these to a `dev-requirements.txt` if you'd like me to prepare one.

## Notes
- The project uses only Python standard library modules (`sqlite3`, `tkinter`, `datetime`).
- Recommended Python version: **3.10+**
