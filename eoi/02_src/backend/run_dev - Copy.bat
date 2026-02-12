@echo off
title EOI SYSTEM - DJANGO DEV SERVER
cd /d %~dp0

echo =====================================
echo   EOI SYSTEM - DJANGO DEV SERVER
echo =====================================
echo.

echo [1/4] Making migrations...
py manage.py makemigrations
if errorlevel 1 goto :error

echo.
echo [2/4] Applying migrations...
py manage.py migrate
if errorlevel 1 goto :error

echo.
echo [3/4] Importing athletes.xlsx + horses.xlsx ...
py manage.py import_excel
if errorlevel 1 goto :error

echo.
echo [4/4] Starting server...
py manage.py runserver

goto :eof

:error
echo.
echo ERROR. Press any key to exit...
pause >nul
exit /b 1
