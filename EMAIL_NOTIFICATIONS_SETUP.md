# 📧 Email Notifications Setup Guide

**Date:** October 20, 2025
**Status:** ✅ Configured (awaiting SMTP credentials)
**Notification Email:** ${NOTIFICATION_EMAIL}

---

## 🎯 What's Been Set Up

### Notification System Components:

1. ✅ **NotificationService** (`utils/notification_service.py`)
   - Send system status notifications
   - Send snapshot capture notifications
   - Send report generation notifications
   - Professional HTML email templates

2. ✅ **Notification Email Configured**
   - Target email: `${NOTIFICATION_EMAIL}`
   - Set in `.env` file as `NOTIFICATION_EMAIL`

3. ✅ **Test Notification Script** (`send_test_notification.py`)
   - Sends test notification to verify setup
   - Saves HTML file if email credentials not configured
   - Includes setup instructions

4. ✅ **Test Notification Created**
   - Saved as HTML file: `outputs/notifications/notification-2025-10-20-150240.html`
   - View at: https://seo.theprofitplatform.com.au/preview/outputs/notifications/notification-2025-10-20-150240.html
   - Contains current system status with all client data

---

## 🚀 How to Enable Email Sending

To actually send emails (instead of just saving HTML files), you need to configure SMTP credentials.

### Step 1: Enable 2-Factor Authentication on Gmail

1. Go to https://myaccount.google.com/security
2. Find "2-Step Verification"
3. Click "Get Started" and follow the instructions
4. Enable 2-Step Verification

### Step 2: Generate App Password

1. Go to https://myaccount.google.com/apppasswords
2. Select "Mail" from the app dropdown
3. Select "Other (Custom name)" from the device dropdown
4. Enter "SEO Analyst" as the app name
5. Click "Generate"
6. Copy the 16-character password (it will look like: `xxxx xxxx xxxx xxxx`)

### Step 3: Add Credentials to .env File

```bash
# Add these lines to your .env file
echo 'SENDER_EMAIL=your-email@gmail.com' >> /home/avi/projects/seoanalyst/seo-analyst-agent/.env
echo 'SENDER_PASSWORD=your-16-char-app-password' >> /home/avi/projects/seoanalyst/seo-analyst-agent/.env
```

**Important:**
- Use your actual Gmail address for `SENDER_EMAIL`
- Use the 16-character app password (not your regular Gmail password)
- Remove spaces from the app password

### Step 4: Test the Email System

```bash
cd /home/avi/projects/seoanalyst/seo-analyst-agent
source venv/bin/activate
python send_test_notification.py
```

This will send a test notification to `${NOTIFICATION_EMAIL}`.

---

## 📬 Types of Notifications

### 1. System Status Notifications

**What it includes:**
- Production service status (seo-analyst, snapshot scheduler)
- Historical tracking data for all 4 clients
- Latest snapshot metrics (clicks, impressions, position)
- Quick links to dashboard and reports

**How to send manually:**
```bash
cd /home/avi/projects/seoanalyst/seo-analyst-agent
source venv/bin/activate
python send_test_notification.py
```

**Or using Python:**
```python
from utils.notification_service import notification_service

notification_service.send_system_status(
    recipient='${NOTIFICATION_EMAIL}'
)
```

### 2. Snapshot Capture Notifications

**What it includes:**
- Client name
- Snapshot month
- Metrics: clicks, impressions, position, CTR, users
- Timestamp

**How to send:**
```python
from utils.notification_service import notification_service

snapshot_data = {
    'snapshot_month': '2025-10',
    'total_clicks': 86,
    'total_impressions': 14349,
    'avg_position': 29.2,
    'avg_ctr': 0.6,
    'total_users': 355
}

notification_service.send_snapshot_notification(
    client_name='Hot Tyres',
    snapshot_data=snapshot_data,
    recipient='${NOTIFICATION_EMAIL}'
)
```

### 3. Report Generation Notifications

**What it includes:**
- Client name
- Report filename and size
- Generation timestamp
- Direct link to view report

**How to send:**
```python
from utils.notification_service import notification_service

notification_service.send_report_notification(
    client_name='The Profit Platform',
    report_path='outputs/html-reports/seo-report-the-profit-platform-2025-10-20-150240.html',
    recipient='${NOTIFICATION_EMAIL}'
)
```

---

## 🔄 Automated Notifications

### Option 1: Add to Monthly Snapshot Script

Edit `capture_monthly_snapshot.py` to send notifications when snapshots are captured:

```python
# At the end of the snapshot capture for each client:
from utils.notification_service import notification_service

notification_service.send_snapshot_notification(
    client_name=client['name'],
    snapshot_data=snapshot_data,
    recipient='${NOTIFICATION_EMAIL}'
)
```

### Option 2: Add to Report Generation

Edit `web/app.py` to send notifications when reports are generated:

