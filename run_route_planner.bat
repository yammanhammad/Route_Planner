@echo off
:: Route Planner - Windows Environment Setup and Launcher
:: This script ensures the virtual environment is properly activated before running the application

echo [34m🎯 Route Planner Environment Setup[0m

:: Project directory - use the directory where this script is located
set "PROJECT_DIR=%~dp0"
set "VENV_DIR=%PROJECT_DIR%.venv"
set "REQUIREMENTS_FILE=%PROJECT_DIR%requirements.txt"
set "MAIN_APP=%PROJECT_DIR%main_app.py"

:: Change to project directory
cd "%PROJECT_DIR%"

:: Create virtual environment if it doesn't exist
if not exist "%VENV_DIR%" (
    echo [33m🔧 Creating virtual environment...[0m
    python -m venv "%VENV_DIR%"
    echo [32m✅ Virtual environment created[0m
)

:: Activate virtual environment
echo [33m⚡ Activating virtual environment...[0m
call "%VENV_DIR%\Scripts\activate.bat"

:: Upgrade pip
echo [33m📦 Upgrading pip...[0m
python -m pip install --upgrade pip --quiet

:: Install/update requirements
if exist "%REQUIREMENTS_FILE%" (
    echo [33m📦 Installing/updating dependencies...[0m
    pip install -r "%REQUIREMENTS_FILE%" --quiet
    echo [32m✅ Dependencies installed[0m
) else (
    echo [31m❌ requirements.txt not found[0m
    exit /b 1
)

:: Verify main application exists
if not exist "%MAIN_APP%" (
    echo [31m❌ main_app.py not found[0m
    exit /b 1
)

:: Run the application
echo [32m🚀 Starting Route Planner...[0m
python "%MAIN_APP%" %*
