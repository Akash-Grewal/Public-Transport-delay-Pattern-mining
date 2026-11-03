@echo off
setlocal
cd /d "%~dp0"
echo ================================================
echo Public Transport Delay Pattern Mining
echo ================================================
where py >nul 2>nul
if errorlevel 1 (
  echo ERROR: Python Launcher 'py' was not found.
  echo Install Python 3.13 from https://www.python.org/downloads/windows/
  echo During installation, enable the Python Launcher option.
  pause
  exit /b 1
)
if not exist ".venv\Scripts\python.exe" (
  echo Creating an isolated Python environment...
  py -3.13 -m venv .venv
  if errorlevel 1 goto setup_error
)
echo Installing/checking compatible packages in .venv...
".venv\Scripts\python.exe" -m pip install --upgrade pip
if errorlevel 1 goto setup_error
".venv\Scripts\python.exe" -m pip install -r requirements.txt
if errorlevel 1 goto setup_error
echo.
echo Running project...
".venv\Scripts\python.exe" main.py
if errorlevel 1 goto run_error
echo.
echo SUCCESS. Opening the generated dashboard...
start "" "%CD%\outputs\dashboard.html"
pause
exit /b 0
:setup_error
echo.
echo Setup failed. Check your internet connection and Python 3.13 installation.
echo Your global Python and NumPy installation were not changed.
pause
exit /b 1
:run_error
echo.
echo The project stopped with an error. Read the message above.
pause
exit /b 1
