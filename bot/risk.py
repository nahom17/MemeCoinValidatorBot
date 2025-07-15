

import requests
from utils.log_print import log_print

def is_token_safe(token):
    try:
        address = token.get("address") or token.get("mint")
        if not address:
            log_print("❌ Missing token address")
            return False
        log_print(f"🔎 Checking token address: {address}")

        # Use pre-fetched metadata if available
        meta = token.get("metadata")
        if not meta:
            url = f"https://pump.fun/api/metadata/{address}"
            headers = {"User-Agent": "Mozilla/5.0"}
            res = requests.get(url, headers=headers)
            if res.status_code != 200:
                log_print(f"❌ Failed to fetch metadata for {token.get('symbol', address)}")
                return False
            meta = res.json()

        # ✅ Check liquidity value
        liquidity = meta.get("liquidity", 0)
        if liquidity < 0.1:
            log_print(f"❌ {token.get('symbol', address)} has low liquidity: {liquidity} SOL")
            return False

        # ✅ Check mint renounced
        if meta.get("mintAuthority") is not None:
            log_print(f"❌ {token.get('symbol', address)} mint not renounced.")
            return False

        # ✅ Check freeze authority
        if meta.get("freezeAuthority") is not None:
            log_print(f"❌ {token.get('symbol', address)} freeze authority active.")
            return False

        # ✅ Check burned status
        if not meta.get("burned", False):
            log_print(f"❌ {token.get('symbol', address)} not burned.")
            return False

        # ✅ Optional: Check supply size
        supply = meta.get("supply", 0)
        if supply > 1_000_000_000:
            log_print(f"❌ {token.get('symbol', address)} has very large supply.")
            return False

        log_print(f"✅ {token.get('symbol', address)} passed risk check.")
        return True

    except Exception as e:
        log_print(f"❌ Error in risk check for {token.get('symbol', 'Unknown')}: {e}")
        return False


