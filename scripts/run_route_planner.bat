@echo off
:: Route Planner - Windows Environment Setup and Launcher
:: This script ensures the virtual environment is properly activated before running the application

echo [34m🎯 Route Planner Environment Setup[0m

:: Project directory - use the directory where this script is located
set "PROJECT_DIR=%~dp0"
:: Remove trailing backslash if present
if "%PROJECT_DIR:~-1%"=="\" set "PROJECT_DIR=%PROJECT_DIR:~0,-1%"
set "VENV_DIR=%PROJECT_DIR%.venv"
set "REQUIREMENTS_FILE=%PROJECT_DIR%requirements.txt"
set "MAIN_APP=%PROJECT_DIR%main.py"

:: Change to project directory
cd "%PROJECT_DIR%"

:: Create virtual environment if it doesn't exist
if not exist "%VENV_DIR%" (
    echo [33m🔧 Creating virtual environment...[0m
    python -m venv "%VENV_DIR%"
    if %ERRORLEVEL% neq 0 (
        echo [31m❌ Failed to create virtual environment. Is Python installed?[0m
        pause
        exit \b 1
    )
    echo [32m✅ Virtual environment created[0m
)

:: Activate virtual environment
echo [33m⚡ Activating virtual environment...[0m
call "%VENV_DIR%\Scripts\activate.bat"
if %ERRORLEVEL% neq 0 (
    echo [31m❌ Failed to activate virtual environment[0m
    pause
    exit \b 1
)

:: Upgrade pip
echo [33m📦 Upgrading pip...[0m
python -m pip install --upgrade pip
if %ERRORLEVEL% neq 0 (
    echo [31m⚠️ Failed to upgrade pip, but continuing...[0m
)

:: Install\update requirements
if exist "%REQUIREMENTS_FILE%" (
    echo [33m📦 Installing\updating dependencies...[0m
    pip install -r "%REQUIREMENTS_FILE%"
    if %ERRORLEVEL% neq 0 (
        echo [31m❌ Failed to install dependencies[0m
        pause
        exit \b 1
    )
    echo [32m✅ Dependencies installed[0m
) else (
    echo [31m❌ requirements.txt not found at: %REQUIREMENTS_FILE%[0m
    pause
    exit \b 1
)

:: Verify main application exists
if not exist "%MAIN_APP%" (
    echo [31m❌ main.py not found at: %MAIN_APP%[0m
    pause
    exit \b 1
)

:: Run the application
echo [32m🚀 Starting Route Planner...[0m
python "%MAIN_APP%" %*
if %ERRORLEVEL% neq 0 (
    echo [31m❌ Application exited with error code: %ERRORLEVEL%[0m
    pause
    exit \b %ERRORLEVEL%
)

exit \b 0
