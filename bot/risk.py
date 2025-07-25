
import requests, time
from utils.log_print import log_print

def is_token_safe(token):
    try:
        address = token.get("address") or token.get("mint")
        if not address:
            log_print("❌ Missing token address")
            return False
        log_print(f"🔎 Checking token address: {address}")
        meta = token.get("metadata")
        if not meta:
            url = f"https://pump.fun/api/metadata/{address}"
            headers = {"User-Agent": "Mozilla/5.0"}
            for attempt in range(5):
                res = requests.get(url, headers=headers)
                if res.status_code == 200:
                    meta = res.json()
                    break
                log_print(f"⏳ Waiting for metadata... Attempt {attempt+1}")
                time.sleep(1)
            else:
                log_print(f"❌ Failed to fetch metadata after retries for {address}")
                return False
        liquidity = token.get("sol_raised") or meta.get("liquidity", 0)
        if liquidity < 0.1:
            log_print(f"❌ {token.get('symbol', address)} has low liquidity: {liquidity} SOL")
            return False
        if meta.get("mintAuthority") is not None:
            log_print(f"❌ {token.get('symbol', address)} mint not renounced.")
            return False
        if meta.get("freezeAuthority") is not None:
            log_print(f"❌ {token.get('symbol', address)} freeze authority active.")
            return False
        if not meta.get("burned", False):
            log_print(f"❌ {token.get('symbol', address)} not burned.")
            return False
        if meta.get("supply", 0) > 1_000_000_000:
            log_print(f"❌ {token.get('symbol', address)} has very large supply.")
            return False
        log_print(f"✅ {token.get('symbol', address)} passed risk check.")
        return True
    except Exception as e:
        log_print(f"❌ Error in risk check for {token.get('symbol', 'Unknown')}: {e}")
        return False
