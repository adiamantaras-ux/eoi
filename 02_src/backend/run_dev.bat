@echo off
chcp 65001 >nul
title EOI Django Dev Server

cd /d %~dp0

echo =====================================
echo   EOI SYSTEM - DJANGO DEV SERVER
echo =====================================
echo.

echo [1/4] Making migrations...
py manage.py makemigrations
if errorlevel 1 (
  echo ERROR in makemigrations.
  pause
  exit /b
)
echo.

echo [2/4] Applying migrations...
py manage.py migrate
if errorlevel 1 (
  echo ERROR in migrate.
  pause
  exit /b
)
echo.

echo [3/4] Importing athletes.xlsx + horses.xlsx ...
py manage.py import_excel
if errorlevel 1 (
  echo ERROR in Excel import.
  pause
  exit /b
)
echo.

echo [4/4] Starting server...
start "" http://127.0.0.1:8000/admin
py manage.py runserver 127.0.0.1:8000
pause
