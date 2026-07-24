@echo off
echo ========================================
echo   Offline AI Assistant - Installation
echo ========================================
echo.

REM Check if Python is installed
py --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.7 or higher from https://python.org
    pause
    exit /b 1
)

REM Use py command for Python
set PYTHON_CMD=py

echo Python found. Proceeding with installation...
echo.

REM Create virtual environment
echo Creating virtual environment...
%PYTHON_CMD% -m venv venv
if %errorlevel% neq 0 (
    echo ERROR: Failed to create virtual environment
    pause
    exit /b 1
)
echo Virtual environment created successfully.
echo.

REM Activate virtual environment and run setup
echo Activating virtual environment and running setup...
call venv\Scripts\activate.bat
if %errorlevel% neq 0 (
    echo ERROR: Failed to activate virtual environment
    pause
    exit /b 1
)

%PYTHON_CMD% setup.py
if %errorlevel% neq 0 (
    echo ERROR: Setup failed
    pause
    exit /b 1
)

echo.
echo ========================================
echo   Installation Complete!
echo ========================================
echo To run the AI, use: run.bat
echo Or manually:
echo   1. Activate virtual environment: venv\Scripts\activate.bat
echo   2. Run: python main.py
echo.
pause