@echo off
title EOI - RESET DEV DATABASE
cd /d %~dp0

echo =====================================
echo   RESET DEV DATABASE (SQLite)
echo =====================================
echo.

REM 1) Σβήσε την SQLite βάση
if exist db.sqlite3 (
  echo Deleting db.sqlite3...
  del /q db.sqlite3
)

REM 2) Σβήσε migrations του accounts (κρατάμε μόνο __init__.py)
if exist accounts\migrations (
  echo Cleaning accounts migrations...
  for %%f in (accounts\migrations\*.py) do (
    if /I not "%%~nxf"=="__init__.py" del /q "%%f"
  )
)

REM 3) Καθάρισμα cache (προαιρετικό)
if exist accounts\__pycache__ rmdir /s /q accounts\__pycache__
if exist config\__pycache__ rmdir /s /q config\__pycache__

echo.
echo Rebuilding migrations...
py manage.py makemigrations accounts
if errorlevel 1 (
  echo ERROR in makemigrations.
  pause
  exit /b
)

echo.
echo Applying migrations...
py manage.py migrate
if errorlevel 1 (
  echo ERROR in migrate.
  pause
  exit /b
)

echo.
echo ✅ Database reset completed.
pause

