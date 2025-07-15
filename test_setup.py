#!/usr/bin/env python3
"""
Test script to verify the PumpFun trading bot setup
"""

import os
import requests
from dotenv import load_dotenv

def test_environment():
    """Test environment variables"""
    print("🔍 Testing environment setup...")

    load_dotenv()

    required_vars = [
        "PRIVATE_KEY",
        "RPC_URL",
        "TELEGRAM_BOT_TOKEN",
        "TELEGRAM_CHAT_ID"
    ]

    missing = []
    for var in required_vars:
        value = os.getenv(var)
        if not value or "your_" in value:
            missing.append(var)
        else:
            print(f"✅ {var}: {'*' * len(value)}")

    if missing:
        print(f"❌ Missing environment variables: {missing}")
        return False
    else:
        print("✅ All environment variables are set")
        return True

def test_pumpfun_api():
    """Test PumpFun API connectivity"""
    print("\n🔍 Testing PumpFun API...")

    try:
        # Test basic API connectivity
        response = requests.get("https://pump.fun/api/health", timeout=10)
        if response.status_code == 200:
            print("✅ PumpFun API is accessible")
            return True
        else:
            print(f"⚠️ PumpFun API returned status {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ PumpFun API error: {e}")
        return False

def test_risk_module():
    """Test risk checking module"""
    print("\n🔍 Testing risk module...")

    try:
        from bot.risk import is_token_safe

        # Test with a sample token
        test_token = {
            "symbol": "TEST",
            "address": "test123"
        }

        result = is_token_safe(test_token)
        print(f"✅ Risk module test completed (result: {result})")
        return True
    except Exception as e:
        print(f"❌ Risk module error: {e}")
        return False

def test_price_tracker():
    """Test price tracking module"""
    print("\n🔍 Testing price tracker...")

    try:
        from bot.price_tracker import fetch_token_price

        # Test with a sample token
        test_token = {
            "symbol": "TEST",
            "address": "test123"
        }

        price = fetch_token_price(test_token)
        print(f"✅ Price tracker test completed (price: {price})")
        return True
    except Exception as e:
        print(f"❌ Price tracker error: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 PumpFun Trading Bot Setup Test")
    print("=" * 40)

    tests = [
        test_environment,
        test_pumpfun_api,
        test_risk_module,
        test_price_tracker
    ]

    passed = 0
    total = len(tests)

    for test in tests:
        if test():
            passed += 1

    print("\n" + "=" * 40)
    print(f"📊 Test Results: {passed}/{total} passed")

    if passed == total:
        print("✅ All tests passed! Bot is ready to run.")
        print("\nTo start the bot, run:")
        print("python run.py")
    else:
        print("❌ Some tests failed. Please fix the issues above.")
        print("\nCommon fixes:")
        print("1. Create a .env file with your configuration")
        print("2. Install dependencies: pip install -r requirements.txt")
        print("3. Check your internet connection")

if __name__ == "__main__":
    main()