# Python Setup Instructions for Windows

It looks like Python is not currently installed or not configured in your system PATH. Follow these steps to get it running.

## 1. Download Python
1.  Go to the official Python website: [https://www.python.org/downloads/windows/](https://www.python.org/downloads/windows/)
2.  Download the latest "Windows installer (64-bit)".

## 2. Install Python (CRITICAL STEP)
1.  Run the installer you just downloaded.
2.  **IMPORTANT**: On the first screen, check the box that says **"Add python.exe to PATH"**.
    - If you miss this, you won't be able to run `python` from the command line easily.
3.  Click "Install Now".

## 3. Verify Installation
1.  Open a new terminal (or restart your current one).
2.  Type `python --version`.
3.  You should see something like `Python 3.12.x`.

## 4. Setup Project
Once Python is installed:
1.  Navigate to the project directory:
    ```powershell
    cd d:\PROJECTS\Antigravity\Erebor
    ```
2.  Install dependencies:
    ```powershell
    pip install -r requirements.txt
    ```
3.  Run the app:
    ```powershell
    python main.py
    ```
