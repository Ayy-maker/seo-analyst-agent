# 🤖 Service Account Setup Guide - Full Automation

## Complete Step-by-Step Guide for Service Account Authentication

This guide will set up **fully automated** data fetching with **zero user authorization** needed. Perfect for production environments!

---

## ⏱️ Time Required: 15-20 minutes

---

## 📋 What You'll Accomplish

By the end of this guide:
- ✅ Service account created in Google Cloud
- ✅ Service account has access to your GSC and GA4
- ✅ System automatically fetches data forever
- ✅ No OAuth, no re-authorization, no user interaction

---

## 🔧 Part 1: Create Service Account (5 minutes)

### Step 1.1: Go to Google Cloud Console

1. Visit [Google Cloud Console](https://console.cloud.google.com/)
2. Select your project (or create new: `SEO-Analyst-Automation`)

### Step 1.2: Create Service Account

1. Click **☰ Menu** → **IAM & Admin** → **Service Accounts**
2. Click **+ CREATE SERVICE ACCOUNT**

3. **Service account details**:
   - Name: `seo-analyst-automation`
   - ID: `seo-analyst-automation` (auto-filled)
   - Description: `Service account for automated SEO data fetching`
   - Click **CREATE AND CONTINUE**

4. **Grant access** (Optional, skip this):
   - Click **CONTINUE** (no roles needed here)

5. **Grant users access** (Optional, skip this):
   - Click **DONE**

### Step 1.3: Create JSON Key

1. Find your new service account in the list
2. Click on the service account email (looks like `seo-analyst-automation@project-id.iam.gserviceaccount.com`)
3. Go to **KEYS** tab
4. Click **ADD KEY** → **Create new key**
5. Select **JSON** format
6. Click **CREATE**

✅ A JSON file will download automatically - **save this securely!**

**File name**: `project-id-1234567890ab.json`

---

## 🔐 Part 2: Upload Service Account Key (2 minutes)

### Step 2.1: Rename the Key File

Rename the downloaded file to: `service_account.json`

### Step 2.2: Upload to Server

**Option A: Using SCP** (from your computer):
```bash
scp service_account.json avi@your-server:/home/avi/projects/seoanalyst/seo-analyst-agent/config/credentials/
```

**Option B: Manual Upload**:
1. Open the JSON file
2. Copy all contents
3. SSH to server:
   ```bash
   ssh avi@your-server
   cd /home/avi/projects/seoanalyst/seo-analyst-agent
   nano config/credentials/service_account.json
   # Paste contents
   # Ctrl+X, Y, Enter to save
   ```

### Step 2.3: Set Secure Permissions

```bash
cd /home/avi/projects/seoanalyst/seo-analyst-agent
chmod 600 config/credentials/service_account.json
ls -la config/credentials/service_account.json

# Should show: -rw------- 1 avi avi service_account.json
```

✅ Service account key is now installed!

---

## 📊 Part 3: Grant Access to Google Search Console (5 minutes)

**IMPORTANT**: You must add the service account email as a user in GSC.

### Step 3.1: Get Service Account Email

From the JSON file you downloaded, find the `client_email` field:

```json
{
  "type": "service_account",
  "project_id": "seo-analyst-123456",
  "private_key_id": "...",
  "private_key": "...",
  "client_email": "seo-analyst-automation@seo-analyst-123456.iam.gserviceaccount.com",
  ...
}
```

**Copy this email**: `seo-analyst-automation@seo-analyst-123456.iam.gserviceaccount.com`

### Step 3.2: Add to Google Search Console

1. Go to [Google Search Console](https://search.google.com/search-console)
2. Select your property (website)
3. Click **Settings** (⚙️) in left sidebar
4. Click **Users and permissions**
5. Click **ADD USER**

6. **Add user details**:
   - Email: `seo-analyst-automation@...` (paste service account email)
   - Permission: **Full** (required for API access)
   - Click **ADD**

7. **Verify email sent** (ignore it):
   - Google will say "Verification email sent"
   - **Service accounts don't receive emails** - this is normal!
   - The account is still added successfully

✅ Service account now has access to GSC data!

### Step 3.3: Repeat for All Properties

If you have multiple websites in GSC, repeat Step 3.2 for each one.

---

## 📈 Part 4: Grant Access to Google Analytics 4 (5 minutes)

### Step 4.1: Get Service Account Email

Same email as before: `seo-analyst-automation@...`

### Step 4.2: Add to GA4 Property

1. Go to [Google Analytics](https://analytics.google.com/)
2. Click **Admin** (⚙️) in bottom left
3. In the **Property** column, select your property
4. Click **Property Access Management**
5. Click **+** (plus icon) in top right
6. Click **Add users**

7. **Add user details**:
   - Email: `seo-analyst-automation@...` (paste service account email)
   - Roles: Check **Viewer** (minimum required)
   - Notify: Uncheck (service accounts don't receive email)
   - Click **ADD**

✅ Service account now has access to GA4 data!

### Step 4.3: Get Your Property ID

1. Still in **Admin** → **Property Settings**
2. Find **PROPERTY ID** at the top
3. **Copy this number** (e.g., `123456789`)

**Save this Property ID** - you'll need it!

---

## 🧪 Part 5: Test the Connection (3 minutes)

### Step 5.1: Test GSC Connection

```bash
cd /home/avi/projects/seoanalyst/seo-analyst-agent

python3 << 'EOF'
from integrations.gsc_api_client import GSCAPIClient

# Initialize with service account
client = GSCAPIClient(service_account_file='config/credentials/service_account.json')

# Try to connect
if client.connect():
    print("✅ GSC Service Account Connected!")
    print(f"   Auth method: {client.auth_method}")

    # List sites
    sites = client.list_sites()
    print(f"   Sites found: {len(sites)}")
    for site in sites:
        print(f"      - {site}")

    # Test data fetch (first site)
    if sites:
        summary = client.get_site_summary(sites[0], days=7)
        print(f"\n📊 Last 7 days data:")
        print(f"   Clicks: {summary['total_clicks']}")
        print(f"   Impressions: {summary['total_impressions']}")
        print(f"   Queries: {summary['total_queries']}")
else:
    print("❌ Failed to connect to GSC")
    print("   Check:")
    print("   1. service_account.json file exists")
    print("   2. Service account added to GSC")
    print("   3. Permissions set to 'Full'")
EOF
```

**Expected Output**:
```
✅ GSC Service Account Connected!
   Auth method: service_account
   Sites found: 1
      - https://yoursite.com/

📊 Last 7 days data:
   Clicks: 1,234
   Impressions: 45,678
   Queries: 245
```

### Step 5.2: Test GA4 Connection

```bash
python3 << 'EOF'
from integrations.ga4_api_client import GA4APIClient

# Initialize with service account and property ID
client = GA4APIClient(
    service_account_file='config/credentials/service_account.json',
    property_id='YOUR_PROPERTY_ID'  # Replace with your Property ID
)

# Try to connect
if client.connect():
    print("✅ GA4 Service Account Connected!")
    print(f"   Auth method: {client.auth_method}")
    print(f"   Property: {client.property_id}")

    # Test data fetch
    summary = client.get_summary_metrics(days=7)
    print(f"\n📊 Last 7 days data:")
    print(f"   Users: {summary['total_users']:,}")
    print(f"   Sessions: {summary['total_sessions']:,}")
    print(f"   Page Views: {summary['total_page_views']:,}")
    print(f"   Engagement: {summary['avg_engagement_rate']}%")
else:
    print("❌ Failed to connect to GA4")
    print("   Check:")
    print("   1. service_account.json file exists")
    print("   2. Service account added to GA4")
    print("   3. Property ID is correct")
    print("   4. Service account has 'Viewer' role")
EOF
```

**Expected Output**:
```
✅ GA4 Service Account Connected!
   Auth method: service_account
   Property: properties/123456789

📊 Last 7 days data:
   Users: 10,354
   Sessions: 13,651
   Page Views: 48,900
   Engagement: 79.1%
```

---

## ✅ Part 6: Verify Full Setup (2 minutes)

### Quick Checklist

Run this verification script:

```bash
cd /home/avi/projects/seoanalyst/seo-analyst-agent

python3 << 'EOF'
from pathlib import Path
from integrations.gsc_api_client import GSCAPIClient
from integrations.ga4_api_client import GA4APIClient

print("🔍 Verifying Service Account Setup\n")
print("=" * 60)

# Check file exists
sa_path = Path('config/credentials/service_account.json')
if sa_path.exists():
    print("✅ Service account file: Found")

    # Check permissions
    import stat
    mode = oct(sa_path.stat().st_mode)[-3:]
    if mode == '600':
        print("✅ File permissions: Secure (600)")
    else:
        print(f"⚠️  File permissions: {mode} (should be 600)")
else:
    print("❌ Service account file: NOT FOUND")
    print("   Path: config/credentials/service_account.json")

print()

# Test GSC
gsc = GSCAPIClient()
if gsc.connect() and gsc.auth_method == 'service_account':
    print("✅ GSC connection: Working (service account)")
    sites = gsc.list_sites()
    print(f"   Sites accessible: {len(sites)}")
else:
    print("❌ GSC connection: Failed")

print()

# Test GA4
ga4 = GA4APIClient()
if ga4.connect() and ga4.auth_method == 'service_account':
    print("✅ GA4 connection: Working (service account)")
    print(f"   Property ID: {ga4.property_id}")
else:
    print("❌ GA4 connection: Failed or no Property ID set")

print()
print("=" * 60)
print("Setup verification complete!")
EOF
```

**Perfect Output**:
```
🔍 Verifying Service Account Setup

============================================================
✅ Service account file: Found
✅ File permissions: Secure (600)

✅ GSC connection: Working (service account)
   Sites accessible: 1

✅ GA4 connection: Working (service account)
   Property ID: properties/123456789

============================================================
Setup verification complete!
```

---

## 🎉 Success! What You Achieved

If all tests pass:

✅ **Service account created and configured**
✅ **GSC access granted** - can fetch search data automatically
✅ **GA4 access granted** - can fetch user behavior automatically
✅ **Credentials stored securely** on server
✅ **System will now auto-fetch data** whenever you upload SEMrush

---

## 🚀 What Happens Now (Automation in Action)

### Your New Workflow

```
Step 1: Upload SEMrush CSV
   ↓
Step 2: Click "Generate Report"
   ↓
Step 3: System automatically:
   ✅ Parses SEMrush data
   ✅ Fetches GSC data (via service account) ← AUTOMATIC!
   ✅ Fetches GA4 data (via service account) ← AUTOMATIC!
   ✅ Merges all 3 data sources
   ✅ Generates comprehensive report
   ↓
Step 4: Download report (ready in 30-60 seconds)
```

**Time saved**: 15-20 minutes per report (no manual GSC/GA4 exports!)

---

## 🔒 Security Notes

### Service Account Best Practices

1. **File Permissions**: Always `600` (owner read/write only)
   ```bash
   chmod 600 config/credentials/service_account.json
   ```

2. **Never Commit to Git**: Already added to `.gitignore`

3. **Backup Securely**:
   ```bash
   # Backup to secure location
   cp config/credentials/service_account.json /secure/backup/location/
   ```

4. **Rotate Keys Annually**:
   - Create new key in Google Cloud
   - Replace old `service_account.json`
   - Delete old key from Google Cloud

5. **Monitor Usage**:
   - Check Google Cloud Console → IAM & Admin → Service Accounts
   - Review activity logs periodically

---

## 🐛 Troubleshooting

### Problem: "Service account file not found"

**Solution**:
```bash
cd /home/avi/projects/seoanalyst/seo-analyst-agent
ls -la config/credentials/service_account.json

# If missing, re-upload the file
```

### Problem: "Permission denied" when accessing GSC

**Solution**:
1. Verify service account email added to GSC
2. Check permission level is "Full"
3. Wait 5-10 minutes for changes to propagate
4. Try again

### Problem: "Property not found" in GA4

**Solutions**:
1. **Check Property ID**:
   ```bash
   # Edit ga4_config.json
   nano config/credentials/ga4_config.json
   # Should contain: {"property_id": "properties/123456789"}
   ```

2. **Verify Service Account Has Access**:
   - GA4 → Admin → Property Access Management
   - Service account should be listed

3. **Re-add Service Account**:
   - Remove and re-add with "Viewer" role

### Problem: "Invalid grant" error

**Solution**:
- Service account key may be corrupted
- Re-download key from Google Cloud
- Replace `service_account.json` file

---

## 📞 Next Steps

### Immediate Actions

1. **Test End-to-End**:
   - Upload a SEMrush CSV via web interface
   - Verify system auto-fetches GSC + GA4 data
   - Review generated report

2. **Set Up GA4 Property ID** (if not done):
   ```bash
   python3 -c "
   from integrations.ga4_api_client import ga4_api_client
   ga4_api_client.set_property_id('YOUR_PROPERTY_ID')
   print('✅ Property ID saved!')
   "
   ```

3. **Deploy to Production**:
   - System is ready for automated reporting
   - Service account authentication works indefinitely
   - No user authorization needed ever

### Optional Enhancements

1. **Add Multiple Properties**:
   - Support multiple GA4 properties
   - Auto-detect which property to use per domain

2. **Scheduled Reports**:
   - Set up cron jobs for automated weekly reports
   - Email reports automatically

3. **Monitoring**:
   - Set up alerts for API failures
   - Track API quota usage

---

## 🎯 Summary

**What You Completed**:
- ✅ Service account created (Google Cloud)
- ✅ Service account key downloaded and secured
- ✅ Access granted in GSC (Full permissions)
- ✅ Access granted in GA4 (Viewer role)
- ✅ Credentials uploaded and tested
- ✅ Full automation verified

**Time Investment**: 15-20 minutes one-time setup
**Time Saved**: 15-20 minutes per report forever
**ROI**: Immediate on first automated report

**Your system now has fully automated data fetching with ZERO manual work!** 🎉

---

## 📧 Support

If you encounter issues:
1. Check troubleshooting section above
2. Verify all steps completed
3. Review Google Cloud logs
4. Check application logs: `docker logs seo-analyst`

**Service account is now the foundation of your automation!**
