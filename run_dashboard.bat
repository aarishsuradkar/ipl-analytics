@echo off
title IPL Analytics Dashboard
cd /d "%~dp0"
echo ===================================================
echo Starting IPL Analytics Dashboard on http://localhost:8501
echo ===================================================
echo.
start http://localhost:8501
".\venv\Scripts\streamlit.exe" run app.py
pause
