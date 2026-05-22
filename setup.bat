@echo off
echo === WGSN Fashion Engine - Windows Setup Script ===
echo.

echo [1/4] Copying images to frontend...
if not exist "frontend\public\images" mkdir "frontend\public\images"
xcopy /s /y "backend\static\images\*" "frontend\public\images\"
echo ✅ Images copied!
echo.

echo [2/4] Installing Python dependencies...
venv\Scripts\pip.exe install -r backend\requirements.txt
echo ✅ Python packages installed!
echo.

echo [3/4] Installing Next.js dependencies...
cd frontend
npm install
cd ..
echo ✅ Next.js packages installed!
echo.

echo === SETUP COMPLETE ===
echo.
echo To run the app:
echo   Terminal 1: venv\Scripts\python.exe backend\app.py
echo   Terminal 2: cd frontend && npm run dev
echo.
echo Then open http://localhost:3000
pause
