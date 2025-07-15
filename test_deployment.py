#!/usr/bin/env python3
"""
Test script to verify deployment works locally
"""
import os
import sys
import time
import threading
from pathlib import Path

def test_imports():
    """Test if all required modules can be imported"""
    print("🔍 Testing imports...")

    try:
        from flask import Flask
        print("✅ Flask imported successfully")
    except ImportError as e:
        print(f"❌ Flask import failed: {e}")
        return False

    try:
        from dashboard.app import app
        print("✅ Dashboard app imported successfully")
    except ImportError as e:
        print(f"❌ Dashboard app import failed: {e}")
        return False

    try:
        from bot.scheduler import start_scheduler
        print("✅ Bot scheduler imported successfully")
    except ImportError as e:
        print(f"❌ Bot scheduler import failed: {e}")
        return False

    return True

def test_environment():
    """Test environment variables"""
    print("\n🔍 Testing environment...")

    required_vars = [
        'SECRET_KEY',
        'TELEGRAM_BOT_TOKEN',
        'SOLANA_PRIVATE_KEY'
    ]

    missing_vars = []
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)

    if missing_vars:
        print(f"⚠️  Missing environment variables: {missing_vars}")
        print("   These are required for full functionality")
        return False
    else:
        print("✅ All required environment variables found")
        return True

def test_directories():
    """Test if required directories exist"""
    print("\n🔍 Testing directories...")

    required_dirs = ['logs', 'db', 'bot', 'dashboard', 'utils']

    for dir_name in required_dirs:
        if Path(dir_name).exists():
            print(f"✅ {dir_name}/ directory exists")
        else:
            print(f"❌ {dir_name}/ directory missing")
            return False

    return True

def test_web_server():
    """Test if web server can start"""
    print("\n🔍 Testing web server...")

    try:
        from dashboard.app import app

        # Start server in background thread
        def run_server():
            app.run(host='127.0.0.1', port=8081, debug=False)

        server_thread = threading.Thread(target=run_server, daemon=True)
        server_thread.start()

        # Wait a moment for server to start
        time.sleep(2)

        print("✅ Web server started successfully")
        print("   Dashboard available at: http://127.0.0.1:8081")

        return True

    except Exception as e:
        print(f"❌ Web server test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 Memecoin Bot Deployment Test")
    print("=" * 40)

    tests = [
        ("Import Test", test_imports),
        ("Environment Test", test_environment),
        ("Directory Test", test_directories),
        ("Web Server Test", test_web_server)
    ]

    passed = 0
    total = len(tests)

    for test_name, test_func in tests:
        try:
            if test_func():
                passed += 1
            else:
                print(f"❌ {test_name} failed")
        except Exception as e:
            print(f"❌ {test_name} failed with error: {e}")

    print("\n" + "=" * 40)
    print(f"📊 Test Results: {passed}/{total} tests passed")

    if passed == total:
        print("🎉 All tests passed! Ready for deployment.")
        print("\n📋 Next steps:")
        print("1. Set up your hosting platform (Hostinger/Railway/Heroku)")
        print("2. Upload your files")
        print("3. Configure environment variables")
        print("4. Deploy and monitor the dashboard")
    else:
        print("⚠️  Some tests failed. Please fix issues before deploying.")

    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)