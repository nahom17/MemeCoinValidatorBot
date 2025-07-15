import json
from utils.log_print import log_print

def is_smart_wallet_involved(buyers: list) -> bool:
    try:
        with open("smart_wallets.json", "r") as f:
            smart_wallets = json.load(f)["wallets"]
        for buyer in buyers:
            if buyer in smart_wallets:
                log_print(f"✅ Smart wallet found: {buyer}")
                return True
        log_print("❌ No smart wallets found among buyers.")
        return False
    except Exception as e:
        log_print(f"⚠️ Error loading smart wallets: {e}")
        return False