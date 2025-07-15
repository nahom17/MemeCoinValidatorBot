#!/usr/bin/env python3
"""
Test script to manually check token detection
"""

import requests
from bs4 import BeautifulSoup
import time

def test_token_detection():
    """Test if we can detect the specific token"""
    print("🔍 Testing token detection for your minted token...")

    # Your token address
    token_address = "AXExPZNRHt54vhTPt6VvpcSoGNKMoMD4qGuMYEEzpump"

    print(f"🎯 Looking for token: {token_address}")

    # Try to get token info from PumpFun
    try:
        url = f"https://pump.fun/coin/{token_address}"
        print(f"📡 Checking: {url}")

        response = requests.get(url, timeout=10)
        print(f"Status: {response.status_code}")

        if response.status_code == 200:
            print("✅ Token page found!")

            # Parse the page
            soup = BeautifulSoup(response.text, 'html.parser')

            # Try to extract token info
            title = soup.find('title')
            if title:
                print(f"📄 Page title: {title.get_text()}")

            # Look for token symbol
            symbol_elements = soup.find_all(['h1', 'h2', 'h3'], string=lambda text: text and 'GEN-Z-POWER' in text)
            if symbol_elements:
                print(f"🎯 Found symbol: {symbol_elements[0].get_text()}")

            # Look for price info
            price_elements = soup.find_all(string=lambda text: text and 'SOL' in text)
            if price_elements:
                print(f"💰 Price info found: {price_elements[0]}")

        else:
            print("❌ Token page not found")

    except Exception as e:
        print(f"❌ Error checking token: {e}")

    # Test the scanner's polling approach
    print("\n🔍 Testing scanner polling approach...")

    try:
        response = requests.get("https://pump.fun/coins", timeout=10)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')

            # Look for your specific token
            coin_links = soup.find_all('a', href=True)
            found = False

            for link in coin_links:
                href = link.get('href', '')
                if token_address in href:
                    print(f"🎯 Found your token in coins page!")
                    print(f"Link: {href}")
                    print(f"Text: {link.get_text().strip()}")
                    found = True
                    break

            if not found:
                print("❌ Your token not found in coins page")
                print("This might be because:")
                print("1. The token is too new and not yet indexed")
                print("2. The token needs time to appear in the listing")
                print("3. The bot needs to wait for the next polling cycle")

    except Exception as e:
        print(f"❌ Error in polling test: {e}")

if __name__ == "__main__":
    test_token_detection()