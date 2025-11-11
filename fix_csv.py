"""
Script to clean the tickets.csv file by removing the Month column
"""
import pandas as pd

print("🔧 Cleaning tickets.csv...")

# Read the CSV
df = pd.read_csv('tickets.csv')
print(f"   Current columns: {list(df.columns)}")

# Keep only core columns
core_columns = ['ID', 'Issue', 'Status', 'Priority', 'Date Submitted']
df_clean = df[core_columns]

# Save back to CSV
df_clean.to_csv('tickets.csv', index=False)

print(f"✅ Cleaned! New columns: {list(df_clean.columns)}")
print(f"📊 Total tickets: {len(df_clean)}")
