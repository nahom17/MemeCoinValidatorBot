
import json
import time
from pathlib import Path
import os
from dotenv import load_dotenv
load_dotenv()

CONFIG = json.load(open('config.json'))

def detect_mev_risk(token_data, recent_trades):
    # Example MEV pattern checks (simplified)
    if token_data.get("liquidity", 0) < CONFIG["min_liquidity"]:
        return "Low liquidity"
    if token_data.get("creator") in get_known_snipers():
        return "Sniper wallet"
    if is_sandwich_pattern(recent_trades):
        return "Sandwich pattern"
    return None

def get_known_snipers():
    try:
        with open("logs/mev_flags.json") as f:
            flagged = json.load(f)
        return set(entry["wallet"] for entry in flagged if "Sniper" in entry["reason"])
    except:
        return set()

def is_sandwich_pattern(trades):
    # Very basic sandwich pattern check
    if len(trades) < 3:
        return False
    first, middle, last = trades[-3:]
    return first["type"] == "buy" and last["type"] == "sell" and middle["type"] == "buy"

from utils.telegram_alerts import send_alert

def log_flagged_trade(token_data, reason):
    log_path = Path("logs/mev_flags.json")
    logs = json.loads(log_path.read_text()) if log_path.exists() else []
    logs.append({
        "timestamp": time.time(),
        "token": token_data.get("symbol"),
        "creator": token_data.get("creator"),
        "reason": reason
    })
    log_path.write_text(json.dumps(logs, indent=2))
    send_alert(f"🚨 MEV Alert: {token_data.get('symbol')} flagged for {reason}")


from bot.scheduler import start_scheduler, handle_token_callback
from bot.scanner import run_scanner
from dashboard.app import app
import threading

if __name__ == "__main__":
    # Start trading logic in background
    threading.Thread(target=start_scheduler, daemon=True).start()
    threading.Thread(target=run_scanner, args=(handle_token_callback,), daemon=True).start()

    # Start Flask in main thread (required for debug=True)
    app.run(debug=True, port=8080)
