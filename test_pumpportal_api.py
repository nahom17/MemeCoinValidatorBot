#!/usr/bin/env python3
"""
Test PumpPortal API with the user's specific token
"""

import requests
import json
import os
from dotenv import load_dotenv

def test_pumpportal_api():
    """Test PumpPortal API with the specific token"""
    print("🔍 Testing PumpPortal API...")

    # Load environment variables
    load_dotenv()
    private_key = os.getenv("PRIVATE_KEY")

    if not private_key:
        print("❌ PRIVATE_KEY not found in environment")
        return

    # Your token address
    token_address = "AXExPZNRHt54vhTPt6VvpcSoGNKMoMD4qGuMYEEzpump"

    print(f"🎯 Testing with token: {token_address}")

    # Test 1: Check if we can get recent tokens
    print("\n📡 Test 1: Getting recent tokens...")
    try:
        response = requests.get("https://pumpportal.fun/api/recent-tokens", timeout=10)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            tokens = response.json()
            print(f"✅ Found {len(tokens)} recent tokens")

            # Look for your specific token
            found = False
            for token in tokens:
                if token.get('mint') == token_address or token.get('address') == token_address:
                    print(f"🎯 Found your token in recent tokens!")
                    print(f"Token data: {json.dumps(token, indent=2)}")
                    found = True
                    break

            if not found:
                print("❌ Your token not found in recent tokens")
        else:
            print(f"❌ API returned status {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {e}")

    # Test 2: Try to get a transaction (without actually sending)
    print("\n📡 Test 2: Getting transaction data...")
    try:
        from solders.keypair import Keypair
        keypair = Keypair.from_base58_string(private_key)
        public_key = str(keypair.pubkey())

        print(f"👤 Public Key: {public_key}")

        # Get transaction data (but don't sign/send)
        url = "https://pumpportal.fun/api/trade-local"
        payload = {
            "publicKey": public_key,
            "action": "buy",
            "mint": token_address,
            "amount": "0.01",
            "denominatedInSol": "true",
            "slippage": 1,
            "priorityFee": 0,
            "pool": "pump"
        }

        headers = {
            "Content-Type": "application/json",
            "User-Agent": "PumpFun-Trading-Bot/1.0"
        }

        response = requests.post(url, json=payload, headers=headers, timeout=30)
        print(f"Status: {response.status_code}")

        if response.status_code == 200:
            data = response.json()
            print("✅ Successfully got transaction data from PumpPortal!")
            print(f"Transaction keys: {list(data.keys())}")

            if 'transaction' in data:
                print("✅ Transaction data received")
            else:
                print("❌ No transaction data in response")
        else:
            print(f"❌ API error: {response.text}")

    except Exception as e:
        print(f"❌ Error: {e}")

    # Test 3: Check token info
    print("\n📡 Test 3: Checking token info...")
    try:
        response = requests.get(f"https://pump.fun/coin/{token_address}")
        print(f"Status: {response.status_code}")

        if response.status_code == 200:
            print("✅ Token page accessible")

            # Try to extract some info
            from bs4 import BeautifulSoup
            soup = BeautifulSoup(response.text, 'html.parser')

            title = soup.find('title')
            if title:
                print(f"📄 Page title: {title.get_text()}")

            # Look for price info
            price_elements = soup.find_all(string=lambda text: text and 'SOL' in text)
            if price_elements:
                print(f"💰 Found price info: {price_elements[0]}")
        else:
            print("❌ Token page not accessible")

    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_pumpportal_api()