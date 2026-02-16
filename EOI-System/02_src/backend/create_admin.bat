@echo off
chcp 65001 >nul
title Create Django Admin (Superuser)

cd /d %~dp0

echo Creating Django superuser...
echo.
py manage.py createsuperuser
echo.
pause
