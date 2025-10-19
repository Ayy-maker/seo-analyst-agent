#!/bin/bash

# SEO Analyst Agent - One-Command Installer
# Usage: bash INSTALL.sh

set -e

echo "========================================"
echo "🚀 SEO Analyst Agent - Quick Installer"
echo "========================================"
echo ""

# Check Python version
echo "📌 Checking Python version..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8+ first."
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2 | cut -d'.' -f1,2)
echo "✅ Found Python $PYTHON_VERSION"
echo ""

# Create virtual environment
echo "📦 Creating virtual environment..."
python3 -m venv venv
echo "✅ Virtual environment created"
echo ""

# Install dependencies
echo "📥 Installing dependencies..."
venv/bin/pip install --upgrade pip > /dev/null 2>&1
venv/bin/pip install -r requirements.txt
echo "✅ Dependencies installed"
echo ""

# Create necessary directories
echo "📁 Setting up directories..."
mkdir -p uploads
mkdir -p outputs/html-reports
mkdir -p database
echo "✅ Directories ready"
echo ""

echo "========================================"
echo "✅ Installation Complete!"
echo "========================================"
echo ""
echo "🎉 Ready to use! Start the server with:"
echo ""
echo "   bash START_SERVER.sh"
echo ""
echo "   OR"
echo ""
echo "   venv/bin/python -c \"from web.app import app; app.run(port=5001)\""
echo ""
echo "Then open: http://localhost:5001"
echo ""
