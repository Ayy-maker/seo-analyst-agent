#!/bin/bash

echo "🚀 Starting SEO Intelligence Platform..."
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found!"
    echo "Creating virtual environment..."
    python3 -m venv venv
    echo "✅ Virtual environment created"
    echo ""
fi

# Activate virtual environment
echo "📦 Activating virtual environment..."
source venv/bin/activate

# Check if dependencies are installed
echo "🔍 Checking dependencies..."
if ! python -c "import flask" 2>/dev/null; then
    echo "📥 Installing dependencies..."
    pip install -r requirements.txt
fi

# Kill existing server on port 5000
echo "🧹 Clearing port 5000..."
lsof -ti:5000 | xargs kill -9 2>/dev/null

echo ""
echo "════════════════════════════════════════════════════════════"
echo "✅ SEO INTELLIGENCE PLATFORM STARTING..."
echo "════════════════════════════════════════════════════════════"
echo ""
echo "📊 Dashboard: http://localhost:5000/dashboard"
echo "🎯 Competitors: http://localhost:5000/competitor-analysis"
echo "🏠 Homepage: http://localhost:5000"
echo ""
echo "Press CTRL+C to stop the server"
echo "════════════════════════════════════════════════════════════"
echo ""

# Start server
python web/app.py
