import json
import re

CALL_KEYWORDS = [
    "buy now", "$", "🔥", "raid", "pump", "moon", "trending", "WLFI", "launch", "to the moon"
]

def is_token_called_or_raided() -> bool:
    try:
        with open("telegram_updates.json", "r") as f:
            data = json.load(f)
        messages = data.get("result", [])
        for entry in messages:
            msg = entry.get("message", {}).get("text", "").lower()
            if any(re.search(keyword, msg) for keyword in CALL_KEYWORDS):
                print(f"📢 Community call detected in message: {msg}")
                return True
        print("🛑 No community call or raiding activity detected.")
        return False
    except Exception as e:
        print(f"⚠️ Error scanning telegram updates: {e}")
        return False