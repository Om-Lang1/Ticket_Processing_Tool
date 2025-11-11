# Quick Start Guide

## 🚀 Get Started in 3 Steps

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Run the Application
```bash
python app.py
```

### Step 3: Open in Browser
Navigate to: **http://localhost:5000**

---

## ✅ Verify Everything Works

### Test 1: Create a Ticket
1. Fill in the issue description
2. Select priority (High/Medium/Low)
3. Click "Submit Ticket"
4. ✅ Ticket should appear in the table below

### Test 2: Verify Persistence
1. Refresh the page (F5)
2. ✅ Your ticket should still be there

### Test 3: Edit a Ticket
1. Click on any Status or Priority cell
2. Select a new value
3. ✅ Change should be saved automatically

### Test 4: Delete Tickets
1. Check the boxes next to tickets you want to delete
2. Click "🗑️ Delete Selected"
3. Confirm deletion
4. ✅ Tickets should be removed

### Test 5: Server Restart
1. Stop the Flask server (Ctrl+C)
2. Start it again: `python app.py`
3. Refresh browser
4. ✅ All your changes should still be there

---

## 📁 Files Generated

After first run, you'll see:
- **`tickets.csv`** - Your ticket database (100 sample tickets + any you create)

---

## 🔍 Troubleshooting

### Tickets not saving?
Run the test script:
```bash
python test_save.py
```

### Port already in use?
Change the port in `app.py`:
```python
app.run(debug=True, port=5001)  # Change 5000 to 5001
```

### Can't access the app?
Make sure:
- Flask is running (you should see output in terminal)
- You're using the correct URL: http://localhost:5000
- No firewall is blocking port 5000

---

## 📊 What You'll See

### Dashboard Sections
1. **Add a Ticket** - Form to create new tickets
2. **Existing Tickets** - Table with all tickets (editable, sortable, deletable)
3. **Statistics** - Metrics and charts showing ticket analytics

### Features
- ✨ Create tickets with custom descriptions and priorities
- ✏️ Edit Status and Priority by clicking cells
- 🗑️ Delete single or multiple tickets
- ☑️ Select all tickets with one click
- 📊 View real-time statistics and charts
- 🔄 Auto-updating dashboard

---

## 🎯 Next Steps

1. **Customize**: Edit the issue descriptions in `app.py`
2. **Style**: Modify colors and design in `templates/index.html`
3. **Extend**: Add new fields like "Assigned To" or "Due Date"
4. **Deploy**: Host on a server for team access

---

## 📚 Documentation

- **README.md** - Full documentation
- **TROUBLESHOOTING.md** - Detailed troubleshooting guide
- **app.py** - Backend code with comments

---

## 💡 Tips

- **Keyboard Shortcuts**: Click column headers to sort
- **Bulk Operations**: Use "Select All" checkbox for mass deletion
- **Data Safety**: `tickets.csv` is your backup - don't delete it!
- **Fresh Start**: Delete `tickets.csv` to reset to 100 sample tickets

---

Enjoy your Support Ticket System! 🎫
