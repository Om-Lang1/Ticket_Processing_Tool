# 🔐 Authorization System Guide

## Overview

The Support Ticket system now has role-based access control with two user types:
- **👤 User** - Can only submit tickets
- **👨‍💼 Admin** - Full access to view, edit, delete tickets and view statistics

## 🚀 How to Use

### Step 1: Start the Application
```bash
python app.py
```

### Step 2: Open Browser
Navigate to: **http://localhost:5000**

You'll be redirected to the login page automatically.

### Step 3: Select Your Role

**Option 1: Login as User**
1. Select "👤 User (Submit Tickets)" from dropdown
2. Click "Continue"
3. No password required ✅

**Option 2: Login as Admin**
1. Select "👨‍💼 Admin (Manage Tickets)" from dropdown
2. Enter password: `admin@123`
3. Click "Continue"

## 👤 User Role

### What Users Can Do:
- ✅ Submit new support tickets
- ✅ View all existing tickets
- ✅ See ticket details (ID, Issue, Status, Priority, Date)

### What Users CANNOT Do:
- ❌ Edit ticket status or priority
- ❌ Delete tickets
- ❌ View statistics and dashboard
- ❌ Select/bulk delete tickets

### User Interface:
```
┌─────────────────────────────────────┐
│  👤 User              [Logout]      │
├─────────────────────────────────────┤
│  Add a Ticket                       │
│  [Form to submit new tickets]       │
├─────────────────────────────────────┤
│  Existing Tickets                   │
│  [Read-only table view]             │
│  - No checkboxes                    │
│  - No edit functionality            │
│  - No delete button                 │
│  - No statistics section            │
└─────────────────────────────────────┘
```

## 👨‍💼 Admin Role

### What Admins Can Do:
- ✅ Everything users can do, PLUS:
- ✅ Edit ticket status (Open/In Progress/Closed)
- ✅ Edit ticket priority (High/Medium/Low)
- ✅ Delete individual tickets
- ✅ Bulk delete multiple tickets
- ✅ View statistics dashboard
- ✅ View charts and metrics

### Admin Password:
```
admin@123
```

### Admin Interface:
```
┌─────────────────────────────────────┐
│  👨‍💼 Admin            [Logout]      │
├─────────────────────────────────────┤
│  Add a Ticket                       │
│  [Form to submit new tickets]       │
├─────────────────────────────────────┤
│  Existing Tickets                   │
│  💡 Admin Tips: Edit, Delete, Sort  │
│  [Selected: 0] [🗑️ Delete Selected] │
│  ┌───┬────┬───────┬────────┬─────┐ │
│  │☑│ ID │ Issue │ Status │ ... │ │
│  ├───┼────┼───────┼────────┼─────┤ │
│  │☐│1100│ ...   │ [Edit] │ ... │ │
│  └───┴────┴───────┴────────┴─────┘ │
├─────────────────────────────────────┤
│  Statistics                         │
│  [Metrics, Charts, Analytics]       │
└─────────────────────────────────────┘
```

## 🔒 Security Features

### Session-Based Authentication
- User role stored in Flask session
- Session persists until logout
- Automatic redirect to login if not authenticated

### Protected Routes
- **Public**: `/login` (login page)
- **Authenticated**: `/` (main app - requires login)
- **Admin Only**: 
  - `PUT /api/tickets/<id>` (edit tickets)
  - `POST /api/tickets/delete` (delete tickets)

### Password Protection
- Admin access requires password
- User access has no password (instant access)
- Password: `admin@123` (change in production!)

## 🎯 Feature Comparison

| Feature | User | Admin |
|---------|------|-------|
| Submit Tickets | ✅ | ✅ |
| View Tickets | ✅ | ✅ |
| Edit Status/Priority | ❌ | ✅ |
| Delete Tickets | ❌ | ✅ |
| Bulk Delete | ❌ | ✅ |
| View Statistics | ❌ | ✅ |
| View Charts | ❌ | ✅ |
| Select Tickets | ❌ | ✅ |

## 📝 How It Works

### Login Flow
```
User visits http://localhost:5000
    ↓
Not logged in? → Redirect to /login
    ↓
Select role (User or Admin)
    ↓
Admin? → Enter password
    ↓
Validate credentials
    ↓
Create session with role
    ↓
Redirect to main app
    ↓
Show features based on role
```

### Role-Based UI
The frontend dynamically shows/hides elements based on role:

**Admin-Only Elements:**
- Checkbox column in table
- Edit functionality on Status/Priority cells
- Delete button and selection counter
- Statistics section with charts
- Admin tips info box

**Always Visible:**
- Add ticket form
- Tickets table (read-only for users)
- Ticket count
- Logout button

## 🔄 Logout

Click the **Logout** button in the top-right corner to:
1. Clear your session
2. Return to login page
3. Require re-authentication

## 🛠️ Customization

### Change Admin Password
Edit `app.py`:
```python
ADMIN_PASSWORD = 'your-new-password'
```

### Add More Roles
You can extend the system to add more roles:
1. Update login.html dropdown
2. Add role validation in app.py
3. Create role-specific decorators
4. Update frontend role checks

### Customize Permissions
Edit the decorators in `app.py`:
```python
@admin_required  # Requires admin role
@login_required  # Requires any logged-in user
```

## 🧪 Testing

### Test User Access
1. Login as User (no password)
2. Try to submit a ticket ✅
3. Try to edit a ticket ❌ (cells not clickable)
4. Try to delete a ticket ❌ (no delete button)
5. Look for statistics ❌ (section hidden)

### Test Admin Access
1. Login as Admin (password: admin@123)
2. Submit a ticket ✅
3. Edit ticket status ✅ (click on badge)
4. Delete tickets ✅ (select and delete)
5. View statistics ✅ (charts visible)

## 🚨 Important Notes

### Security
- **Change the admin password in production!**
- Current password is for demo purposes only
- Consider adding password hashing
- Add HTTPS in production

### Session Management
- Sessions persist until logout or server restart
- Secret key should be changed in production
- Sessions are server-side (Flask session)

### Data Persistence
- All ticket data persists in `tickets.csv`
- Role information is session-based only
- No user database (sessions only)

## 📊 API Endpoints

### Public
- `GET /login` - Login page
- `POST /login` - Handle login

### Authenticated (Any Role)
- `GET /` - Main application
- `GET /api/tickets` - Get all tickets
- `POST /api/tickets` - Create ticket
- `GET /api/user/role` - Get current user role
- `GET /logout` - Logout

### Admin Only
- `PUT /api/tickets/<id>` - Update ticket
- `POST /api/tickets/delete` - Delete tickets
- `GET /api/statistics` - Get statistics

## 💡 Tips

### For Users
- Focus on describing issues clearly
- Set appropriate priority levels
- Check existing tickets before creating duplicates

### For Admins
- Regularly update ticket statuses
- Use bulk delete for cleanup
- Monitor statistics for trends
- Keep tickets organized

## 🎉 Summary

**Login Page:**
- Beautiful gradient design
- Role selection dropdown
- Password field for admin
- Role descriptions

**User Experience:**
- Simple, focused interface
- Submit tickets easily
- View ticket status
- No complex features

**Admin Experience:**
- Full control over tickets
- Edit and delete capabilities
- Statistics and analytics
- Bulk operations

The authorization system ensures users can submit tickets while admins have full management capabilities!
