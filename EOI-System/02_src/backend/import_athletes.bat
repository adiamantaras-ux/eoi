@echo off
cd /d %~dp0
py manage.py import_athletes --file "..\..\01_docs\03_excel_sources\athletes.xlsx"
pause
