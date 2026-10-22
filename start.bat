@echo off
cd /d "%~dp0"
set "PYTHONNOUSERSITE=1"
set "PYTHONDONTWRITEBYTECODE=1"

"%~dp0runtime\python.exe" "%~dp0run_server.py"

pause