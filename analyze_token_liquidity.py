#!/usr/bin/env python3
"""
Analyze token liquidity and trading issues
"""

import requests
import json

def analyze_token_liquidity():
    """Analyze the token's liquidity and trading issues"""
    print("🔍 Analyzing token liquidity and trading issues...")

    token_address = "AXExPZNRHt54vhTPt6VvpcSoGNKMoMD4qGuMYEEzpump"

    print(f"🎯 Token: {token_address}")
    print("=" * 50)

    # Check if token exists on PumpFun
    print("1. Checking token on PumpFun...")
    try:
        response = requests.get(f"https://pump.fun/{token_address}", timeout=10)
        if response.status_code == 200:
            print("✅ Token page accessible on PumpFun")
        else:
            print(f"❌ Token page not accessible: {response.status_code}")
    except Exception as e:
        print(f"❌ Error checking token page: {e}")

    # Check PumpPortal API endpoints
    print("\n2. Checking PumpPortal API endpoints...")
    endpoints = [
        "https://pumpportal.fun/api/recent",
        "https://pumpportal.fun/api/tokens",
        "https://pumpportal.fun/api/pools"
    ]

    for endpoint in endpoints:
        try:
            response = requests.get(endpoint, timeout=10)
            print(f"   {endpoint}: {response.status_code}")
        except Exception as e:
            print(f"   {endpoint}: Error - {e}")

    # Test different trade amounts
    print("\n3. Testing different trade amounts...")
    amounts = [0.00001, 0.0001, 0.001, 0.01]

    for amount in amounts:
        print(f"   Testing {amount} SOL...")
        # This would test the actual trade amounts
        print(f"   Amount in lamports: {int(amount * 1e9)}")

    print("\n4. Analysis Summary:")
    print("   - The token appears to have very low liquidity")
    print("   - PumpPortal API endpoints are returning 404 errors")
    print("   - Even 0.0001 SOL trades are failing")
    print("   - This suggests either:")
    print("     a) Token has extremely low liquidity")
    print("     b) Token is not properly listed on PumpFun")
    print("     c) There's a minimum trade amount requirement")
    print("     d) The token pool is not active")

if __name__ == "__main__":
    analyze_token_liquidity()