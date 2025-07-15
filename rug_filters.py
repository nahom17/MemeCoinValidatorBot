import requests

def is_token_safe(token_data: dict) -> bool:
    try:
        liquidity = float(token_data.get("liquidity", 0))
        mint_authority = token_data.get("mint_authority", "unknown")
        is_locked = token_data.get("lp_locked", False)
        creator = token_data.get("creator", "")

        if liquidity < 1.0:
            print("❌ Low liquidity (<1 SOL) — Skipping token.")
            return False

        if mint_authority != "renounced":
            print("❌ Mint authority not renounced — Risky.")
            return False

        if not is_locked:
            print("❌ LP not locked — Rug risk.")
            return False

        if creator in get_blacklisted_creators():
            print(f"❌ Creator {creator} is blacklisted.")
            return False

        print("✅ Token passed safety checks.")
        return True
    except Exception as e:
        print(f"⚠️ Error in rug filter: {e}")
        return False

def get_blacklisted_creators():
    return ["7NAoHkjxScamCreator1", "5DqFskWLrugpuller2"]