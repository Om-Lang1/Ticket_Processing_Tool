# Troubleshooting Guide

## Issue: Tickets Not Saving After Submit

### Problem
When clicking "Submit Ticket", the ticket appears briefly but disappears after page refresh or when the server restarts.

### Root Cause
The Flask app wasn't properly reloading the CSV file on each request, causing data inconsistency between the in-memory dataframe and the persisted CSV file.

### Solution Implemented

#### 1. **Created `load_tickets()` function**
- Loads tickets from CSV file on every API request
- Ensures data types are consistent (all strings)
- Handles missing CSV file by initializing new data

#### 2. **Modified all API endpoints to reload data**
- `GET /api/tickets` - Reloads before returning tickets
- `POST /api/tickets` - Reloads before adding new ticket
- `PUT /api/tickets/<id>` - Reloads before updating
- `POST /api/tickets/delete` - Reloads before deleting
- `GET /api/statistics` - Reloads before calculating stats

#### 3. **Enhanced `save_tickets()` function**
- Properly references global dataframe
- Saves to CSV immediately after any modification

### How to Verify It's Working

1. **Start the Flask app:**
   ```bash
   python app.py
   ```

2. **Check if tickets.csv is created:**
   ```bash
   python test_save.py
   ```

3. **Test ticket creation:**
   - Open http://localhost:5000
   - Submit a new ticket
   - Refresh the page - ticket should still be there
   - Stop and restart the server
   - Ticket should still be there

4. **Check the CSV file directly:**
   - Open `tickets.csv` in a text editor or Excel
   - You should see all tickets including newly created ones

### Data Persistence Flow

```
User submits ticket
    ↓
Frontend sends POST to /api/tickets
    ↓
Backend loads latest data from tickets.csv
    ↓
Backend adds new ticket to dataframe
    ↓
Backend saves dataframe to tickets.csv
    ↓
Backend returns success response
    ↓
Frontend reloads tickets from server
```

### Key Files
- **`app.py`** - Flask backend with proper save/load logic
- **`tickets.csv`** - Persistent storage (auto-generated)
- **`test_save.py`** - Test script to verify data persistence

### Common Issues

#### Issue: "tickets.csv not found"
**Solution:** The file is created automatically on first run. Just start the app.

#### Issue: "Tickets disappear after server restart"
**Solution:** Make sure the Flask app is running from the correct directory where `tickets.csv` is located.

#### Issue: "Old tickets showing instead of new ones"
**Solution:** Clear browser cache or do a hard refresh (Ctrl+F5 on Windows, Cmd+Shift+R on Mac).

#### Issue: "Can't write to tickets.csv"
**Solution:** Check file permissions. The app needs write access to the directory.

### Testing Checklist

- [ ] Create a new ticket - appears in table
- [ ] Refresh page - ticket still there
- [ ] Edit ticket status - change persists
- [ ] Delete ticket - removal persists
- [ ] Stop server, restart - all changes preserved
- [ ] Check tickets.csv file - contains all tickets

### Debug Mode

To see detailed logs of save/load operations, you can add print statements:

```python
def save_tickets():
    """Save tickets to CSV"""
    global df
    print(f"💾 Saving {len(df)} tickets to CSV...")
    df.to_csv('tickets.csv', index=False)
    print("✅ Save complete!")
```

### Need More Help?

1. Check the Flask console for error messages
2. Verify `tickets.csv` exists in the project directory
3. Check browser console (F12) for JavaScript errors
4. Ensure all dependencies are installed: `pip install -r requirements.txt`
