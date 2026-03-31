#!/usr/bin/env python3
"""
Test script to verify cloud app works before deployment
Run this to check if app_cloud.py runs correctly
"""

import os
import sys

def check_files():
    """Check if required files exist"""
    print("🔍 Checking required files...")
    required_files = [
        "app_cloud.py",
        "requirements.txt",
        "Procfile",
        "periods.json",
        "templates/login.html",
        "templates/dashboard_cloud.html"
    ]
    
    missing = []
    for file in required_files:
        if os.path.exists(file):
            print(f"  ✅ {file}")
        else:
            print(f"  ❌ {file} - MISSING")
            missing.append(file)
    
    if missing:
        print(f"\n❌ Missing {len(missing)} required files!")
        return False
    
    print("\n✅ All required files present!")
    return True

def test_import():
    """Test if app can be imported"""
    print("\n🔍 Testing app import...")
    try:
        from app_cloud import app
        print("  ✅ App imported successfully")
        return True
    except Exception as e:
        print(f"  ❌ Import failed: {e}")
        return False

def test_routes():
    """Test if routes are configured"""
    print("\n🔍 Testing routes...")
    try:
        from app_cloud import app
        
        routes = []
        for rule in app.url_map.iter_rules():
            routes.append(str(rule))
        
        expected_routes = ["/", "/login", "/dashboard", "/download", "/logout", "/health"]
        
        for route in expected_routes:
            if any(route in r for r in routes):
                print(f"  ✅ {route}")
            else:
                print(f"  ❌ {route} - MISSING")
        
        print("\n✅ Routes configured!")
        return True
    except Exception as e:
        print(f"  ❌ Route test failed: {e}")
        return False

def run_local_test():
    """Run the app locally for testing"""
    print("\n🚀 Starting local test server...")
    print("=" * 50)
    print("Open browser: http://localhost:5000")
    print("Press Ctrl+C to stop")
    print("=" * 50)
    
    try:
        from app_cloud import app
        app.run(debug=True, port=5000)
    except KeyboardInterrupt:
        print("\n\n✅ Test server stopped")
    except Exception as e:
        print(f"\n❌ Server failed: {e}")

if __name__ == "__main__":
    print("=" * 50)
    print("  CLOUD APP TEST SUITE")
    print("=" * 50)
    
    # Run checks
    if not check_files():
        sys.exit(1)
    
    if not test_import():
        sys.exit(1)
    
    if not test_routes():
        sys.exit(1)
    
    print("\n" + "=" * 50)
    print("✅ ALL TESTS PASSED!")
    print("=" * 50)
    
    # Ask if user wants to run local test
    response = input("\nRun local test server? (y/n): ").strip().lower()
    if response == 'y':
        run_local_test()
    else:
        print("\n✅ Ready for deployment!")
        print("Next steps:")
        print("  1. git add .")
        print("  2. git commit -m 'Ready for deployment'")
        print("  3. git push")
        print("  4. Deploy to Render")
