# 🤖 SEO Automation Setup Guide

## Complete Guide to Setting Up Automated Data Fetching

This guide will help you set up **fully automated** SEO reporting where you only need to upload SEMrush data and the system automatically fetches Google Search Console and Google Analytics 4 data.

---

## 📋 Prerequisites

- Google Account with access to:
  - Google Search Console (for your website)
  - Google Analytics 4 (for your website)
- Google Cloud Platform account (free tier is sufficient)
- Admin access to this SEO Analyst application

---

## 🔧 Step 1: Google Cloud Platform Setup (15 minutes)

### 1.1 Create a Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Click "Select a Project" →  "New Project"
3. Enter project name: `SEO-Analyst-Automation`
4. Click "Create"

### 1.2 Enable Required APIs

**Enable Google Search Console API**:
1. In Google Cloud Console, go to "APIs & Services" → "Library"
2. Search for "Google Search Console API"
3. Click on it → Click "Enable"

**Enable Google Analytics Data API**:
1. In "APIs & Services" → "Library"
2. Search for "Google Analytics Data API"
3. Click on it → Click "Enable"

### 1.3 Create OAuth 2.0 Credentials

1. Go to "APIs & Services" → "Credentials"
2. Click "Create Credentials" → "OAuth client ID"
3. If prompted, configure OAuth consent screen:
   - User Type: **External**
   - App name: `SEO Analyst Automation`
   - User support email: `your-email@example.com`
   - Developer contact: `your-email@example.com`
   - Click "Save and Continue"
   - Scopes: Skip this step → Click "Save and Continue"
   - Test users: Add your Google account email → Click "Save and Continue"
   - Click "Back to Dashboard"

4. Now create OAuth client ID:
   - Application type: **Web application**
   - Name: `SEO Analyst Web App`
   - Authorized redirect URIs: Add these two:
     ```
     http://localhost:5001/oauth2callback
     https://seo.theprofitplatform.com.au/oauth2callback
     ```
   - Click "Create"

5. **Download credentials**:
   - You'll see a dialog with Client ID and Client Secret
   - Click "Download JSON"
   - Save as `client_secrets.json`
   - **Keep this file secure!**

---

## 📂 Step 2: Install Credentials (5 minutes)

### 2.1 Upload client_secrets.json

**On the server**:
```bash
# Create credentials directory
mkdir -p /home/avi/projects/seoanalyst/seo-analyst-agent/config/credentials

# Upload your client_secrets.json to this directory
# You can use SCP, FTP, or copy-paste
scp client_secrets.json avi@server:/home/avi/projects/seoanalyst/seo-analyst-agent/config/credentials/

# Set proper permissions
chmod 600 /home/avi/projects/seoanalyst/seo-analyst-agent/config/credentials/client_secrets.json
```

### 2.2 Verify Installation

```bash
cd /home/avi/projects/seoanalyst/seo-analyst-agent
ls -la config/credentials/

# Should show:
# -rw------- 1 avi avi client_secrets.json
```

---

## 🔐 Step 3: Authorize Applications (10 minutes)

### 3.1 Authorize Google Search Console

**Option A: Via Web Interface** (Recommended):
1. Go to: https://seo.theprofitplatform.com.au/settings
2. Click "Connect Google Search Console"
3. You'll be redirected to Google OAuth
4. Sign in with your Google account
5. Grant permissions to access Search Console
6. You'll be redirected back to the app
7. Status should show: ✅ Connected

**Option B: Via CLI** (for testing):
```bash
cd /home/avi/projects/seoanalyst/seo-analyst-agent

# Run authorization script
python3 -c "
from integrations.gsc_api_client import gsc_api_client
import os

# Get authorization URL
auth_url = gsc_api_client.get_authorization_url('config/credentials/client_secrets.json')
print(f'Visit this URL to authorize: {auth_url}')
"

# Visit the URL in your browser
# After authorization, you'll get a code
# Paste it here:
# code = 'YOUR_AUTHORIZATION_CODE'
```

### 3.2 Authorize Google Analytics 4

