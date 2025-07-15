from telegram import Bot
import os

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def send_alert(message):
    if not BOT_TOKEN or not CHAT_ID:
        print("Telegram bot config missing.")
        return

    try:
        bot = Bot(token=BOT_TOKEN)
        bot.send_message(chat_id=CHAT_ID, text=message)
        print(f"✅ Telegram alert sent: {message}")
    except Exception as e:
        print(f"❌ Failed to send Telegram alert: {e}")
