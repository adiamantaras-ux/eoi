echo off
chcp 65001 >nul
title EOI - Update DB (migrations)

cd /d %~dp0

echo Making migrations...
py manage.py makemigrations accounts organizations registry

echo.
echo Migrating...
py manage.py migrate

echo.
echo Done.
pause