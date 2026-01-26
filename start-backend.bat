@echo off
echo ========================================
echo   Yemen ALPR System - Backend Server
echo ========================================
echo.

cd backend

echo [*] Starting Django server...
echo [*] Backend will be available at: http://localhost:8000
echo [*] Press Ctrl+C to stop
echo.

python manage.py runserver
