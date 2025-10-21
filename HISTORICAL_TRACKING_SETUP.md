# 📊 Historical Tracking System - Setup Complete!

**Date:** October 20, 2025
**Status:** ✅ **FULLY OPERATIONAL**

---

## 🎯 What Was Implemented

### 1. **Monthly Snapshot System**

**SnapshotManager Class** (`utils/snapshot_manager.py`)
- Captures monthly SEO performance data
- Stores GSC metrics (clicks, impressions, CTR, position)
- Stores GA4 metrics (users, sessions, engagement)
- Calculates month-over-month changes
- Provides trend data for charts

**Database Table** (`monthly_snapshots`)
```sql
CREATE TABLE monthly_snapshots (
    id INTEGER PRIMARY KEY,
    client_id INTEGER NOT NULL,
    snapshot_date DATE NOT NULL,
    snapshot_month TEXT NOT NULL,

    -- GSC Metrics
    total_clicks INTEGER,
    total_impressions INTEGER,
    avg_ctr REAL,
    avg_position REAL,
    total_queries INTEGER,

    -- GA4 Metrics
    total_users INTEGER,
    total_sessions INTEGER,
    total_pageviews INTEGER,
    engagement_rate REAL,
    bounce_rate REAL,

    -- Month-over-Month Changes
    clicks_change_percent REAL,
    impressions_change_percent REAL,
    ctr_change_percent REAL,
    position_change REAL,
    users_change_percent REAL
);
```

### 2. **Snapshot Capture Script**

**capture_monthly_snapshot.py**
- Fetches current GSC data for all clients
- Fetches current GA4 data for all clients
- Captures snapshots with real metrics
- Displays summary and changes

**Current Snapshots** (captured October 20, 2025):

| Client | Clicks | Impressions | CTR | Avg Position | Users | Sessions |
|--------|--------|-------------|-----|--------------|-------|----------|
| Hot Tyres | 86 | 14,349 | 0.60% | 29.2 | 355 | 401 |
| Instant Auto Traders | 11 | 2,486 | 0.44% | 32.9 | 138 | 164 |
| SADC Disability Services | 6 | 594 | 1.01% | 50.6 | 70 | 81 |
| The Profit Platform | 5 | 1,673 | 0.30% | 57.2 | 2,973 | 3,154 |

### 3. **Trend Visualization in Reports**

**Enhanced HTML Generator** (`agents/reporter/enhanced_html_generator.py`)
- Added `client_id` parameter to `generate_full_report()`
- Created `_add_historical_trends()` method to fetch snapshot data
- Updated `_get_chartjs_code()` to generate real Chart.js visualizations
- Added 3 interactive charts:
  - **Clicks & Impressions Trend** (line chart)
  - **Average Position Trend** (line chart, inverted)
  - **Users & Sessions Trend** (bar chart)

**Chart Features:**
- Real historical data from monthly snapshots
- Interactive tooltips
- Responsive design
- Chronological display (oldest to newest)
- Automatically enabled when 2+ months of data exist

### 4. **Automated Monthly Scheduler**

**Systemd Timer** (`seo-snapshot-capture.timer`)
- Runs on the 1st of each month at 2:00 AM UTC
- Randomized delay up to 1 hour (to avoid load spikes)
- Persistent (runs missed executions if system was off)

**Systemd Service** (`seo-snapshot-capture.service`)
- Executes `capture_monthly_snapshot.py`
- Runs in project virtual environment
- Logs to systemd journal

**Next Scheduled Run:** November 1, 2025 at 00:04:16 UTC

---

## 🚀 How It Works

### 1. **Monthly Snapshot Capture**

On the 1st of each month, the system automatically:

1. Fetches last 30 days of GSC data for each client
2. Fetches last 30 days of GA4 data for each client
3. Normalizes the data using `data_normalizer`
4. Captures snapshot with `snapshot_manager.capture_snapshot()`
5. Calculates month-over-month changes
6. Stores in database with snapshot month (e.g., "2025-10")

### 2. **Report Generation with Trends**

When generating a report:

