# Debug Guide - Frontend Display Issue

## Problem
Data is saving to CSV but not displaying on the frontend.

## How to Debug

### Step 1: Check Browser Console
1. Open your browser (Chrome/Edge/Firefox)
2. Press **F12** to open Developer Tools
3. Go to the **Console** tab
4. Refresh the page
5. Look for these messages:

**Expected output:**
```
🔄 Loading tickets from API...
✅ Loaded 100 tickets: [...]
🎨 Rendering tickets table...
📋 Rendering 100 tickets
✅ Table rendered successfully
```

**If you see errors:**
- Red error messages → API connection problem
- "0 tickets" → Backend not returning data
- "undefined" errors → Data format mismatch

### Step 2: Check Flask Server Console
Look at your terminal where Flask is running.

**Expected output when page loads:**
```
📤 API: Returning 100 tickets to frontend
   First ticket: {'ID': 'TICKET-1100', ...}
```

**When creating a ticket:**
```
📥 API: Received new ticket request: {'issue': '...', 'priority': '...'}
   Current tickets in DB: 100
   Creating ticket: TICKET-1101
✅ Ticket saved! Total tickets now: 101
```

### Step 3: Check Network Tab
1. In Developer Tools, go to **Network** tab
2. Refresh the page
3. Look for request to `/api/tickets`
4. Click on it
5. Check the **Response** tab

**Should see:**
```json
[
  {
    "ID": "TICKET-1100",
    "Issue": "...",
    "Status": "Open",
    "Priority": "High",
    "Date Submitted": "2023-06-01"
  },
  ...
]
```

### Step 4: Verify CSV File
Run the test script:
```bash
python test_save.py
```

**Expected output:**
```
✅ tickets.csv exists
📊 Number of tickets in CSV: 100
📋 Columns: ['ID', 'Issue', 'Status', 'Priority', 'Date Submitted']
```

## Common Issues & Solutions

### Issue 1: "No tickets found" message
**Cause:** API returning empty array or not being called

**Solutions:**
1. Check browser console for errors
2. Verify Flask server is running
3. Check if `tickets.csv` exists and has data
4. Try hard refresh: **Ctrl+Shift+R** (Windows) or **Cmd+Shift+R** (Mac)

### Issue 2: Loading spinner stuck
**Cause:** JavaScript error preventing table render

**Solutions:**
1. Check browser console for JavaScript errors
2. Clear browser cache
3. Try in incognito/private window

### Issue 3: Old data showing
**Cause:** Browser cache

**Solutions:**
1. Hard refresh: **Ctrl+Shift+R**
2. Clear browser cache
3. Open in incognito mode

### Issue 4: API returns data but table is empty
**Cause:** JavaScript rendering error

**Solutions:**
1. Check browser console for errors
2. Verify data format matches expected structure
3. Check if `tickets` variable is being set correctly

### Issue 5: 404 or 500 errors
**Cause:** Flask routing or server error

**Solutions:**
1. Check Flask console for error messages
2. Verify Flask is running on correct port (5000)
3. Check if `templates/index.html` exists
4. Restart Flask server

## Quick Fixes

### Fix 1: Clear Everything and Restart
```bash
# Stop Flask (Ctrl+C)
# Delete tickets.csv to start fresh
# Restart Flask
python app.py
```

### Fix 2: Force Reload Data
In browser console, type:
```javascript
loadTickets()
```

### Fix 3: Check if API is accessible
Open in browser:
```
http://localhost:5000/api/tickets
```
Should see JSON array of tickets.

## Testing Checklist

- [ ] Flask server is running (check terminal)
- [ ] No errors in Flask console
- [ ] Browser console shows no errors
- [ ] `/api/tickets` returns JSON data
- [ ] `tickets.csv` exists and has data
- [ ] Browser cache cleared
- [ ] Tried hard refresh (Ctrl+Shift+R)

## Still Not Working?

### Enable Full Debug Mode

**In `app.py`, add at the top:**
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

**In browser console, check:**
```javascript
console.log('Tickets variable:', tickets);
console.log('Table body:', document.getElementById('ticketsBody'));
```

### Manual Test
1. Open browser console
2. Run:
```javascript
fetch('/api/tickets')
  .then(r => r.json())
  .then(data => console.log('API Response:', data))
```

This will show exactly what the API is returning.

## Contact Points

If still having issues, check:
1. ✅ Flask console output
2. ✅ Browser console errors
3. ✅ Network tab in DevTools
4. ✅ CSV file contents
5. ✅ Port 5000 is not blocked by firewall
