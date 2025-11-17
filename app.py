import datetime
import random
import json
from flask import Flask, render_template, request, jsonify, session, redirect, url_for, send_file
from functools import wraps
import pandas as pd
import numpy as np
import io

app = Flask(__name__)
app.secret_key = 'your-secret-key-here-change-in-production'

# Admin password
ADMIN_PASSWORD = 'admin@123'

# Decorator to require login
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'role' not in session:
            return redirect(url_for('login_page'))
        return f(*args, **kwargs)
    return decorated_function

# Decorator to require admin role
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'role' not in session:
            return redirect(url_for('login_page'))
        if session.get('role') != 'admin':
            return jsonify({"success": False, "error": "Admin access required"}), 403
        return f(*args, **kwargs)
    return decorated_function

# Initialize the dataframe
def initialize_dataframe():
    """Create initial ticket data"""
    np.random.seed(42)
    
    issue_descriptions = [
        "Network connectivity issues in the office",
        "Software application crashing on startup",
        "Printer not responding to print commands",
        "Email server downtime",
        "Data backup failure",
        "Login authentication problems",
        "Website performance degradation",
        "Security vulnerability identified",
        "Hardware malfunction in the server room",
        "Employee unable to access shared files",
        "Database connection failure",
        "Mobile application not syncing data",
        "VoIP phone system issues",
        "VPN connection problems for remote employees",
        "System updates causing compatibility issues",
        "File server running out of storage space",
        "Intrusion detection system alerts",
        "Inventory management system errors",
        "Customer data not loading in CRM",
        "Collaboration tool not sending notifications",
    ]
    
    data = {
        "ID": [f"TICKET-{i}" for i in range(1100, 1000, -1)],
        "Issue": np.random.choice(issue_descriptions, size=100).tolist(),
        "Status": np.random.choice(["Open", "In Progress", "Closed"], size=100).tolist(),
        "Priority": np.random.choice(["High", "Medium", "Low"], size=100).tolist(),
        "Date Submitted": [
            (datetime.date(2023, 6, 1) + datetime.timedelta(days=random.randint(0, 182))).strftime("%Y-%m-%d")
            for _ in range(100)
        ],
    }
    df = pd.DataFrame(data)
    return df

# Load or initialize tickets
def load_tickets():
    """Load tickets from CSV or initialize new dataframe"""
    global df
    try:
        df = pd.read_csv('tickets.csv')
        
        # Define all required columns
        required_columns = [
            'ID', 'Username', 'Department', 'Issue', 
            'Status', 'Priority', 'Date Submitted', 'Company'
        ]
        
        # Add any missing columns with default values
        for col in required_columns:
            if col not in df.columns:
                if col == 'Status':
                    df[col] = 'Open'
                elif col == 'Priority':
                    df[col] = 'Medium'
                elif col == 'Date Submitted':
                    df[col] = datetime.datetime.now().strftime("%Y-%m-%d")
                elif col in ['Company', 'Username', 'Department']:
                    df[col] = 'N/A'
        
        # Ensure data types are correct
        for col in df.columns:
            if col in ['ID', 'Issue', 'Status', 'Priority', 'Company', 'Username', 'Department']:
                df[col] = df[col].astype(str)
            if col == 'Date Submitted':
                df[col] = pd.to_datetime(df[col]).dt.strftime('%Y-%m-%d')
                
        # Reorder columns to maintain consistency
        existing_columns = [col for col in required_columns if col in df.columns]
        df = df[existing_columns]
        
        return df
    except FileNotFoundError:
        df = initialize_dataframe()
        # Ensure the Company column exists in the new dataframe
        if 'Company' not in df.columns:
            df['Company'] = 'N/A'
        df.to_csv('tickets.csv', index=False)
        return df

