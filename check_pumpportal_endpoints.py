#!/usr/bin/env python3
"""
Check for correct PumpPortal API endpoints
"""

import requests

def check_pumpportal_endpoints():
    """Check various PumpPortal API endpoints to find the correct ones"""
    print("🔍 Checking PumpPortal API endpoints...")
    print("=" * 50)

    # Test various possible endpoints
    endpoints_to_test = [
        # Recent tokens endpoints
        "https://pumpportal.fun/api/recent",
        "https://pumpportal.fun/api/recent-tokens",
        "https://pumpportal.fun/api/tokens",
        "https://pumpportal.fun/api/coins",
        "https://pumpportal.fun/api/new-tokens",
        "https://pumpportal.fun/api/latest",

        # General API endpoints
        "https://pumpportal.fun/api/",
        "https://pumpportal.fun/api/status",
        "https://pumpportal.fun/api/health",

        # Trading endpoints
        "https://pumpportal.fun/api/trade",
        "https://pumpportal.fun/api/trade-local",
        "https://pumpportal.fun/api/buy",
        "https://pumpportal.fun/api/sell",

        # Pool endpoints
        "https://pumpportal.fun/api/pools",
        "https://pumpportal.fun/api/pool",
        "https://pumpportal.fun/api/liquidity",

        # Token info endpoints
        "https://pumpportal.fun/api/token",
        "https://pumpportal.fun/api/token-info",
        "https://pumpportal.fun/api/price",

        # Alternative domains
        "https://pumpportal.com/api/recent",
        "https://pumpportal.com/api/tokens",
        "https://pumpportal.com/api/",
    ]

    working_endpoints = []

    for endpoint in endpoints_to_test:
        try:
            response = requests.get(endpoint, timeout=5)
            status = response.status_code
            if status == 200:
                print(f"✅ {endpoint}: {status} (WORKING)")
                working_endpoints.append(endpoint)
            elif status == 404:
                print(f"❌ {endpoint}: {status} (NOT FOUND)")
            else:
                print(f"⚠️  {endpoint}: {status} (OTHER)")
        except Exception as e:
            print(f"❌ {endpoint}: Error - {e}")

    print("\n" + "=" * 50)
    print("📊 Results:")

    if working_endpoints:
        print("✅ Working endpoints found:")
        for endpoint in working_endpoints:
            print(f"   - {endpoint}")
    else:
        print("❌ No working endpoints found")
        print("This suggests that:")
        print("1. The PumpPortal API endpoints we're using don't exist")
        print("2. The API might be private or require authentication")
        print("3. The endpoints might have changed")
        print("4. The API might be deprecated")

    print("\n💡 Recommendation:")
    print("Since the PumpPortal API endpoints are not working,")
    print("we should rely on website scraping for token detection.")
    print("The trading API (trade-local) is working correctly.")

if __name__ == "__main__":
    check_pumpportal_endpoints()