1. Web app calls `html_generator.generate_full_report(client_id=client_id)`
2. Generator calls `_add_historical_trends(seo_data, client_id)`
3. `_add_historical_trends()` checks if client has 2+ snapshots
4. If yes, fetches last 12 months of snapshots
5. Converts to `monthly_progress` data structure
6. Adds to `seo_data` with `has_historical_data=True`
7. `_get_chartjs_code()` generates Chart.js code with real data
8. Report includes interactive trend charts

### 3. **Viewing Historical Trends**

**For clients with 1 snapshot:**
- Report shows current baseline data
- Message: "Historical charts will appear next month"

**For clients with 2+ snapshots:**
- Report shows interactive trend charts
- Charts display month-by-month progression
- Hover over data points to see exact values
- Visual representation of growth/decline

---

## 📁 Files Created/Modified

### Created Files:
- `utils/snapshot_manager.py` - Snapshot capture and retrieval
- `capture_monthly_snapshot.py` - Monthly snapshot script
- `init_clients.py` - Initialize clients in database
- `seo-snapshot-capture.service` - Systemd service
- `seo-snapshot-capture.timer` - Systemd timer
- `HISTORICAL_TRACKING_SETUP.md` - This documentation

### Modified Files:
- `agents/reporter/enhanced_html_generator.py`
  - Added `client_id` parameter (line 42)
  - Added `_add_historical_trends()` method (lines 228-272)
  - Updated `_get_chartjs_code()` to generate real charts (lines 1651-1769)
  - Updated call to pass `data` parameter (line 483)
  - Added import for `snapshot_manager` (line 22)

- `web/app.py`
  - Updated 2 calls to `generate_full_report()` to pass `client_id` (lines 319, 521)

---

## 🎯 Usage

### Manual Snapshot Capture

Run anytime to capture current month's data:

```bash
cd /home/avi/projects/seoanalyst/seo-analyst-agent
source venv/bin/activate
python capture_monthly_snapshot.py
```

### Check Scheduler Status

```bash
# View timer status and next run time
sudo systemctl status seo-snapshot-capture.timer

# View all timers
sudo systemctl list-timers

# View snapshot capture logs
sudo journalctl -u seo-snapshot-capture.service -f
```

### Test Snapshot Service

```bash
# Manually trigger snapshot capture
sudo systemctl start seo-snapshot-capture.service

# Check if it ran successfully
sudo systemctl status seo-snapshot-capture.service
```

### Query Snapshot Data

```python
from utils.snapshot_manager import snapshot_manager

# Get latest snapshot for client
snapshot = snapshot_manager.get_latest_snapshot(client_id=1)

# Get last 6 months of snapshots
snapshots = snapshot_manager.get_snapshots(client_id=1, months=6)

# Get trend data for specific metric
trend = snapshot_manager.get_trend_data(
    client_id=1,
    metric='total_clicks',
    months=12
)

# Check snapshot count
count = snapshot_manager.get_snapshot_count(client_id=1)
```

---

## 📊 Database Snapshots

**Current Status** (as of October 20, 2025):

```
Hot Tyres:
   Total Snapshots: 1
   Latest: 2025-10
   ⏳ Need 1 more month for comparison

Instant Auto Traders:
   Total Snapshots: 1
   Latest: 2025-10
   ⏳ Need 1 more month for comparison

SADC Disability Services:
   Total Snapshots: 1
   Latest: 2025-10
   ⏳ Need 1 more month for comparison

The Profit Platform:
   Total Snapshots: 1
   Latest: 2025-10
   ⏳ Need 1 more month for comparison
```

**After November 1, 2025:**
- All clients will have 2 snapshots
- Month-over-month changes will be calculated
- Trend charts will appear in reports
- Reports will show growth/decline percentages

---

## 🎨 Chart Examples

Once historical data exists, reports will include:

### 1. Clicks & Impressions Trend
```
Line chart showing:
- Clicks (red line)
- Impressions in thousands (blue line)
- Monthly progression over time
```

