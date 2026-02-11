@echo off
chcp 65001 >nul
title Create ORGANIZATIONS app

cd /d %~dp0

if exist organizations\apps.py (
  echo organizations app already exists.
) else (
  echo Creating organizations app...
  py manage.py startapp organizations
)

echo.
pause
