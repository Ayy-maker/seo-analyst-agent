# 🚀 Quick Test - 2 Minutes

Want to make sure everything works? Follow this quick test!

## ✅ Pre-Test Checklist

1. **Server Running?**
   ```bash
   # Check if server is up
   curl http://localhost:5001
   ```
   
   If not running, start it:
   ```bash
   bash START_SERVER.sh
   ```

## 📝 Test Single Upload

1. **Open Browser**
   ```
   http://localhost:5001
   ```

2. **Click "📄 Single Upload" tab**

3. **Select a Test File**
   - Click the upload area
   - Choose any CSV, XLSX, or PDF file
   - Or use the sample: `data/samples/search-console-keywords.csv`

4. **Add More Files (Optional)**
   - Click "+ Add More Files" button
   - Select another file
   - See both files in the list!

5. **Fill Form**
   - Company Name: "Test Company"
   - Report Period: "November 2024"

6. **Generate Report**
   - Click "Generate Premium Report"
   - Wait 2-3 seconds

7. **Verify Success** ✅
   - You should see report preview page
   - Click "👁️ Preview Report" - opens in new tab
   - Click "📥 Download HTML Report" - saves file

## 📁 Test Batch Upload

1. **Click "📁 Batch Upload" tab**

2. **Select Multiple Files**
   - Click upload area
   - Select 2-3 files
   - See brand names auto-detected

3. **Add More (Optional)**
   - Click "+ Add More Files"
   - Select more files

4. **Fill Form**
   - Report Period: "November 2024"

5. **Generate Reports**
   - Click "Generate Reports for All Brands"
   - Wait for batch processing

6. **Verify Success** ✅
   - Multiple reports generated
   - Each has preview & download buttons

## 🎯 Expected Results

### Single Upload Success:
- ✅ Files uploaded without errors
- ✅ Report generated in 2-3 seconds
- ✅ Preview opens in new tab showing beautiful HTML report
- ✅ Download triggers browser save dialog
- ✅ HTML file is 40KB and complete

### Batch Upload Success:
- ✅ Multiple files processed
- ✅ Brands auto-detected from filenames
- ✅ Separate reports for each brand
- ✅ All previews work
- ✅ All downloads work

## 🐛 If Something Goes Wrong

### "No files uploaded" error
```bash
# Refresh the page and try again
# Make sure files are selected before clicking Generate
```

### Preview shows error
```bash
# Check if file exists
ls outputs/html-reports/

# Restart server
bash START_SERVER.sh
```

### Download doesn't work
```bash
# Try preview first (opens in new tab)
# Then use browser's "Save As" to download
```

## 🎨 What You Should See

### In Preview:
- Beautiful purple gradient header
- 4 interactive Chart.js graphs
- Animated KPI counters
- Month-over-month growth charts
- Top keywords and landing pages
- Device distribution
- Strategic recommendations

### HTML File Features:
- Single file (40KB)
- Works offline
- Mobile responsive
- Professional design
- Interactive elements
- Print-friendly

## ✅ Test Complete!

If you saw:
- ✅ Files upload successfully
- ✅ Reports generate
- ✅ Preview opens with beautiful charts
- ✅ Download works with popup

**Everything is working perfectly!** 🎉

## 🆘 Need Help?

Check these files:
- **README.md** - Complete documentation
- **QUICKSTART.md** - 2-minute setup guide
- **SETUP_COMPLETE.md** - Post-install guide

Or check server logs:
```bash
tail -f /tmp/seo_server.log
```

---

Made with ❤️ by SEO Analyst Agent