### 2. Average Position Trend
```
Line chart showing:
- Average position (yellow line, inverted scale)
- Lower positions = better ranking
- Visual representation of SEO improvement
```

### 3. Users & Sessions Trend
```
Bar chart showing:
- Users (teal bars)
- Sessions (purple bars)
- Traffic growth over time
```

---

## ⚙️ Configuration

### Change Schedule

Edit `/etc/systemd/system/seo-snapshot-capture.timer`:

```ini
# Run on 1st of month at 2 AM
OnCalendar=monthly

# Run every 2 weeks
OnCalendar=biweekly

# Run on specific day/time
OnCalendar=*-*-01 02:00:00
```

Then reload:
```bash
sudo systemctl daemon-reload
sudo systemctl restart seo-snapshot-capture.timer
```

### Change Snapshot Data Range

Edit `capture_monthly_snapshot.py` line 85:

```python
# Change from 30 days to 60 days
queries = gsc_client.fetch_queries_with_metrics(gsc_property, days=60)
```

---

## 🔍 Troubleshooting

### Timer Not Running?

```bash
# Check timer is enabled
sudo systemctl is-enabled seo-snapshot-capture.timer

# Check timer is active
sudo systemctl is-active seo-snapshot-capture.timer

# View timer logs
sudo journalctl -u seo-snapshot-capture.timer
```

### Service Failed?

```bash
# View service logs
sudo journalctl -u seo-snapshot-capture.service -n 50

# Test service manually
sudo systemctl start seo-snapshot-capture.service

# Check for errors
sudo systemctl status seo-snapshot-capture.service
```

### No Historical Data?

```python
from database import DatabaseManager
from utils.snapshot_manager import snapshot_manager

db = DatabaseManager()
clients = db.get_all_clients()

for client in clients:
    count = snapshot_manager.get_snapshot_count(client['id'])
    print(f"{client['name']}: {count} snapshots")
```

---

## 📈 Timeline

**October 20, 2025:**
- ✅ Snapshot system created
- ✅ Initial snapshots captured for all 4 clients
- ✅ Report generator updated with trend support
- ✅ Automated scheduler configured

**November 1, 2025:**
- 🔜 Second snapshot will be captured
- 🔜 Month-over-month changes will be calculated
- 🔜 Trend charts will appear in reports

**December 1, 2025:**
- 🔜 Third snapshot captured
- 🔜 3-month trend visible
- 🔜 Historical patterns emerging

**Future:**
- After 6 months: Strong trend data
- After 12 months: Full year-over-year comparison
- Unlimited historical tracking

---

## 🎉 Success Metrics

### Before Historical Tracking:
- ❌ No month-over-month comparisons
- ❌ No trend visualizations
- ❌ Static baseline reports only
- ❌ No growth measurement

### After Historical Tracking:
- ✅ Automatic monthly snapshots
- ✅ Month-over-month change calculations
- ✅ Interactive trend charts
- ✅ Growth visualization
- ✅ Long-term performance tracking
- ✅ Data-driven insights

---

## 💡 Next Steps

1. **Wait for November 1** - First automated snapshot will be captured
2. **Generate New Reports** - After Nov 1, reports will show trends
3. **Review Trend Data** - Verify charts are displaying correctly
4. **Monitor Scheduler** - Check logs to ensure monthly captures work
5. **Build History** - Over time, collect 12+ months of data for comprehensive trends

---

## 🔗 Related Files

- **Snapshot Manager:** `utils/snapshot_manager.py`
- **Capture Script:** `capture_monthly_snapshot.py`
- **Report Generator:** `agents/reporter/enhanced_html_generator.py`
- **Web App:** `web/app.py`
- **Systemd Service:** `/etc/systemd/system/seo-snapshot-capture.service`
- **Systemd Timer:** `/etc/systemd/system/seo-snapshot-capture.timer`

---

**System Status:** ✅ Production Ready
**Next Snapshot:** November 1, 2025 at 00:04:16 UTC
**Current Snapshots:** 4 clients with 1 snapshot each
**Trend Charts:** Will activate after November 1, 2025

**Welcome to automated historical tracking!** 📊✨
