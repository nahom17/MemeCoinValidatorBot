import os
from dotenv import load_dotenv

load_dotenv()

required_keys = [
    "PRIVATE_KEY",
    "RPC_URL",
    "TELEGRAM_BOT_TOKEN",
    "TELEGRAM_CHAT_ID"
]

missing = []
for key in required_keys:
    value = os.getenv(key)
    if not value or "your_" in value:
        missing.append(key)

if missing:
    print("❌ Missing or invalid .env keys:")
    for key in missing:
        print(f" - {key}")
else:
    print("✅ All required .env keys are present and look valid.")
