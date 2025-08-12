#!/usr/bin/env python3
"""Simple subscription test for the Pump.fun WebSocket feed."""

import json
import threading
import time

import websocket


WEBSOCKET_URL = "wss://pumpportal.fun/api/ws"
SUBSCRIBE_MSG = {"type": "subscribe", "channel": "new_token"}


def on_message(ws, message):
    try:
        data = json.loads(message)
        if data.get("type") == "new_token":
            token = data.get("data", {})
            symbol = token.get("symbol", "UNKNOWN")
            sol_raised = float(token.get("sol_raised", 0))
            print(f"🪙 Token: {symbol} | 💰 SOL Raised: {sol_raised}")
        else:
            print("📥 Unhandled message type.")
    except Exception as e:
        print(f"❌ Error parsing message: {e}")


def on_error(ws, error):
    print(f"❌ WebSocket error: {error}")


def on_close(ws, code, msg):
    print(f"🔌 WebSocket closed: {code} - {msg}")


def on_open(ws):
    print("📡 Connected to PumpPortal WebSocket")
    ws.send(json.dumps(SUBSCRIBE_MSG))
    print("✅ Subscription message sent")


def test_websocket_subscription():
    print("🔍 Testing PumpPortal WebSocket subscription...")
    ws = websocket.WebSocketApp(
        WEBSOCKET_URL,
        on_open=on_open,
        on_message=on_message,
        on_error=on_error,
        on_close=on_close,
    )

    thread = threading.Thread(target=ws.run_forever)
    thread.daemon = True
    thread.start()

    # Allow some time to receive messages
    time.sleep(5)
    ws.close()
    thread.join()
    print("📊 Test completed")


if __name__ == "__main__":
    test_websocket_subscription()