**Via Web Interface**:
1. Go to: https://seo.theprofitplatform.com.au/settings
2. Click "Connect Google Analytics 4"
3. Sign in and grant permissions
4. Enter your GA4 Property ID:
   - Go to [GA4 Admin](https://analytics.google.com/analytics/web/)
   - Select your property
   - Go to Admin → Property Settings
   - Copy "Property ID" (looks like: `123456789`)
5. Paste Property ID in the app
6. Click "Save"
7. Status should show: ✅ Connected

---

## 🚀 Step 4: Test Automation (5 minutes)

### 4.1 Test GSC Connection

```bash
cd /home/avi/projects/seoanalyst/seo-analyst-agent

# Test script
python3 -c "
from integrations.gsc_api_client import gsc_api_client

# Check authentication
if gsc_api_client.is_authenticated():
    print('✅ GSC authenticated!')

    # List available sites
    sites = gsc_api_client.list_sites()
    print(f'Sites you have access to: {sites}')

    # Fetch data for first site
    if sites:
        summary = gsc_api_client.get_site_summary(sites[0], days=7)
        print(f'Last 7 days clicks: {summary[\"total_clicks\"]}')
else:
    print('❌ Not authenticated. Please authorize first.')
"
```

### 4.2 Test GA4 Connection

```bash
python3 -c "
from integrations.ga4_api_client import ga4_api_client

# Set your property ID
ga4_api_client.set_property_id('YOUR_PROPERTY_ID')

# Check authentication
if ga4_api_client.is_authenticated():
    print('✅ GA4 authenticated!')

    # Fetch summary metrics
    summary = ga4_api_client.get_summary_metrics(days=7)
    print(f'Last 7 days users: {summary[\"total_users\"]}')
    print(f'Sessions: {summary[\"total_sessions\"]}')
else:
    print('❌ Not authenticated. Please authorize first.')
"
```

---

## ✅ Step 5: Verify Full Automation (5 minutes)

### 5.1 Upload SEMrush Data (Test)

1. Go to: https://seo.theprofitplatform.com.au
2. Upload a SEMrush CSV export
3. Enter company name
4. Click "Generate Automated Report"

**What Should Happen**:
```
🔄 Processing your request...

[████████░░] 40% Parsing SEMrush data...
  ✅ Found domain: example.com

[████████████] 60% Fetching Google Search Console data...
  ✅ Retrieved 1,363 clicks from 245 queries

[████████████████] 80% Fetching Google Analytics 4 data...
  ✅ Retrieved 10,354 users, 13,651 sessions

[████████████████████] 100% Generating comprehensive report...
  ✅ Report ready!

✨ Complete report generated in 45 seconds
```

### 5.2 Verify Report Contents

The generated report should have:
- ✅ **SEMrush Data**: Keyword rankings, competitors
- ✅ **GSC Data**: Real clicks, impressions, CTR (auto-fetched!)
- ✅ **GA4 Data**: Real users, sessions, engagement (auto-fetched!)
- ✅ **Cross-Referenced**: SEMrush positions vs GSC actuals
- ✅ **AI Insights**: Automated recommendations

---

## 🔒 Security Best Practices

### Protect Your Credentials

**1. File Permissions**:
```bash
# Credentials should only be readable by app user
chmod 600 config/credentials/client_secrets.json
chmod 600 config/credentials/gsc_token.json
chmod 600 config/credentials/ga4_token.json
```

**2. Gitignore**:
```bash
# Add to .gitignore
echo "config/credentials/*.json" >> .gitignore
echo "config/credentials/gsc_token.json" >> .gitignore
echo "config/credentials/ga4_token.json" >> .gitignore
```

**3. Environment Variables** (Optional):
```bash
# Instead of file, use environment variable
export GOOGLE_APPLICATION_CREDENTIALS="/path/to/credentials.json"
```

**4. Backup Credentials**:
```bash
# Backup to secure location
cp -r config/credentials /secure/backup/location/
```

---

## 🔄 Refresh Tokens

### What Are Refresh Tokens?

OAuth tokens expire after a certain period. Refresh tokens allow the app to get new access tokens without user re-authorization.

**How It Works**:
- Access token: Valid for 1 hour
- Refresh token: Valid for 6 months (or until revoked)
- App automatically refreshes access tokens using refresh token
- User only needs to authorize once every 6 months

### Manual Refresh (if needed)

If tokens expire or become invalid:

```bash
# Re-authorize GSC
python3 -c "
from integrations.gsc_api_client import gsc_api_client
gsc_api_client.disconnect()  # Clear old tokens
"

# Then re-authorize via web interface
```

---

## 🐛 Troubleshooting

### Problem: "Not authenticated" error

**Solution**:
1. Check if token files exist:
   ```bash
   ls -la config/credentials/
   ```
2. If missing, re-authorize via web interface
3. Check file permissions (should be `600`)

### Problem: "Invalid grant" error

**Solution**:
1. Tokens expired → Re-authorize
2. Or: User revoked access → Re-authorize

### Problem: "Access denied" error

**Solution**:
1. Check OAuth consent screen configuration
2. Add your email to "Test users"
3. Re-authorize

### Problem: "Property not found" error (GA4)

**Solution**:
1. Verify Property ID is correct
2. Ensure your Google account has access to that property
3. Re-check Property ID in GA4 Admin

### Problem: "Site not found" error (GSC)

**Solution**:
1. Verify site URL format: `https://example.com/` or `sc-domain:example.com`
2. Ensure your Google account is a verified owner in GSC
3. Check site list: `gsc_api_client.list_sites()`

---

## 📊 Usage After Setup

Once automation is set up, your workflow becomes:

### Simple Workflow
```
1. Upload SEMrush CSV
2. Click "Generate Report"
3. Wait 30-60 seconds
4. Download comprehensive report
```

**That's it!** No manual GSC/GA4 exports needed.

### Advanced: Scheduled Reports

Set up recurring reports:
```
Settings → Scheduled Reports
- Frequency: Weekly
- Day: Monday
- Time: 9:00 AM
- Email to: your@email.com

Save → Done!
```

Every Monday at 9 AM:
- System auto-fetches GSC data
- System auto-fetches GA4 data
- Generates report
- Emails PDF to you

**Zero manual work!** 🎉

---

## 🔐 Credential Files Reference

After setup, you should have these files:

```
config/credentials/
├── client_secrets.json       # OAuth client credentials (from Google Cloud)
├── gsc_token.json           # GSC access/refresh tokens (auto-generated)
├── ga4_token.json           # GA4 access/refresh tokens (auto-generated)
└── ga4_config.json          # GA4 property ID (auto-generated)
```

**Never commit these files to git!**

---

## 📞 Support

If you encounter issues:

1. Check troubleshooting section above
2. Verify all prerequisites are met
3. Review Google Cloud Console for API errors
4. Check application logs: `docker logs seo-analyst`

---

## 🎉 Success Checklist

- ✅ Google Cloud project created
- ✅ GSC API enabled
- ✅ GA4 API enabled
- ✅ OAuth credentials created and downloaded
- ✅ client_secrets.json uploaded to server
- ✅ GSC authorized via web interface
- ✅ GA4 authorized and Property ID set
- ✅ Test data fetch successful (GSC + GA4)
- ✅ Full automation test passed
- ✅ Credentials backed up securely

**You're all set for fully automated SEO reporting!** 🚀