def save_tickets():
    """Save tickets to CSV"""
    global df
    
    # Define all required columns in the desired order
    required_columns = [
        'ID', 'Username', 'Department', 'Issue', 
        'Status', 'Priority', 'Date Submitted', 'Company'
    ]
    
    # Add any missing columns with default values
    for col in required_columns:
        if col not in df.columns:
            if col == 'Status':
                df[col] = 'Open'
            elif col == 'Priority':
                df[col] = 'Medium'
            elif col == 'Date Submitted':
                df[col] = datetime.datetime.now().strftime("%Y-%m-%d")
            elif col in ['Company', 'Username', 'Department']:
                df[col] = 'N/A'
    
    # Ensure all string columns are properly encoded
    string_columns = ['ID', 'Username', 'Department', 'Issue', 'Status', 'Priority', 'Company']
    for col in string_columns:
        if col in df.columns:
            df[col] = df[col].astype(str)
    
    # Ensure date is in the correct format
    if 'Date Submitted' in df.columns:
        df['Date Submitted'] = pd.to_datetime(df['Date Submitted']).dt.strftime('%Y-%m-%d')
    
    # Reorder columns to maintain consistency
    existing_columns = [col for col in required_columns if col in df.columns]
    
    # Save to CSV with all columns
    df[existing_columns].to_csv('tickets.csv', index=False)

# Initialize dataframe
df = load_tickets()

@app.route('/login')
def login_page():
    """Render the login page"""
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    """Handle login"""
    data = request.json
    role = data.get('role')
    password = data.get('password', '')
    
    if role == 'admin':
        if password == ADMIN_PASSWORD:
            session['role'] = 'admin'
            return jsonify({"success": True})
        else:
            return jsonify({"success": False, "message": "Invalid admin password"})
    elif role == 'user':
        session['role'] = 'user'
        return jsonify({"success": True})
    else:
        return jsonify({"success": False, "message": "Invalid role"})

@app.route('/logout')
def logout():
    """Handle logout"""
    session.clear()
    return redirect(url_for('login_page'))

@app.route('/api/user/role', methods=['GET'])
@login_required
def get_user_role():
    """Get current user's role"""
    return jsonify({"role": session.get('role', 'user')})

@app.route('/')
@login_required
def index():
    """Render the main page"""
    user_role = session.get('role', 'user')
    return render_template('index.html', role=user_role)

@app.route('/api/tickets', methods=['GET'])
@login_required
def get_tickets():
    """Get all tickets"""
    global df
    df = load_tickets()
    
    # Define all columns we want to return
    columns = [
        'ID', 'Username', 'Department', 'Issue', 
        'Status', 'Priority', 'Date Submitted', 'Company'
    ]
    
    # Only include columns that exist in the dataframe
    existing_columns = [col for col in columns if col in df.columns]
    
    # Create a clean copy with only the columns we want to return
    df_clean = df[existing_columns].copy()
    
    # Convert to list of dictionaries
    tickets = df_clean.to_dict('records')
    
    # If user is not admin, only show their own tickets
    if session.get('role') != 'admin':
        tickets = [t for t in tickets if t.get('Status') != 'Resolved']
    
    return jsonify(tickets)

@app.route('/api/tickets', methods=['POST'])
def add_ticket():
    """Add a new ticket"""
    global df
    data = request.json
    print(f"API: Received new ticket request: {data}")
    
    # Reload to ensure we have latest data
    df = load_tickets()
    print(f"   Current tickets in DB: {len(df)}")
    
    # Get the next ticket number
    if len(df) > 0:
        recent_ticket_number = int(df['ID'].max().split('-')[1])
    else:
        recent_ticket_number = 1000
    
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    
    new_ticket = {
        "ID": f"TICKET-{recent_ticket_number + 1}",
        "Username": data.get('username', 'N/A'),
        "Department": data.get('department', 'N/A'),
        "Issue": data['issue'],
        "Status": "Open",
        "Priority": data['priority'],
        "Date Submitted": today,
        "Company": data.get('company', 'N/A')
    }
    
    print(f"   Creating ticket: {new_ticket['ID']}")
    
    # Add to dataframe
    new_df = pd.DataFrame([new_ticket])
    df = pd.concat([new_df, df], ignore_index=True)
    save_tickets()
    
    print(f"Ticket saved! Total tickets now: {len(df)}")
    
    return jsonify(new_ticket)

