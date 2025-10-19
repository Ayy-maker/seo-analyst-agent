#!/bin/bash

# SEO Analyst Agent - Server Startup Script
# Starts the Flask web server for the SEO Intelligence Platform

echo "========================================"
echo "🚀 Starting SEO Analyst Agent Server"
echo "========================================"
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found!"
    echo ""
    echo "Please run the installer first:"
    echo "   bash INSTALL.sh"
    echo ""
    exit 1
fi

# Check if port 5001 is already in use
if lsof -Pi :5001 -sTCP:LISTEN -t >/dev/null 2>&1 ; then
    echo "⚠️  Port 5001 is already in use"
    echo ""
    echo "Killing existing process..."
    lsof -ti:5001 | xargs kill -9 2>/dev/null
    sleep 1
    echo "✅ Port cleared"
    echo ""
fi

echo "📦 Using virtual environment..."
echo "🌐 Starting Flask server..."
echo ""
echo "✅ Server will be available at:"
echo "   → http://localhost:5001"
echo "   → http://127.0.0.1:5001"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""
echo "========================================"
echo ""

# Start the server
venv/bin/python -c "from web.app import app; app.run(host='0.0.0.0', port=5001, debug=False)"
