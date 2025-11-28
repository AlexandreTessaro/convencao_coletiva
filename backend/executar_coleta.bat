@echo off
chcp 65001 >nul
cd /d "%~dp0"
call venv\Scripts\activate.bat
python collect_convencoes.py %1
pause