@app.route('/api/tickets/<ticket_id>', methods=['PUT'])
@admin_required
def update_ticket(ticket_id):
    """Update an existing ticket - Admin only"""
    global df
    data = request.json
    
    # Reload to ensure we have latest data
    df = load_tickets()
    
    # Find and update the ticket
    idx = df[df['ID'] == ticket_id].index
    if len(idx) > 0:
        if 'Status' in data:
            df.loc[idx, 'Status'] = data['Status']
        if 'Priority' in data:
            df.loc[idx, 'Priority'] = data['Priority']
        if 'Issue' in data:
            df.loc[idx, 'Issue'] = data['Issue']
        
        save_tickets()
        return jsonify({"success": True})
    
    return jsonify({"success": False, "error": "Ticket not found"}), 404

@app.route('/api/tickets/delete', methods=['POST'])
@admin_required
def delete_tickets():
    """Delete multiple tickets - Admin only"""
    global df
    data = request.json
    ticket_ids = data.get('ticket_ids', [])
    
    if not ticket_ids:
        return jsonify({"success": False, "error": "No ticket IDs provided"}), 400
    
    # Reload to ensure we have latest data
    df = load_tickets()
    
    # Remove tickets with matching IDs
    df = df[~df['ID'].isin(ticket_ids)]
    save_tickets()
    
    return jsonify({"success": True, "deleted_count": len(ticket_ids)})

@app.route('/api/statistics', methods=['GET'])
def get_statistics():
    """Get ticket statistics"""
    global df
    
    # Reload to ensure we have latest data
    df = load_tickets()
    
    # Create a COPY of the dataframe for statistics to avoid modifying the original
    df_stats = df.copy()
    
    # Calculate statistics
    num_open = len(df_stats[df_stats['Status'] == 'Open'])
    num_in_progress = len(df_stats[df_stats['Status'] == 'In Progress'])
    num_closed = len(df_stats[df_stats['Status'] == 'Closed'])
    
    # Status per month data - work on the copy
    df_stats['Date Submitted'] = pd.to_datetime(df_stats['Date Submitted'], errors='coerce')
    df_stats['Month'] = df_stats['Date Submitted'].dt.strftime('%Y-%m')
    
    # Remove rows with NaN months (invalid dates)
    df_stats = df_stats.dropna(subset=['Month'])
    
    status_by_month = df_stats.groupby(['Month', 'Status']).size().reset_index(name='count')
    status_data = status_by_month.to_dict('records')
    
    # Priority distribution
    priority_counts = df['Priority'].value_counts().to_dict()
    
    stats = {
        "num_open": num_open,
        "num_in_progress": num_in_progress,
        "num_closed": num_closed,
        "total": len(df),
        "status_by_month": status_data,
        "priority_counts": priority_counts
    }
    
    print(f"Statistics calculated for {len(df)} tickets")
    
    return jsonify(stats)

@app.route('/api/tickets/export', methods=['GET'])
@admin_required
def export_tickets():
    """Export all tickets to Excel - Admin only"""
    global df
    
    # Reload to ensure we have latest data
    df = load_tickets()
    
    # Create a copy of the dataframe for export
    export_df = df.copy()
    
    # Ensure all required columns are present and in the correct order
    columns_order = [
        'ID', 'Username', 'Department', 'Issue', 
        'Status', 'Priority', 'Date Submitted', 'Company'
    ]
    
    # Only include columns that exist in the dataframe
    existing_columns = [col for col in columns_order if col in export_df.columns]
    export_df = export_df[existing_columns]
    
    # Create Excel file in memory
    output = io.BytesIO()
    
    # Use openpyxl engine for better Excel formatting
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        export_df.to_excel(writer, sheet_name='Tickets', index=False)
        
        # Get the workbook and worksheet
        workbook = writer.book
        worksheet = writer.sheets['Tickets']
        
        # Auto-adjust column widths
        for column in worksheet.columns:
            max_length = 0
            column_letter = column[0].column_letter
            for cell in column:
                try:
                    if len(str(cell.value)) > max_length:
                        max_length = len(str(cell.value))
                except:
                    pass
            adjusted_width = min(max_length + 2, 50)  # Cap at 50 characters
            worksheet.column_dimensions[column_letter].width = adjusted_width
    
    output.seek(0)
    
    # Generate filename with current date
    current_date = datetime.datetime.now().strftime("%Y-%m-%d")
    filename = f"tickets_export_{current_date}.xlsx"
    
    return send_file(
        output,
        mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        as_attachment=True,
        download_name=filename
    )

if __name__ == '__main__':
    app.run(debug=True, port=5000)
