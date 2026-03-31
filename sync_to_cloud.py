#!/usr/bin/env python3
"""
Quick script to sync attendance.csv to cloud (via git)
Run this after marking attendance locally to update the cloud dashboard
"""

import subprocess
import sys
from datetime import datetime

def run_command(cmd):
    """Run shell command and return output"""
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        return False, "", str(e)

def sync_attendance():
    print("🔄 Syncing attendance data to cloud...")
    print("-" * 50)
    
    # Check if git is initialized
    success, _, _ = run_command("git status")
    if not success:
        print("❌ Git not initialized. Run 'git init' first.")
        return False
    
    # Add attendance.csv
    print("📝 Adding attendance.csv...")
    success, _, error = run_command("git add attendance.csv")
    if not success:
        print(f"❌ Failed to add file: {error}")
        return False
    
    # Check if there are changes
    success, output, _ = run_command("git status --porcelain")
    if not output.strip():
        print("✅ No changes to sync. Attendance is up to date!")
        return True
    
    # Commit changes
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    commit_msg = f"Update attendance - {timestamp}"
    print(f"💾 Committing changes: {commit_msg}")
    success, _, error = run_command(f'git commit -m "{commit_msg}"')
    if not success:
        print(f"❌ Failed to commit: {error}")
        return False
    
    # Push to remote
    print("☁️ Pushing to cloud...")
    success, output, error = run_command("git push")
    if not success:
        print(f"❌ Failed to push: {error}")
        print("\nTip: Make sure you've set up remote:")
        print("  git remote add origin https://github.com/YOUR_USERNAME/smart-attendance-system.git")
        return False
    
    print("-" * 50)
    print("✅ Sync complete! Cloud dashboard will update in 1-2 minutes.")
    return True

if __name__ == "__main__":
    try:
        success = sync_attendance()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n⚠️ Sync cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1)
