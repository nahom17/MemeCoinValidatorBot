
import json
from pathlib import Path

wallet_file = Path("wallets.json")

def load_wallets():
    if not wallet_file.exists():
        return []
    return json.loads(wallet_file.read_text())

from utils.telegram_alerts import send_alert

def get_next_wallet():
    wallets = load_wallets()
    if not wallets:
        raise Exception("No wallets available")
    # Rotate to next wallet
    next_wallet = wallets.pop(0)
    wallets.append(next_wallet)
    wallet_file.write_text(json.dumps(wallets, indent=2))
    send_alert(f"🔄 Switched to new wallet: {next_wallet['wallet']}")
    return next_wallet
