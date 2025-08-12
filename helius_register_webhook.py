import os, requests, json
from dotenv import load_dotenv

load_dotenv()

HELIUS_API_KEY = os.getenv("HELIUS_API_KEY")
NGROK_URL = os.getenv("NGROK_URL")  # e.g., https://abc123.ngrok-free.app

webhook_url = f"{NGROK_URL}/webhook/helius"

payload = {
    "webhookURL": webhook_url,
    "transactionTypes": ["ALL"],
    "accountAddresses": [],
    "webhookType": "enhanced"
}

headers = {
    "Content-Type": "application/json"
}

url = f"https://api.helius.xyz/v0/webhooks?api-key={HELIUS_API_KEY}"
res = requests.post(url, headers=headers, data=json.dumps(payload))

print("✅ Webhook registration response:")
print(res.status_code, res.text)
if res.status_code == 200:
    print("Webhook registered successfully!")
else:
    print("Failed to register webhook. Check your API key and URL.")
    print("Response:", res.text)