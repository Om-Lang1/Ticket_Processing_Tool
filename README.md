# 🎫 Support Tickets - Flask Application

A modern, user-friendly support ticket management system built with Flask and vanilla JavaScript.

## Features

- ✨ **Create Tickets**: Submit new support tickets with issue descriptions and priority levels
- 📝 **Edit Tickets**: Click on Status or Priority cells to edit them inline
- 🗑️ **Delete Tickets**: Select individual tickets, multiple tickets, or all tickets to delete them
- ☑️ **Bulk Selection**: Use checkboxes to select tickets and "Select All" for bulk operations
- 📊 **Statistics Dashboard**: View real-time metrics and charts
- 🎨 **Modern UI**: Beautiful gradient design with smooth animations
- 📱 **Responsive**: Works seamlessly on desktop and mobile devices
- 🔄 **Auto-refresh**: Charts and statistics update automatically when tickets are modified

## Installation

1. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the application**:
   ```bash
   python app.py
   ```

3. **Open your browser**:
   Navigate to `http://localhost:5000`

## Usage

### Adding a Ticket
1. Fill in the issue description in the text area
2. Select a priority level (High, Medium, or Low)
3. Click "Submit Ticket"

### Editing Tickets
- Click on any Status or Priority cell in the table
- Select a new value from the dropdown
- The change is saved automatically

### Deleting Tickets
- **Select individual tickets**: Check the checkbox next to each ticket you want to delete
- **Select all tickets**: Click the checkbox in the table header to select/deselect all tickets
- **Delete selected**: Click the "🗑️ Delete Selected" button that appears when tickets are selected
- Confirm the deletion in the popup dialog

### Sorting Tickets
- Click on any column header to sort the table
- Click again to reverse the sort order

### Viewing Statistics
- **Metrics**: View open tickets count and response times
- **Status Chart**: See ticket distribution by month and status
- **Priority Chart**: View current ticket priorities in a doughnut chart

## Project Structure

```
ticket tool/
├── app.py                 # Flask backend with API endpoints
├── templates/
│   └── index.html        # Frontend with HTML, CSS, and JavaScript
├── requirements.txt      # Python dependencies
├── tickets.csv          # Data storage (auto-generated)
└── README.md            # This file
```

## API Endpoints

- `GET /` - Main application page
- `GET /api/tickets` - Get all tickets
- `POST /api/tickets` - Create a new ticket
- `PUT /api/tickets/<ticket_id>` - Update a ticket
- `POST /api/tickets/delete` - Delete multiple tickets (requires `ticket_ids` array in request body)
- `GET /api/statistics` - Get ticket statistics

## Technologies Used

- **Backend**: Flask (Python)
- **Frontend**: HTML5, CSS3, Vanilla JavaScript
- **Charts**: Chart.js
- **Data Processing**: Pandas, NumPy
- **Storage**: CSV file

## Features Comparison with Streamlit Version

✅ All Streamlit functionality implemented:
- Ticket creation with form validation
- Editable ticket table
- Real-time statistics
- Interactive charts (status by month, priority distribution)
- Persistent data storage
- Responsive design

🎨 Additional improvements:
- Modern gradient UI design
- Smooth animations and transitions
- Better mobile responsiveness
- Inline editing with dropdowns
- Checkbox selection for bulk operations
- Delete functionality with confirmation
- Success/delete notifications
- Sortable table columns
- Real-time selection counter

## Notes

- **Data Persistence**: The application uses a CSV file (`tickets.csv`) for persistent storage
  - All tickets are automatically saved to CSV after any create/update/delete operation
  - Data persists across server restarts
  - The CSV file is created automatically on first run with 100 sample tickets
- **Data Reloading**: Each API request reloads data from CSV to ensure consistency
- **Secret Key**: Should be changed in production (see `app.py`)
- **Auto-refresh**: Charts and statistics update automatically when tickets are modified
- **Testing**: Run `python test_save.py` to verify data persistence is working

## License

Free to use and modify for your projects!
