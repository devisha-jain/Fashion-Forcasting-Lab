#!/bin/bash
echo "=== WGSN Fashion Engine - Unix Setup Script ==="
echo ""

echo "[1/4] Copying images to frontend public folder..."
mkdir -p frontend/public/images
cp -R backend/static/images/* frontend/public/images/ 2>/dev/null
echo "✅ Images copied!"
echo ""

echo "[2/4] Installing Python dependencies..."
if [ -d "venv" ]; then
    ./venv/bin/pip install -r backend/requirements.txt
else
    pip install -r backend/requirements.txt
fi
echo "✅ Python packages installed!"
echo ""

echo "[3/4] Installing Next.js dependencies..."
cd frontend
npm install
cd ..
echo "✅ Next.js packages installed!"
echo ""

echo "=== SETUP COMPLETE ==="
echo ""
echo "To run the services:"
echo "  Terminal 1: cd backend && ../venv/bin/python app.py"
echo "  Terminal 2: cd frontend && npm run dev"
echo ""
