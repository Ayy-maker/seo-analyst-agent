#!/bin/bash
# SEO Analyst Agent - Quick Analysis Script
# Usage: ./run_analysis.sh

set -e  # Exit on error

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${BLUE}🚀 SEO Analyst Agent - Starting Analysis${NC}\n"

# Get script directory
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$DIR"

# Activate virtual environment
echo -e "${YELLOW}📦 Activating environment...${NC}"
source venv/bin/activate

# Check if data files exist
if [ ! "$(ls -A data/*.csv 2>/dev/null)" ] && [ ! "$(ls -A data/*.xlsx 2>/dev/null)" ]; then
    echo -e "${YELLOW}⚠️  No data files found in data/ folder${NC}"
    echo "Please add CSV or XLSX files to the data/ folder first"
    echo ""
    echo "Example:"
    echo "  cp ~/Downloads/search-console-export.csv data/"
    echo ""
    exit 1
fi

# Show files to be analyzed
echo -e "\n${GREEN}📊 Files to analyze:${NC}"
ls -1 data/*.{csv,xlsx} 2>/dev/null || true
echo ""

# Run analysis
echo -e "${BLUE}🔍 Running analysis...${NC}\n"
python main.py analyze --reports data/*.csv data/*.xlsx 2>/dev/null || \
python main.py analyze --reports data/*.csv 2>/dev/null || \
python main.py analyze --reports data/*.xlsx

# Find latest PDF
LATEST_PDF=$(ls -t outputs/pdf-reports/*.pdf 2>/dev/null | head -1)

if [ -n "$LATEST_PDF" ]; then
    echo -e "\n${GREEN}✅ Analysis complete!${NC}"
    echo -e "${GREEN}📄 Report: $LATEST_PDF${NC}\n"
    
    # Ask if user wants to open PDF
    read -p "Open PDF report? (y/n) " -n 1 -r
    echo ""
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        open "$LATEST_PDF"
    fi
else
    echo -e "\n${YELLOW}⚠️  No PDF generated${NC}"
fi

echo -e "\n${BLUE}📁 All reports saved in outputs/ folder${NC}\n"
