#!/usr/bin/env python3
"""
Test dashboard data reading
"""

from app import read_attendance

def test_dashboard():
    print("🔍 Testing dashboard data reading...")
    
    # Test reading all records
    all_records = read_attendance()
    print(f"📊 Total records: {len(all_records)}")
    
    # Show recent records
    print("\n📋 Recent 5 records:")
    for i, record in enumerate(all_records[-5:]):
        print(f"  {i+1}. ID:{record['ID']} PIN:{record['PIN']} Date:{record['Date']} Period:{record['Period']} Time:{record['Time']}")
    
    # Test filtering by today's date
    today = "2026-03-16"
    today_records = read_attendance(date_filter=today)
    print(f"\n📅 Today's records ({today}): {len(today_records)}")
    
    for record in today_records:
        print(f"  - ID:{record['ID']} PIN:{record['PIN']} Period:{record['Period']} Time:{record['Time']}")
    
    # Test filtering by PIN
    test_pin = "23155-CM-067"
    pin_records = read_attendance(pin_filter=test_pin)
    print(f"\n👤 Records for PIN {test_pin}: {len(pin_records)}")
    
    for record in pin_records[-3:]:
        print(f"  - Date:{record['Date']} Period:{record['Period']} Time:{record['Time']}")

if __name__ == "__main__":
    test_dashboard()