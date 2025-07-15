#!/usr/bin/env python3
"""
Test different PumpFun URLs to find the correct endpoints
"""

import requests
from bs4 import BeautifulSoup

def test_pumpfun_urls():
    """Test different PumpFun URLs to find working endpoints"""
    print("🔍 Testing PumpFun URLs...")
    print("=" * 50)

    # Test various possible URLs
    urls_to_test = [
        "https://pump.fun/",
        "https://pump.fun/coins",
        "https://pump.fun/tokens",
        "https://pump.fun/trending",
        "https://pump.fun/latest",
        "https://pump.fun/new",
        "https://pump.fun/explore",
        "https://pump.fun/market",
        "https://pump.fun/discover",
        "https://pump.fun/browse"
    ]

    working_urls = []

    for url in urls_to_test:
        try:
            print(f"🧪 Testing: {url}")
            response = requests.get(url, timeout=10)
            status = response.status_code

            if status == 200:
                print(f"✅ {url}: {status} (WORKING)")
                working_urls.append(url)

                # Check if it contains token links
                soup = BeautifulSoup(response.text, 'html.parser')
                coin_links = soup.find_all('a', href=True)
                token_links = [link for link in coin_links if '/coin/' in link.get('href', '')]

                if token_links:
                    print(f"   📊 Found {len(token_links)} token links")
                    # Show first few token links
                    for i, link in enumerate(token_links[:3]):
                        href = link.get('href', '')
                        text = link.get_text().strip()[:30]
                        print(f"   - {text} -> {href}")
                else:
                    print("   ⚠️  No token links found")

            elif status == 404:
                print(f"❌ {url}: {status} (NOT FOUND)")
            else:
                print(f"⚠️  {url}: {status} (OTHER)")

        except Exception as e:
            print(f"❌ {url}: Error - {e}")

    print("\n" + "=" * 50)
    print("📊 Results:")

    if working_urls:
        print("✅ Working URLs found:")
        for url in working_urls:
            print(f"   - {url}")

        print("\n💡 Recommendation:")
        print("Update the scanner to use these working URLs")
    else:
        print("❌ No working URLs found")
        print("This suggests PumpFun may have changed their structure")
        print("or requires authentication/special headers")

    return working_urls

if __name__ == "__main__":
    test_pumpfun_urls()