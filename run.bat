@echo off
REM Guardian Angels - Windows Quick Start Script

echo.
echo ====================================
echo Guardian Angels - Setup & Run
echo ====================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8+ and add it to PATH
    pause
    exit /b 1
)

echo [1/6] Python found: 
python --version
echo.

REM Check if pip is available
pip --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: pip is not available
    pause
    exit /b 1
)

REM Install requirements
echo [2/6] Installing Python dependencies...
echo This may take a few minutes...
pip install -r requirements.txt
if errorlevel 1 (
    echo WARNING: Some packages may have failed to install
    echo Trying alternative MySQL backend...
    pip install PyMySQL
    echo Please add the following to guardian_angels/settings.py after imports:
    echo import pymysql
    echo pymysql.install_as_MySQLdb()
)
echo.

REM Run migrations
echo [3/6] Running database migrations...
python manage.py migrate
if errorlevel 1 (
    echo ERROR: Migration failed
    echo Ensure MySQL is running in XAMPP
    pause
    exit /b 1
)
echo.

REM Populate demo data
echo [4/6] Populating demo data...
python manage.py populate_demo_data
if errorlevel 1 (
    echo WARNING: Demo data population failed (this is optional)
)
echo.

REM Collect static files
echo [5/6] Collecting static files...
python manage.py collectstatic --noinput >nul 2>&1
echo.

REM Start server
echo [6/6] Starting development server...
echo.
echo ====================================
echo Guardian Angels is running!
echo ====================================
echo.
echo Access the application at:
echo   Main Site: http://localhost:8000
echo   Admin:     http://localhost:8000/admin
echo.
echo Demo Credentials:
echo   Doctor: dr.rajesh@guardianangels.com / password123
echo   Patient: john.doe@example.com / password123
echo.
echo Press Ctrl+C to stop the server
echo ====================================
echo.

python manage.py runserver

pause
