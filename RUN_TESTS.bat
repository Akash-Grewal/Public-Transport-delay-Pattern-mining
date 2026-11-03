@echo off
setlocal
cd /d "%~dp0"
if not exist ".venv\Scripts\python.exe" (
  echo Run RUN_PROJECT.bat once first to create the isolated environment.
  pause
  exit /b 1
)
".venv\Scripts\python.exe" -m unittest discover -s tests -v
pause
