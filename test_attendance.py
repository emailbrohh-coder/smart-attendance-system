#!/usr/bin/env python3
"""
Test attendance marking
"""

import csv
import os
from datetime import datetime
import json

ATT_FILE = "attendance.csv"

# Load periods
with open("periods.json", "r") as f:
    periods_data = json.load(f)
    periods_list = periods_data["periods"]

def get_current_period():
    """Return current period number (1-7) or "-" if outside period times."""
    now = datetime.now()
    current_time = now.time()
    
    for period in periods_list:
        start = datetime.strptime(period["start"], "%H:%M").time()
        end = datetime.strptime(period["end"], "%H:%M").time()
        
        if start <= current_time < end:
            return period["number"]
    
    # If outside period times, return "-" to allow flexible attendance
    return "-"

def is_already_marked(uid, date, period):
    """Check if attendance already exists in CSV for this uid+date+period"""
    if not os.path.exists(ATT_FILE):
        return False
    
    with open(ATT_FILE, "r", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if (row.get("ID", "").strip() == str(uid) and 
                row.get("Date", "").strip() == date and 
                row.get("Period", "").strip() == str(period)):
                return True
    return False

def test_mark_attendance(uid, pin):
    """Test marking attendance"""
    today = datetime.now().strftime("%Y-%m-%d")
    period = get_current_period()
    
    print(f"📅 Testing attendance for:")
    print(f"   ID: {uid}")
    print(f"   PIN: {pin}")
    print(f"   Date: {today}")
    print(f"   Period: {period}")
    
    # Check if already marked
    if is_already_marked(uid, today, period):
        print(f"⚠️ Already marked: {pin} for {today} period {period}")
        return False

    now = datetime.now()

    # Mark attendance
    with open(ATT_FILE, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([uid, pin, today, period, now.strftime("%H:%M:%S")])

    print(f"✅ Attendance Marked: {pin} (Date: {today}, Period: {period})")
    return True

if __name__ == "__main__":
    print("🧪 Testing Attendance Marking")
    print("=" * 40)
    
    # Test with a known student
    test_mark_attendance(19, "23155-CM-067")
    
    print("\n📊 Checking recent records...")
    with open(ATT_FILE, "r", newline="") as f:
        reader = csv.DictReader(f)
        records = list(reader)
    
    print(f"Total records: {len(records)}")
    print("Last 3 records:")
    for record in records[-3:]:
        print(f"  ID:{record.get('ID')} PIN:{record.get('PIN')} Date:{record.get('Date')} Period:{record.get('Period')} Time:{record.get('Time')}")