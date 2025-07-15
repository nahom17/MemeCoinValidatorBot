import requests
import time

# Cache for token prices to avoid excessive API calls
price_cache = {}
CACHE_DURATION = 30  # seconds

def fetch_token_price(token):
    """Fetch real token price from PumpFun API"""
    address = token.get("address") or token.get("mint")

    if not address:
        print("❌ No token address provided")
        return 0

    # Check cache first
    current_time = time.time()
    if address in price_cache:
        cached_price, cache_time = price_cache[address]
        if current_time - cache_time < CACHE_DURATION:
            return cached_price

    try:
        # Fetch price from PumpFun API
        url = f"https://pump.fun/api/token/{address}"
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers, timeout=10)

        if response.status_code == 200:
            data = response.json()
            price = data.get("price", 0)

            # Cache the price
            price_cache[address] = (price, current_time)

            print(f"💰 {token.get('symbol', 'Unknown')} price: {price} SOL")
            return price
        else:
            print(f"❌ Failed to fetch price for {token.get('symbol', 'Unknown')}: {response.status_code}")
            return 0

    except Exception as e:
        print(f"❌ Error fetching price for {token.get('symbol', 'Unknown')}: {e}")
        return 0

def calculate_profit(buy_price, current_price):
    """Calculate profit percentage"""
    if buy_price <= 0:
        return 0

    profit_percentage = ((current_price - buy_price) / buy_price) * 100
    return round(profit_percentage, 2)

def get_token_metadata(token_address):
    """Get additional token metadata from PumpFun"""
    try:
        url = f"https://pump.fun/api/metadata/{token_address}"
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers, timeout=10)

        if response.status_code == 200:
            return response.json()
        else:
            print(f"❌ Failed to fetch metadata: {response.status_code}")
            return {}

    except Exception as e:
        print(f"❌ Error fetching metadata: {e}")
        return {}
