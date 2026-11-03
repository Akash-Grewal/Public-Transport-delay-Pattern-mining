PUBLIC TRANSPORT DELAY PATTERN MINING - WINDOWS QUICK START

1. Extract this ZIP completely (right-click > Extract All).
2. Open the extracted transport_delay_mining folder.
3. Double-click CHECK_PYTHON.bat to confirm Python 3.13 is installed.
4. Double-click RUN_PROJECT.bat.

WHAT THE RUN FILE DOES
- Creates a private .venv folder inside this project.
- Installs compatible packages into that private environment.
- Runs main.py and opens outputs\dashboard.html.
- Does NOT use or modify packages in your global Python installation.

IMPORTANT
- Internet is required the first time to download packages.
- Keep the folder extracted; do not run the BAT file from inside the ZIP.
- Python 3.13 (64-bit recommended) must be installed.
- Existing broken global NumPy is bypassed, not repaired or modified.

OPTIONAL
- RUN_TESTS.bat runs the automated tests after the first setup.
- Your own CSV can be used by running:
  .venv\Scripts\python.exe main.py --input "your_file.csv"

DATA NOTE
The included sample dataset is synthetic and is for demonstration only.
