#!/usr/bin/env python3
"""
Analyze PumpFun website structure to understand how tokens are loaded
"""

import requests
from bs4 import BeautifulSoup
import json
import re

def analyze_pumpfun_structure():
    """Analyze PumpFun website structure"""
    print("🔍 Analyzing PumpFun website structure...")
    print("=" * 50)

    # Test the working URLs
    urls_to_analyze = [
        "https://pump.fun/",
        "https://pump.fun/explore"
    ]

    for url in urls_to_analyze:
        print(f"\n📄 Analyzing: {url}")
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')

                # Look for different patterns
                print("🔍 Searching for token patterns...")

                # 1. Look for script tags with token data
                scripts = soup.find_all('script')
                token_scripts = []
                for script in scripts:
                    if script.string and ('token' in script.string.lower() or 'coin' in script.string.lower()):
                        token_scripts.append(script)

                if token_scripts:
                    print(f"✅ Found {len(token_scripts)} scripts with token data")
                else:
                    print("❌ No scripts with token data found")

                # 2. Look for data attributes
                elements_with_data = soup.find_all(attrs={"data-token": True})
                if elements_with_data:
                    print(f"✅ Found {len(elements_with_data)} elements with data-token")
                else:
                    print("❌ No elements with data-token found")

                # 3. Look for any links that might be tokens
                all_links = soup.find_all('a', href=True)
                print(f"📊 Total links found: {len(all_links)}")

                # 4. Look for specific patterns
                patterns_to_check = [
                    r'/coin/[a-zA-Z0-9]+',
                    r'/token/[a-zA-Z0-9]+',
                    r'[a-zA-Z0-9]{32,}',  # Long alphanumeric strings (token addresses)
                ]

                for pattern in patterns_to_check:
                    matches = re.findall(pattern, response.text)
                    if matches:
                        print(f"✅ Found {len(matches)} matches for pattern: {pattern}")
                        print(f"   First few: {matches[:3]}")
                    else:
                        print(f"❌ No matches for pattern: {pattern}")

                # 5. Look for JSON data in script tags
                json_data = []
                for script in scripts:
                    if script.string:
                        # Try to find JSON objects
                        json_matches = re.findall(r'\{[^{}]*"[^"]*"[^{}]*\}', script.string)
                        if json_matches:
                            json_data.extend(json_matches)

                if json_data:
                    print(f"✅ Found {len(json_data)} potential JSON objects")
                    print(f"   First JSON: {json_data[0][:100]}...")
                else:
                    print("❌ No JSON data found")

                # 6. Check for API endpoints in the HTML
                api_patterns = [
                    r'/api/[a-zA-Z0-9/]+',
                    r'https?://[^"]*api[^"]*',
                ]

                for pattern in api_patterns:
                    api_matches = re.findall(pattern, response.text)
                    if api_matches:
                        print(f"✅ Found {len(api_matches)} API endpoints: {pattern}")
                        print(f"   First few: {api_matches[:3]}")
                    else:
                        print(f"❌ No API endpoints found: {pattern}")

            else:
                print(f"❌ URL returned {response.status_code}")

        except Exception as e:
            print(f"❌ Error analyzing {url}: {e}")

    print("\n" + "=" * 50)
    print("📊 Analysis Summary:")
    print("If no token patterns were found, PumpFun likely:")
    print("1. Loads tokens dynamically via JavaScript")
    print("2. Uses a different URL structure")
    print("3. Requires authentication or special headers")
    print("4. Has changed their frontend architecture")

if __name__ == "__main__":
    analyze_pumpfun_structure()