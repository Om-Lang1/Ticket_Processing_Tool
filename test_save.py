"""
Simple test script to verify ticket saving functionality
"""
import pandas as pd
import os

# Check if tickets.csv exists
if os.path.exists('tickets.csv'):
    print("✅ tickets.csv exists")
    df = pd.read_csv('tickets.csv')
    print(f"📊 Number of tickets in CSV: {len(df)}")
    print(f"📋 Columns: {list(df.columns)}")
    print("\n🎫 First 3 tickets:")
    print(df.head(3).to_string())
else:
    print("❌ tickets.csv does not exist yet")
    print("Run the Flask app first to generate initial data")
