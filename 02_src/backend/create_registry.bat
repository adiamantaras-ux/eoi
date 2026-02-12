@echo off
chcp 65001 >nul
title Create Registry app

cd /d %~dp0
py manage.py startapp registry
pause