```python
# After generating HTML report:
from utils.notification_service import notification_service

notification_service.send_report_notification(
    client_name=company_name,
    report_path=report_path,
    recipient='${NOTIFICATION_EMAIL}'
)
```

### Option 3: Scheduled Daily/Weekly Status

Create a cron job or systemd timer to send regular status updates:

```bash
# Daily status email at 8 AM
0 8 * * * /home/avi/projects/seoanalyst/seo-analyst-agent/venv/bin/python /home/avi/projects/seoanalyst/seo-analyst-agent/send_test_notification.py
```

---

## 📊 Current Notification Preview

The test notification created today includes:

### Production Services Status:
- ✅ SEO Analyst Service: ACTIVE
- ✅ Snapshot Scheduler: ACTIVE
- 📅 Next snapshot: Sat 2025-11-01 00:22:24 UTC

### Client Data:

| Client | Snapshots | Latest | Clicks | Impressions | Position |
|--------|-----------|--------|--------|-------------|----------|
| Hot Tyres | 1 | 2025-10 | 86 | 14,349 | 29.2 |
| Instant Auto Traders | 1 | 2025-10 | 11 | 2,486 | 32.9 |
| SADC Disability Services | 1 | 2025-10 | 6 | 594 | 50.6 |
| The Profit Platform | 1 | 2025-10 | 5 | 1,673 | 57.2 |

**View the notification:**
- Web: https://seo.theprofitplatform.com.au/preview/outputs/notifications/notification-2025-10-20-150240.html
- Local: `outputs/notifications/notification-2025-10-20-150240.html`

---

## 🛠️ Troubleshooting

### Email not sending?

**Check 1: Credentials configured?**
```bash
grep -E "SENDER_EMAIL|SENDER_PASSWORD" .env
```

**Check 2: App password correct?**
- Must be 16 characters (remove spaces)
- Generated from Google App Passwords, not your regular password
- 2-Factor Authentication must be enabled

**Check 3: Test connection**
```python
from utils.notification_service import notification_service
notification_service.send_notification(
    subject='Test',
    message='<h1>Test</h1>',
    recipient='${NOTIFICATION_EMAIL}'
)
```

### Gmail blocking emails?

**Less secure app access:** Google deprecated this - must use App Passwords

**2FA not enabled:** Required for App Passwords to work

**Account locked:** Check https://myaccount.google.com/security

### Notification saved as HTML instead of sent?

This means email credentials are not configured. Follow Steps 1-3 above to set up SMTP.

---

## 📁 Files Created

### Core Files:
- ✅ `utils/notification_service.py` - Notification service class
- ✅ `send_test_notification.py` - Test notification script
- ✅ `outputs/notifications/notification-2025-10-20-150240.html` - Test notification HTML
- ✅ `EMAIL_NOTIFICATIONS_SETUP.md` - This documentation

### Configuration:
- ✅ `.env` - Added `NOTIFICATION_EMAIL=${NOTIFICATION_EMAIL}`

---

## 🎯 Quick Commands

### Send Test Notification:
```bash
cd /home/avi/projects/seoanalyst/seo-analyst-agent
source venv/bin/activate
python send_test_notification.py
```

### Send System Status via CLI:
```bash
source venv/bin/activate
python -m utils.notification_service --status --to ${NOTIFICATION_EMAIL}
```

### View Latest Notification:
```bash
# Open in browser
xdg-open outputs/notifications/notification-2025-10-20-150240.html

# Or curl the web URL
curl https://seo.theprofitplatform.com.au/preview/outputs/notifications/notification-2025-10-20-150240.html
```

---

## ✅ Current Status

| Component | Status |
|-----------|--------|
| **Notification Service** | ✅ Implemented |
| **Notification Email** | ✅ Configured (${NOTIFICATION_EMAIL}) |
| **SMTP Credentials** | ⚠️ Not configured (follow steps above) |
| **Test Notification** | ✅ Created and saved as HTML |
| **HTML Preview** | ✅ Available online |

---

## 🔜 Next Steps

1. **Enable Email Sending** (Optional)
   - Follow Steps 1-3 above to configure SMTP credentials
   - Run `python send_test_notification.py` to test

2. **Automate Notifications** (Optional)
   - Add notification calls to `capture_monthly_snapshot.py`
   - Add notification calls to `web/app.py` after report generation
   - Set up cron job for daily/weekly status emails

3. **Monitor Notifications**
   - Check `outputs/notifications/` directory for saved notifications
   - View online at https://seo.theprofitplatform.com.au/preview/outputs/notifications/

---

**Created:** October 20, 2025
**Notification System:** ✅ Ready to use (add SMTP credentials to enable email sending)
**Test Notification:** ✅ Available at https://seo.theprofitplatform.com.au/preview/outputs/notifications/notification-2025-10-20-150240.html
