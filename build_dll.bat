@echo off
echo Building YouTube Downloader DLL...

REM Activate virtual environment if it exists
if exist .venv\Scripts\activate.bat (
    call .venv\Scripts\activate.bat
    echo Virtual environment activated.
) else (
    echo No virtual environment found. Creating one...
    python -m venv .venv
    call .venv\Scripts\activate.bat
    echo Virtual environment created and activated.
)

REM Install required packages
echo Installing required packages...
pip install -r requirements.txt

REM Build the DLL
echo Building the DLL...
python setup.py build_ext --inplace

if %ERRORLEVEL% EQU 0 (
    echo.
    echo Build successful! The DLL is now available as downloader_dll.pyd
    echo.
) else (
    echo.
    echo Build failed. Please check the error messages above.
    echo.
)

REM Deactivate virtual environment
call .venv\Scripts\deactivate.bat

pause