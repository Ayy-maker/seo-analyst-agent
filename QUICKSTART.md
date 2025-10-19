# Quick Start Guide - 2 Minutes ⚡

Get the SEO Analyst Agent running with interactive HTML reports in 2 minutes.

## Step 1: Install Dependencies (30 seconds)

```bash
# Clone the repository (if you haven't already)
git clone https://github.com/Ayy-maker/seo-analyst-agent.git
cd seo-analyst-agent

# Create virtual environment
python3 -m venv venv

# Activate it
source venv/bin/activate  # On macOS/Linux
# or
venv\Scripts\activate  # On Windows

# Install requirements
pip install -r requirements.txt
```

## Step 2: Start the Server (10 seconds)

```bash
# Start the Flask web server
python -c "from web.app import app; app.run(port=5001)"

# Or use venv directly without activation
venv/bin/python -c "from web.app import app; app.run(port=5001)"
```

You should see:
```
 * Running on http://127.0.0.1:5001
```

## Step 3: Open in Browser (5 seconds)

Open your browser and go to: **http://localhost:5001**

## Step 4: Generate Your First Report (1 minute)

### Option A: Upload Files

1. Click "Choose files" or drag & drop your SEO data files
2. Enter company name and report period
3. Click "Upload & Generate Report"
4. View the interactive HTML report with charts!

### Option B: Use Sample Data

```bash
# Generate a sample report with realistic data
venv/bin/python generate_enhanced_sample_report.py

# Open the generated file
open outputs/html-reports/SAMPLE-enhanced-report.html
```

## What You Get 🎉

Your HTML report includes:

- ✨ **4 Interactive Chart.js Visualizations**
  - Clicks Trend (7 months)
  - Health Score Progress
  - Impressions Growth
  - Position Improvement

- 📊 **Animated KPI Dashboard**
  - Total Clicks with growth %
  - Impressions with trends
  - CTR improvements
  - Average Position changes

- 📈 **Month-Over-Month Growth**
  - 7 months of historical data
  - Progress comparison table
  - Growth percentages

- 📱 **Device Distribution**
  - Mobile, Desktop, Tablet breakdown
  - Animated progress bars

- 💡 **Strategic Recommendations**
  - Top performing keywords
  - Landing page insights
  - Deliverables completed

All in a single, responsive HTML file!

## Supported File Types

Upload any of these:
- ✅ CSV - Google Search Console exports
- ✅ XLSX/XLS - Excel files from any SEO tool
- ✅ DOCX/DOC - Word documents with SEO data
- ✅ PDF - PDF reports from SEO tools

## Quick Commands Reference

### Start Server
```bash
# Method 1: Activate venv first
source venv/bin/activate
python -c "from web.app import app; app.run(port=5001)"

# Method 2: Direct python path (no activation needed)
venv/bin/python -c "from web.app import app; app.run(port=5001)"
```

### Generate Sample Report
```bash
venv/bin/python generate_enhanced_sample_report.py
```

### View Sample Report
```bash
open outputs/html-reports/SAMPLE-enhanced-report.html
```

## Common Issues & Solutions

### Port 5001 Already in Use
```bash
# Kill the existing process
lsof -ti:5001 | xargs kill -9

# Start server again
venv/bin/python -c "from web.app import app; app.run(port=5001)"
```

### "No module named 'flask'"
```bash
# Make sure you're using the venv python
venv/bin/pip install -r requirements.txt
```

### "python: command not found"
```bash
# Use python3 or venv/bin/python
python3 -m venv venv
venv/bin/python -c "from web.app import app; app.run(port=5001)"
```

### Report Not Found / No Preview
This has been fixed! The issue was that HTML file paths weren't being stored in the database. The latest version (commit f49550c) includes:
- ✅ HTML file paths stored in database
- ✅ Preview and download buttons work correctly
- ✅ Graceful error handling for missing files

**If you still see this issue:**
1. Pull the latest changes: `git pull origin main`
2. Restart the server
3. Generate a new report

## Next Steps

### 1. Upload Your Real Data
- Export from Google Search Console (CSV)
- Export from Google Analytics (XLSX)
- Upload via web interface at http://localhost:5001

### 2. Batch Processing
- Upload multiple files for different companies
- Automatic brand detection
- Generate reports for all clients at once

### 3. Explore Features
- Interactive charts with hover tooltips
- Responsive design (works on mobile)
- Single HTML file (easy to share)
- No PDF dependencies

### 4. Optional: Add AI Insights
If you want AI-powered insights:
```bash
# Add your Anthropic API key to .env
echo "ANTHROPIC_API_KEY=your-key-here" > .env
```
Get a key at: https://console.anthropic.com/

**Note:** AI insights are optional. The reports work great with the sample data!

## Example Workflow

1. **Start Server**
   ```bash
   venv/bin/python -c "from web.app import app; app.run(port=5001)"
   ```

2. **Open Browser**
   ```
   http://localhost:5001
   ```

3. **Upload Files**
   - Drag & drop your SEO reports
   - Or click "Choose files"

4. **Enter Details**
   - Company Name: "Your Client Name"
   - Report Period: "September 2024"

5. **Generate Report**
   - Click "Upload & Generate Report"
   - Wait 2-3 seconds

6. **View & Download**
   - Click "👁️ Preview Report" to see it in browser
   - Click "📥 Download HTML Report" to save it
   - Share the HTML file with your client!

## That's It! 🚀

You now have a professional SEO reporting tool that generates stunning interactive HTML reports.

**Questions or Issues?**
- Check the main [README.md](README.md) for detailed documentation
- See [FINAL_SETUP.md](FINAL_SETUP.md) for complete setup guide
- Read [PRD.md](PRD.md) for product specifications

Happy reporting! 📊✨
