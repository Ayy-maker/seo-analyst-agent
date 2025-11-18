# 🚀 SEO Analyst Agent

<div align="center">

![Version](https://img.shields.io/badge/version-3.0-blue.svg)
![Python](https://img.shields.io/badge/python-3.8+-green.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Status](https://img.shields.io/badge/status-production--ready-success.svg)

**Intelligent SEO Analysis Platform That Generates Stunning Interactive HTML Reports**

[Features](#-features) • [Quick Start](#-quick-start) • [How to Run](#-how-to-run) • [Documentation](#-documentation)

</div>

---

## 🎯 What Is This?

**SEO Analyst Agent** is an intelligent automation tool that transforms raw SEO data into **stunning interactive HTML reports** with Chart.js visualizations that clients love.

### The Problem It Solves:
- ❌ Manual SEO reporting takes hours
- ❌ Clients get overwhelmed by spreadsheets
- ❌ No visual way to show improvements
- ❌ Hard to track historical trends
- ❌ Repetitive work for every client

### The Solution:
- ✅ **Upload Files** via web interface
- ✅ **Interactive HTML Reports** with Chart.js visualizations
- ✅ **Real-time Preview** in browser
- ✅ **Month-over-Month Growth** tracking (7 months)
- ✅ **Animated KPIs** and progress bars
- ✅ **Mobile Responsive** design
- ✅ **Single HTML File** - easy to share

---

## ✨ Features

### 📊 Interactive HTML Reports
<table>
<tr>
<td width="50%">

**Stunning Visual Design**
- Beautiful purple gradient headers
- 4 Interactive Chart.js visualizations
- Animated KPI dashboard
- Month-over-month growth tracking
- Color-coded performance badges
- Glassmorphism effects
- Professional Inter font typography

</td>
<td width="50%">

**Interactive Elements**
- Line charts (clicks, impressions, position)
- Bar chart (health score progress)
- Animated counters (count up on load)
- Progress bars (device distribution)
- Hover effects (cards lift and glow)
- Smooth scrolling one-page layout
- Mobile responsive design

</td>
</tr>
</table>

### 🔍 5 Complete Analysis Modules

| Module | What It Analyzes |
|--------|------------------|
| **🔑 Keywords** | Top performers, CTR, position tracking, opportunities, cannibalization |
| **🔧 Technical SEO** | Errors (4xx/5xx), Core Web Vitals, indexability, page speed, crawl depth |
| **📝 On-Page SEO** | Metadata, content quality, images, alt text, schema markup, internal links |
| **🔗 Backlinks** | Link quality, toxic links, anchor text, domain authority, diversity |
| **📈 Traffic & Conversions** | Landing pages, devices, bounce rates, engagement, conversion tracking |

### 🎨 Beautiful Visualizations

- **Interactive Charts** - 4 Chart.js visualizations with tooltips and animations
- **Clicks Trend** - Line chart showing 7 months of growth
- **Health Score Progress** - Animated bar chart (72% → 87%)
- **Impressions Growth** - Line chart in thousands
- **Position Improvement** - Inverted line chart (lower is better)
- **Device Distribution** - Animated progress bars with percentages

### 🤖 Automation & APIs

- **📧 Email Delivery** - Auto-send reports to clients
- **🔌 Google Search Console API** - Fetch data automatically
- **⏰ Scheduler** - Monthly/weekly/daily automation
- **🔄 Batch Processing** - Handle multiple clients
- **📅 Historical Tracking** - Store and compare past reports

---

## 🌐 Web Interface (PRIMARY METHOD)

**The easiest and recommended way to use the platform:**

```bash
# Start the web server
python -c "from web.app import app; app.run(port=5001)"

# Open in browser
http://localhost:5001
```

**Features:**
- 📄 **Single Upload** - Upload multiple files for one company, get consolidated report
- 📁 **Batch Upload** - Upload files for multiple companies, auto-detect brands, get all reports!
- 👁️ **Live Preview** - See your report in browser with interactive charts
- 📥 **Download** - Save complete HTML report as single file
- 📊 **Dashboard** - View all clients and statistics

**Smart Brand Detection:**
- Files are automatically grouped by company name
- Generate reports for multiple clients in one upload

---

## 🚀 Quick Start (3 Commands!)

### Option 1: Automatic Install (Easiest)

```bash
# Clone and enter directory
git clone https://github.com/Ayy-maker/seo-analyst-agent.git
cd seo-analyst-agent

# One-command install (sets up everything!)
bash INSTALL.sh

# Start server
bash START_SERVER.sh
```

### Option 2: Manual Install

```bash
# Clone repository
git clone https://github.com/Ayy-maker/seo-analyst-agent.git
cd seo-analyst-agent

# Create virtual environment
python3 -m venv venv

# Install dependencies
venv/bin/pip install -r requirements.txt

# Start server
venv/bin/python -c "from web.app import app; app.run(port=5001)"
```

**Then open:** http://localhost:5001

## 🎯 How to Run

### Method 1: Using Virtual Environment (Recommended)

```bash
# Activate virtual environment
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Start the server
python -c "from web.app import app; app.run(port=5001)"

# Open in browser
open http://localhost:5001
```

### Method 2: Direct Python Path

```bash
# Start the server (no activation needed)
venv/bin/python -c "from web.app import app; app.run(port=5001)"

# Open in browser
open http://localhost:5001
```

### Method 3: View Sample Report (Demo Only)

**For demonstration purposes only - view example output without uploading files**

```bash
# Generate a sample HTML report with realistic data
python generate_enhanced_sample_report.py

# View the sample report
open outputs/html-reports/SAMPLE-enhanced-report.html
```

**Note:** This generates a demo report with sample data. For real reports, use Method 1 or 2 to start the web server and upload your actual SEO data files.

### Using the Web Interface

1. **Start Server** - Run one of the commands above
2. **Open Browser** - Navigate to `http://localhost:5001`
3. **Upload Files** - Drag and drop or select your SEO data files
4. **Enter Details** - Company name and report period
5. **Generate** - Click "Upload & Generate Report"
6. **Preview** - View interactive report in browser
7. **Download** - Save HTML report file

That's it! 🎉

---

## 📸 Demo

### Example Output

**Generated HTML Report Includes:**

```
📄 Interactive Single-Page HTML Report
├── 📊 Executive Summary (growth context)
├── 📈 Animated KPI Dashboard (4 metrics)
├── 📊 Month-Over-Month Growth Charts
│   ├── Clicks Trend (line chart)
│   ├── Health Score Progress (bar chart)
│   ├── Impressions Growth (line chart)
│   └── Position Improvement (inverted line)
├── 🔍 Top Performing Search Queries (5 keywords)
├── 📄 Top Landing Pages (with growth indicators)
├── 📱 Device Distribution (animated progress bars)
├── 📊 Progress Comparison Table (8 metrics)
├── 💡 Strategic Recommendations (8 items)
├── 🎯 Performance Insights (Strengths & Opportunities)
└── ✅ SEO Deliverables Completed (10 items)
```

**Sample Metrics Displayed:**
- **7 months** of historical data visualized
- **4 interactive charts** with hover tooltips
- **8 metrics** with month-over-month comparison
- **5 top keywords** with performance badges
- **3 device types** with percentage breakdown
- Health Score: 87/100 (tracking from 72%)

### Report Features

```
✨ Interactive Elements:
├── Chart.js visualizations with animations
├── Animated counters (count up on load)
├── Progress bars with fill animations
├── Hover effects on all cards
├── Smooth scrolling navigation
├── Color-coded badges (🔴 🟡 🟢)
└── Mobile-responsive layout

📊 Visual Design:
├── Purple gradient header (#667eea → #764ba2)
├── Glassmorphism date badge
├── Professional Inter font
├── Box shadows and depth effects
├── Gradient backgrounds
└── Print-friendly CSS

🎯 Content Sections:
├── Executive Summary with growth context
├── 4 KPI metrics with trend indicators
├── Month-over-month visualizations
├── Strategic recommendations
├── Performance insights (strengths/opportunities)
└── Deliverables completed list
```

---

## 📚 Documentation

### Essential Guides
- **[FINAL_SETUP.md](FINAL_SETUP.md)** - Complete setup and usage guide
- **[QUICKSTART.md](QUICKSTART.md)** - Quick 2-minute setup
- **[PRD.md](PRD.md)** - Product requirements and specifications

---

## 🛠️ Usage Examples

### Web Interface (Primary Method)

```bash
# Start the server
venv/bin/python -c "from web.app import app; app.run(port=5001)"

# Open browser to http://localhost:5001
# Upload your files and generate reports!
```

### View Sample/Demo Report

```bash
# Create a demo report with sample data (for testing/preview only)
python generate_enhanced_sample_report.py

# This generates:
# - outputs/html-reports/SAMPLE-enhanced-report.html
# - Includes 7 months of mock data
# - 4 interactive Chart.js visualizations
# - All report sections populated
```

### Testing with Sample Data

```bash
# Use the provided sample files
# Located in: data/samples/
# - search-console-keywords.csv
# - traffic-analytics.csv
# - backlinks-report.csv
# - onpage-audit.csv
# - technical-audit.csv

# Upload these via web interface at http://localhost:5001
```

---

## 📋 Requirements

### System Requirements
- Python 3.8+
- 256MB RAM minimum
- 50MB disk space
- Modern web browser (Chrome, Firefox, Safari, Edge)

### Python Dependencies
```
flask
flask-cors
pandas
openpyxl
python-docx
PyPDF2
```

### API Keys (Optional)
- **Anthropic API** - For AI-powered insights ([Get key](https://console.anthropic.com/))

### Supported Data Formats
Upload any of these file types:
- ✅ **CSV** - Google Search Console, analytics exports
- ✅ **XLSX/XLS** - Excel files from any SEO tool
- ✅ **DOCX/DOC** - Word documents with SEO data
- ✅ **PDF** - PDF reports from SEO tools

### Data Sources
Works with exports from:
- ✅ Google Search Console
- ✅ Google Analytics 4
- ✅ Screaming Frog
- ✅ Ahrefs
- ✅ SEMrush
- ✅ Any SEO tool that exports to CSV/Excel

---

## 🎨 Customization

### Client Configuration

Create `config/client-name.json`:

```json
{
  "client_name": "ACME Corporation",
  "report_period": "October 2025 Monthly Report",
  "branding": {
    "primary_color": "#667eea",
    "secondary_color": "#764ba2"
  },
  "modules": {
    "keywords": { "enabled": true },
    "technical": { "enabled": true },
    "onpage": { "enabled": true },
    "backlinks": { "enabled": true },
    "traffic": { "enabled": true }
  },
  "thresholds": {
    "ranking_drop_alert": 5,
    "traffic_drop_percent": 20,
    "bounce_rate_warning": 70
  }
}
```

---

## 🔐 Environment Setup

Create `.env` file:

```bash
# Required for AI insights
ANTHROPIC_API_KEY=sk-ant-xxxxx

# Optional: Email delivery
SENDER_EMAIL=your-email@gmail.com
SENDER_PASSWORD=your-app-password
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587

# Optional: API integrations
# (Add your API keys here)
```

---

## 📊 Project Structure

```
seo-analyst-agent/
├── web/                                # Web interface
│   ├── app.py                          # Flask server (HTML-only)
│   └── templates/
│       ├── index.html                  # Upload interface
│       ├── report_preview.html         # Preview page
│       └── batch_results.html          # Batch results
├── agents/                             # Analysis agents
│   ├── analyst/                        # Extract insights
│   ├── critic/                         # Validate insights
│   └── reporter/
│       ├── enhanced_html_generator.py  # HTML report generator (Chart.js)
│       ├── html_report_generator.py    # Base HTML generator
│       └── formatter.py                # Formatting utilities
├── utils/                              # Utilities
│   ├── visualizations.py              # Chart generation
│   └── pdf_styles.py                  # Styling utilities
├── parsers/                            # Data parsers
│   ├── csv_parser.py                  # CSV parsing
│   ├── xlsx_parser.py                 # Excel parsing
│   ├── docx_parser.py                 # Word document parsing
│   └── pdf_parser.py                  # PDF parsing
├── data/
│   └── samples/                        # Sample data (generic)
├── outputs/
│   └── html-reports/                   # Generated HTML reports
├── database/                           # SQLite database
├── generate_enhanced_sample_report.py  # Sample generator
├── main.py                             # CLI interface
├── requirements.txt                    # Dependencies
├── README.md                           # This file
├── FINAL_SETUP.md                      # Complete setup guide
└── QUICKSTART.md                       # Quick start guide
```

---

## 🚀 Current Features (v3.0)

### ✅ Interactive HTML Reports
- [x] Chart.js visualizations (4 interactive charts)
- [x] Month-over-month growth tracking (7 months)
- [x] Animated KPI dashboard
- [x] Device distribution with progress bars
- [x] Mobile-responsive design
- [x] Single-file HTML output

### ✅ Web Platform
- [x] Flask web interface
- [x] File upload (CSV, XLSX, DOCX, PDF)
- [x] Live preview in browser
- [x] Batch processing for multiple companies
- [x] Multi-client dashboard
- [x] Report download

### ✅ Data Processing
- [x] CSV/XLSX/DOCX/PDF parsing
- [x] Multiple file format support
- [x] Smart data consolidation
- [x] Historical data storage (SQLite)
- [x] Sample data with generic placeholders

### 🔮 Future Enhancements
- [ ] Real-time data integration (Google Search Console API)
- [ ] Automated email delivery
- [ ] Custom branding/white-label
- [ ] PDF export option
- [ ] More chart types (geographic, funnel, sankey)
- [ ] AI-powered insights (with Anthropic Claude)

---

## 🤝 Contributing

Contributions welcome! Areas for improvement:

- **New Modules**: Content analysis, local SEO, mobile SEO
- **More Charts**: Trend lines, comparison bars, geographic maps
- **API Integrations**: Analytics, Ahrefs, SEMrush
- **UI**: Web interface for non-technical users
- **Export Formats**: PowerPoint, Google Slides, Excel

See [IMPROVEMENTS.md](IMPROVEMENTS.md) for full list.

---

## 📄 License

MIT License - feel free to use for commercial projects!

---

## 🙏 Acknowledgments

Built with:
- [ReportLab](https://www.reportlab.com/) - PDF generation
- [Matplotlib](https://matplotlib.org/) - Visualizations
- [Anthropic Claude](https://www.anthropic.com/) - AI insights
- [Google APIs](https://developers.google.com/) - Data integration

---

## 💬 Support

- **Issues**: [GitHub Issues](https://github.com/Ayy-maker/seo-analyst-agent/issues)
- **Discussions**: [GitHub Discussions](https://github.com/Ayy-maker/seo-analyst-agent/discussions)
- **Documentation**: See [docs folder](/) for guides

---

## 📈 Stats

- **Clean, production-ready codebase**
- **HTML-only reporting** (no PDF bloat)
- **4 interactive Chart.js visualizations**
- **40KB average report size**
- **7 months historical tracking**
- **SQLite database** for data persistence
- **Mobile-responsive** design
- **Single-file HTML** output
- **No sensitive data** in examples

---

<div align="center">

**Made with ❤️ for SEO professionals who want to work smarter, not harder**

⭐ Star this repo if you find it useful!

[Get Started](#-quick-start) • [View Demo](#-demo) • [Read Docs](#-documentation)

</div>
