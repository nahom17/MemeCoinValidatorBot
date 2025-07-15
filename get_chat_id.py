import requests

TOKEN = "7853717134:AAG5E99SCeD2K6lcyUnc5aPJvJdi3yGXW5c"
url = f"https://api.telegram.org/bot{TOKEN}/getUpdates"
response = requests.get(url)
with open("telegram_updates.json", "w", encoding="utf-8") as f:
    f.write(response.text)
print("Output written to telegram_updates.json")