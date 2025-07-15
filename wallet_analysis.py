import json

def is_smart_wallet_involved(buyers: list) -> bool:
    try:
        with open("smart_wallets.json", "r") as f:
            smart_wallets = json.load(f)["wallets"]
        for buyer in buyers:
            if buyer in smart_wallets:
                print(f"✅ Smart wallet found: {buyer}")
                return True
        print("❌ No smart wallets found among buyers.")
        return False
    except Exception as e:
        print(f"⚠️ Error loading smart wallets: {e}")
        return False