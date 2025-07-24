@echo off
title YASMIN - Sign Language Translator
mode con: cols=80 lines=30
color 0f
chcp 65001 > nul
setlocal enabledelayedexpansion

cls
echo.
echo  ██╗   ██╗ █████╗ ███████╗███╗   ███╗██╗███╗   ██╗
echo  ╚██╗ ██╔╝██╔══██╗██╔════╝████╗ ████║██║████╗  ██║
echo   ╚████╔╝ ███████║███████╗██╔████╔██║██║██╔██╗ ██║
echo    ╚██╔╝  ██╔══██║╚════██║██║╚██╔╝██║██║██║╚██╗██║
echo     ██║   ██║  ██║███████║██║ ╚═╝ ██║██║██║ ╚████║
echo     ╚═╝   ╚═╝  ╚═╝╚══════╝╚═╝     ╚═╝╚═╝╚═╝  ╚═══╝
echo.
echo                Sign Language Translator
echo                =======================
echo.
echo  Press ENTER to continue...
pause > nul

cls
echo ╔════════════════════════════════════════════════════════════╗
echo ║                    Installation Starting                  ║
echo ╚════════════════════════════════════════════════════════════╝
echo.

:: Python check
echo [INFO] Checking Python version...
python --version > nul 2>&1
if errorlevel 1 (
    echo.
    echo [ERROR] Python not found!
    echo Please download and install Python from https://www.python.org/downloads/
    echo Remember to check "Add Python to PATH" during installation.
    echo.
    pause
    exit /b 1
)
echo [SUCCESS] Python is installed and working.
echo.

:: Virtual environment check and activation
if not exist "venv" (
    echo [INFO] Creating virtual environment...
    python -m venv venv
    echo [SUCCESS] Virtual environment created.
    echo.
)

:: Activate virtual environment
echo [INFO] Activating virtual environment...
call venv\Scripts\activate
echo [SUCCESS] Virtual environment activated.
echo.

:: Install packages
echo [INFO] Installing required packages...
echo.

echo [1/8] Installing basic packages (numpy, opencv-python)...
pip install numpy opencv-python --quiet

echo [2/8] Installing MediaPipe and configuration packages...
pip install mediapipe PyYAML python-dotenv --quiet

echo [3/8] Installing machine learning packages...
pip install scikit-learn==1.2.0 --quiet

echo [4/8] Installing translation and visualization packages...
pip install googletrans==3.1.0a0 matplotlib --quiet

echo [5/8] Installing data processing packages...
pip install pickle-mixin --quiet

echo [6/8] Installing GUI components...
pip install customtkinter --quiet

echo [7/8] Installing test packages...
pip install pytest pytest-cov pytest-html pytest-mock pytest-asyncio pytest-timeout pytest-xdist coverage --quiet

echo [8/8] Installing code quality tools...
pip install mypy pylint black isort --quiet

echo.
echo [SUCCESS] All packages installed successfully.
echo.
echo Installation completed. Press ENTER to continue...
pause > nul

cls
echo ╔════════════════════════════════════════════════════════════╗
echo ║                    Code Quality Check                     ║
echo ╚════════════════════════════════════════════════════════════╝
echo.

echo [INFO] Formatting code...
black . --quiet
isort . --quiet

echo [INFO] Checking type hints...
mypy src --ignore-missing-imports

echo [INFO] Running code analysis...
pylint src

echo.
echo Code quality checks completed. Press ENTER to continue...
pause > nul

cls
echo ╔════════════════════════════════════════════════════════════╗
echo ║                    Testing Phase                          ║
echo ╚════════════════════════════════════════════════════════════╝
echo.
echo ┌─────────────────────────────────────────────────────────┐
echo │                    Running Tests                        │
echo └─────────────────────────────────────────────────────────┘

:: Run tests
python -m pytest tests/ -v --no-header --capture=no --color=yes
echo.
echo ┌─────────────────────────────────────────────────────────┐
echo │                    Test Results                         │
echo └─────────────────────────────────────────────────────────┘
echo.
echo Tests completed. Press ENTER to start the application...
pause > nul

cls
echo ╔════════════════════════════════════════════════════════════╗
echo ║                 Starting Application                      ║
echo ╚════════════════════════════════════════════════════════════╝
echo.
echo [INFO] Starting application...
echo.

python run.py
if errorlevel 1 (
    echo.
    echo [ERROR] An error occurred while running the application!
    pause
    exit /b 1
)

:: Successful exit
echo.
echo Program ended. Press ENTER to exit...
pause > nul
exit /b 0 