# 🔐 Google API Credentials Explained

## Important: Two Types of Credentials Needed

You've provided **API Keys**, which is great! However, for Google Search Console and Google Analytics 4, we need **TWO types of credentials**:

---

## 📋 What You Provided (API Keys)

✅ **Google Analytics API Key**: `AIzaSyCSIwK_YVE6yBzZy7-r2dNC1LyfA6eVfmY`
✅ **Google Search Console API Key**: `AIzaSyBaEI319a5_NwxGnhjHp5K8piQSpw6rK40`

**What API Keys Do**:
- Identify your application to Google
- Track API usage and quotas
- Required for billing/monitoring
- Used in API requests as `key=AIzaSy...`

**What API Keys DON'T Do**:
- ❌ Cannot access user-specific data
- ❌ Cannot fetch your GSC search queries
- ❌ Cannot fetch your GA4 user metrics
- ❌ Not sufficient for authentication

---

## 🔑 What We Still Need (OAuth 2.0)

For **automated data fetching**, we need **OAuth 2.0 credentials** because:

1. **Google Search Console API** - Requires OAuth to access YOUR search data
2. **Google Analytics 4 Data API** - Requires OAuth to access YOUR analytics data

### Why OAuth is Required

These services contain **private user data**:
- Your website's search performance
- Your website's user behavior
- Competitor-sensitive metrics
- Business-critical analytics

Google requires **explicit user authorization** via OAuth 2.0 to access this data.

---

## 🎯 Complete Setup: What's Needed

### Current Status

| Credential Type | Status | Purpose |
|----------------|--------|---------|
| **API Keys** | ✅ **Provided** | Identify app, track usage |
| **OAuth 2.0** | ❌ **Still needed** | Access user data |

### How to Get OAuth 2.0 Credentials

**Step 1: Create OAuth Client** (5 minutes)

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Select your project (or create one)
3. Go to "APIs & Services" → "Credentials"
4. Click "Create Credentials" → "OAuth client ID"
5. Configure OAuth consent screen:
   - User type: **External**
   - App name: `SEO Analyst`
   - Add your email
6. Create OAuth client ID:
   - Application type: **Web application**
   - Authorized redirect URIs:
     ```
     https://seo.theprofitplatform.com.au/oauth2callback
     http://localhost:5001/oauth2callback
     ```
7. Download JSON file → Save as `client_secrets.json`

**Step 2: Upload to Server**

```bash
# Upload client_secrets.json to server
scp client_secrets.json avi@server:/home/avi/projects/seoanalyst/seo-analyst-agent/config/credentials/
```

---

## 🔄 How It Works Together

### Combined Flow

```
┌─────────────────────────────────────────────────────────┐
│  User authorizes app (OAuth 2.0)                        │
│  └─ One-time authorization                              │
│  └─ Grants access to GSC and GA4 data                   │
└─────────────────┬───────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────────┐
│  App stores OAuth tokens (automatic refresh)            │
└─────────────────┬───────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────────┐
│  API Requests include:                                  │
│  1. API Key (identifies app)                            │
│  2. OAuth Token (proves user authorization)             │
└─────────────────────────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────────┐
│  Google validates both → Returns data                   │
└─────────────────────────────────────────────────────────┘
```

### Example API Request

```python
# GSC API request with BOTH credentials
response = service.searchanalytics().query(
    siteUrl='https://yoursite.com',
    body=request_body,
    # OAuth token used here (automatically by client library)
    # API key used here: key='AIzaSyBaEI319a5_NwxGnhjHp5K8piQSpw6rK40'
).execute()
```

---

## ⚡ Quick Alternative: Service Account (Advanced)

If you want to skip OAuth authorization, you can use a **Service Account**:

### Service Account Setup

**Pros**:
- ✅ No user authorization needed
- ✅ Works automatically
- ✅ Good for server-to-server

**Cons**:
- ❌ More complex setup
- ❌ Need to grant service account access to GSC & GA4
- ❌ Requires domain verification

**How to Set Up**:

1. **Create Service Account**:
   ```
   Google Cloud Console → IAM & Admin → Service Accounts
   → Create Service Account
   → Download JSON key file
   ```

2. **Grant Access to GSC**:
   ```
   Google Search Console → Settings → Users and permissions
   → Add user → Use service account email
   → Grant "Full" permissions
   ```

3. **Grant Access to GA4**:
   ```
   Google Analytics → Admin → Property Access Management
   → Add user → Use service account email
   → Grant "Viewer" role
   ```

4. **Update Code**:
   ```python
   from google.oauth2 import service_account

   credentials = service_account.Credentials.from_service_account_file(
       'config/credentials/service_account.json',
       scopes=['https://www.googleapis.com/auth/webmasters.readonly']
   )
   ```

**This is more advanced but eliminates the OAuth flow!**

---

## 🎯 Recommended Path Forward

### Option 1: OAuth 2.0 (Easier, Recommended)
```
1. Create OAuth client ID (5 min)
2. Download client_secrets.json
3. Upload to server
4. Authorize via web interface (1 click)
5. Done! Tokens auto-refresh for 6 months
```

**Best for**:
- Single user/admin access
- Quick setup
- Personal use

### Option 2: Service Account (Advanced)
```
1. Create service account (5 min)
2. Download key file
3. Grant access in GSC & GA4 (10 min)
4. Update code to use service account
5. Done! Works indefinitely, no re-auth
```

**Best for**:
- Multiple sites/properties
- Production automation
- No user intervention needed

---

## 💾 Current Credentials Stored

**Location**: `config/credentials/api_keys.json`

**Contents**:
```json
{
  "google_analytics": {
    "api_key": "AIzaSyCSIwK_YVE6yBzZy7-r2dNC1LyfA6eVfmY"
  },
  "google_search_console": {
    "api_key": "AIzaSyBaEI319a5_NwxGnhjHp5K8piQSpw6rK40"
  }
}
```

**Status**: ✅ Saved securely (not in git)

---

## 🚀 Next Steps

### To Enable Full Automation:

**Choose your path**:

**A) OAuth Path** (Recommended for you):
1. Create OAuth client ID in Google Cloud
2. Download `client_secrets.json`
3. Upload to server: `/config/credentials/client_secrets.json`
4. I'll integrate it into the web interface
5. You'll click "Connect" buttons once
6. System auto-fetches data forever (with auto-refresh)

**B) Service Account Path** (Advanced):
1. Create service account in Google Cloud
2. Download service account JSON key
3. Grant access in GSC and GA4
4. I'll update code to use service account
5. System works automatically, no user auth needed

**Which path do you prefer?**
- OAuth = Easier, 1-click setup
- Service Account = More powerful, fully automated

Let me know and I'll proceed accordingly!

---

## 🔒 Security Notes

✅ **API keys stored securely**: `config/credentials/api_keys.json`
✅ **Not committed to git**: Added to `.gitignore`
✅ **File permissions**: `600` (owner read/write only)
⚠️ **Never share these keys publicly**

Your API keys are safe and ready to use once OAuth is configured!
