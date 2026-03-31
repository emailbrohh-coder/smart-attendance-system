#!/usr/bin/env python3
"""
Debug script to check attendance system
"""

import csv
import os
from datetime import datetime
import json

ATT_FILE = "attendance.csv"

def check_attendance_file():
    print("🔍 Checking attendance.csv file...")
    
    if not os.path.exists(ATT_FILE):
        print("❌ attendance.csv does not exist!")
        return
    
    print(f"✅ File exists: {ATT_FILE}")
    
    # Read and display recent records
    with open(ATT_FILE, "r", newline="") as f:
        reader = csv.DictReader(f)
        records = list(reader)
    
    print(f"📊 Total records: {len(records)}")
    
    if records:
        print("\n📋 Recent 5 records:")
        for i, record in enumerate(records[-5:]):
            print(f"  {i+1}. ID:{record.get('ID', 'N/A')} PIN:{record.get('PIN', 'N/A')} Date:{record.get('Date', 'N/A')} Period:{record.get('Period', 'N/A')} Time:{record.get('Time', 'N/A')}")
    
    # Check today's records
    today = datetime.now().strftime("%Y-%m-%d")
    today_records = [r for r in records if r.get('Date', '') == today]
    print(f"\n📅 Today's records ({today}): {len(today_records)}")
    
    for record in today_records:
        print(f"  - ID:{record.get('ID', 'N/A')} PIN:{record.get('PIN', 'N/A')} Period:{record.get('Period', 'N/A')} Time:{record.get('Time', 'N/A')}")

def check_periods():
    print("\n⏰ Checking periods configuration...")
    
    try:
        with open("periods.json", "r") as f:
            periods_data = json.load(f)
            periods_list = periods_data["periods"]
        
        print(f"✅ Loaded {len(periods_list)} periods")
        
        now = datetime.now()
        current_time = now.time()
        current_period = None
        
        for period in periods_list:
            start = datetime.strptime(period["start"], "%H:%M").time()
            end = datetime.strptime(period["end"], "%H:%M").time()
            
            print(f"  Period {period['number']}: {period['start']} - {period['end']}")
            
            if start <= current_time < end:
                current_period = period["number"]
        
        print(f"\n🕐 Current time: {current_time.strftime('%H:%M')}")
        print(f"📍 Current period: {current_period if current_period else 'Outside period times'}")
        
    except Exception as e:
        print(f"❌ Error reading periods: {e}")

def check_names():
    print("\n👥 Checking names.txt...")
    
    if not os.path.exists("names.txt"):
        print("❌ names.txt does not exist!")
        return
    
    names = {}
    with open("names.txt", "r") as f:
        for line in f:
            if line.strip():
                try:
                    uid, name = line.strip().split(",", 1)
                    names[int(uid)] = name
                except:
                    print(f"⚠️ Invalid line: {line.strip()}")
    
    print(f"✅ Loaded {len(names)} names")
    for uid, name in list(names.items())[:5]:
        print(f"  ID {uid}: {name}")
    
    if len(names) > 5:
        print(f"  ... and {len(names) - 5} more")

if __name__ == "__main__":
    print("=" * 50)
    print("  ATTENDANCE SYSTEM DEBUG")
    print("=" * 50)
    
    check_attendance_file()
    check_periods()
    check_names()
    
    print("\n" + "=" * 50)
    print("✅ Debug complete!")