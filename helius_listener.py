import os
import json
import requests
from flask import Flask, request, jsonify
from dotenv import load_dotenv

from bot.scanner import fetch_token_metadata, fetch_liquidity, on_token_callback
from utils.log_print import log_print

load_dotenv()

app = Flask(__name__)

# Register this URL in your Helius dashboard when deploying
@app.route("/webhook/helius", methods=["POST"])
def helius_webhook():
    data = request.get_json()
    log_print("📩 Webhook received from Helius")

    # Example structure: check and process tokens
    for tx in data.get("transactions", []):
        mint = tx.get("tokenMint") or tx.get("mint")
        if not mint:
            continue

        if not mint.endswith("pump"):
            log_print(f"⚠️ Ignored non-PumpFun token: {mint}")
            continue

        log_print(f"🚀 Helius new token: {mint}")

        uri = tx.get("uri")  # Optional, fallback to metadata
        meta = fetch_token_metadata(mint, uri)
        if not meta:
            log_print(f"⛔ Metadata unavailable for {mint}")
            continue

        log_print(f"✅ Metadata: {meta.get('name')} {meta.get('symbol')} {meta.get('image')}")

        liquidity = fetch_liquidity(mint)
        if liquidity is None:
            log_print(f"❌ Liquidity info unavailable for {mint}")
            continue

        log_print(f"💧 Liquidity: {liquidity} SOL")

        LIQUIDITY_THRESHOLD = float(os.getenv("MIN_LIQ", 0.1))
        if liquidity >= LIQUIDITY_THRESHOLD:
            tx["metadata"] = meta
            tx["liquidity"] = liquidity
            tx["type"] = "create"
            on_token_callback(tx)
        else:
            log_print(f"⚠️ Skipping low-liquidity token: {liquidity} SOL < {LIQUIDITY_THRESHOLD}")

    return jsonify({"status": "ok"})


if __name__ == "__main__":
    port = int(os.getenv("WEBHOOK_PORT", 5678))
    app.run(host="0.0.0.0", port=port, debug=True)
