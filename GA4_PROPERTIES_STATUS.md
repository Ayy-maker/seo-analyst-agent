# GA4 Properties Configuration Status

**Last Updated**: October 20, 2025
**Total Properties**: 6
**Working**: 2/6 (33%)
**Need Access**: 4/6 (67%)

---

## 📊 All GA4 Properties

### ✅ Working Properties (2)

#### 1. Property 500340846 ✅
- **Status**: Active and fetching data
- **Last 7 days**:
  - Users: 1,448
  - Sessions: 1,494
  - Page Views: 1,976
  - Engagement: 20.8%
- **Action**: None needed - working perfectly!

#### 2. Property 499372671 ✅
- **Status**: Active and fetching data
- **Last 7 days**:
  - Users: 17
  - Sessions: 23
  - Page Views: 35
  - Engagement: 66.2%
- **Action**: None needed - working perfectly!

---

### ❌ Need Service Account Access (4)

These properties need the service account added in Google Analytics:

#### 3. Property 354069162 ❌
- **Status**: Permission denied
- **Action Required**: Add service account to GA4

#### 4. Property 364509088 ❌
- **Status**: Permission denied
- **Action Required**: Add service account to GA4

#### 5. Property 361477303 ❌
- **Status**: Permission denied
- **Action Required**: Add service account to GA4

#### 6. Property 363690330 ❌
- **Status**: Permission denied
- **Action Required**: Add service account to GA4

---

## 🔧 How to Fix the 4 Properties

You need to add the service account to each property in Google Analytics. Here's how:

### Service Account Email (Copy This)
```
seo-analyst-automation@robotic-goal-456009-r2.iam.gserviceaccount.com
```

### Steps to Add Access (Repeat for Each Property)

1. **Go to [Google Analytics](https://analytics.google.com/)**

2. **Select the property** from the dropdown
   - Property 354069162, or
   - Property 364509088, or
   - Property 361477303, or
   - Property 363690330

3. **Click Admin** ⚙️ (bottom left)

4. In the **Property** column, click **"Property access management"**

5. **Click the "+" button** (top right)

6. **Click "Add users"**

7. **Enter service account details**:
   - Email: `seo-analyst-automation@robotic-goal-456009-r2.iam.gserviceaccount.com`
   - Role: **Viewer** (check the box)
   - Notify user: **Uncheck** (service accounts don't receive email)

8. **Click "Add"**

9. Wait 2-5 minutes for changes to take effect

10. **Test the connection** (see below)

---

## 🧪 Test After Adding Access

After adding the service account to a property, test it:

```bash
cd /home/avi/projects/seoanalyst/seo-analyst-agent
source venv/bin/activate

# Replace PROPERTY_ID with the actual property ID
python3 << 'EOF'
from integrations.ga4_api_client import GA4APIClient

property_id = 'PROPERTY_ID'  # e.g., '354069162'
client = GA4APIClient(property_id=property_id)

if client.connect():
    try:
        summary = client.get_summary_metrics(days=7)
        print(f"✅ Property {property_id} is now working!")
        print(f"   Users (7 days): {summary['total_users']:,}")
        print(f"   Sessions: {summary['total_sessions']:,}")
    except Exception as e:
        if '403' in str(e):
            print(f"❌ Still no access - wait 5 minutes and try again")
        else:
            print(f"⚠️  Error: {str(e)[:100]}")
else:
    print(f"❌ Connection failed")
EOF
```

---

## 📋 Quick Test All Properties

Test all 6 properties at once:

```bash
cd /home/avi/projects/seoanalyst/seo-analyst-agent
source venv/bin/activate

python3 << 'EOF'
from integrations.ga4_api_client import GA4APIClient

properties = [
    '500340846',
    '499372671',
    '354069162',
    '364509088',
    '361477303',
    '363690330'
]

print("Testing all GA4 properties:\n")
working = 0
denied = 0

for prop_id in properties:
    client = GA4APIClient(property_id=prop_id)
    if client.connect():
        try:
            summary = client.get_summary_metrics(days=7)
            users = summary['total_users']
            print(f"✅ {prop_id}: Working ({users:,} users)")
            working += 1
        except Exception as e:
            if '403' in str(e):
                print(f"❌ {prop_id}: Permission denied")
                denied += 1
            else:
                print(f"⚠️  {prop_id}: Error")
    else:
        print(f"❌ {prop_id}: Connection failed")

print(f"\nSummary: {working}/6 working, {denied}/6 need access")
EOF
```

---

## 💡 Tips

### Batch Add Service Account
To save time, you can add the service account to all 4 properties at once:

1. Open 4 browser tabs
2. Go to Google Analytics in each tab
3. Select a different property in each tab
4. Follow steps 3-8 above in parallel across all tabs
5. Takes ~5 minutes total instead of 20 minutes sequentially

### Verify Correct Property
Before adding access, verify you're in the right property:
- Check **Admin** → **Property Settings**
- Confirm the **Property ID** matches (354069162, 364509088, etc.)

### Common Issues

**Q: "User already exists" error?**
A: The service account is already added! Test the connection - it might just need 5 minutes to propagate.

**Q: Can't find "Property access management"?**
A: Make sure you're in the **Property** column (middle), not Account (left) or View (right).

**Q: Test still fails after adding?**
A: Wait 5-10 minutes. Google can take time to propagate permissions.

---

## 🎯 Next Steps

1. **Add service account** to the 4 properties (takes ~5-10 minutes total)
2. **Wait 5 minutes** for permissions to propagate
3. **Run the test script** above to verify all 6 are working
4. **Start using** all properties in your automated reports!

---

## 📞 Support

If you need help with a specific property, let me know the Property ID and I'll help troubleshoot!
