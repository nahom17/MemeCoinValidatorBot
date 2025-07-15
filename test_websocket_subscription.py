#!/usr/bin/env python3
"""
Test different WebSocket subscription formats for PumpPortal
"""

import json
import websocket
import time
import threading

def test_websocket_subscriptions():
    """Test different subscription formats"""
    print("🔍 Testing WebSocket subscription formats...")
    print("=" * 50)

    # Different subscription formats to test
    subscription_formats = [
        # Format 1: Direct subscription
        {
            "action": "subscribe",
            "channel": "subscribeNewToken"
        },
        # Format 2: With type
        {
            "type": "subscribe",
            "channel": "subscribeNewToken"
        },
        # Format 3: Simple subscription
        {
            "subscribe": "subscribeNewToken"
        },
        # Format 4: Alternative channel name
        {
            "action": "subscribe",
            "channel": "newToken"
        },
        # Format 5: Different action
        {
            "action": "subscribe",
            "channel": "token"
        },
        # Format 6: Minimal format
        {
            "subscribe": "newToken"
        }
    ]

    
def on_message(ws, message):
    try:
        data = json.loads(message)
        if "type" in data and data["type"] == "new_token":
            token = data["data"]
            symbol = token.get("symbol", "UNKNOWN")
            sol_raised = float(token.get("sol_raised", 0))

            print(f"🪙 Token: {symbol} | 💰 SOL Raised: {sol_raised}")

            if 3 <= sol_raised <= 15:
                print(f"✅ Volume Spike Detected for {symbol} — Consider Buying!")
            else:
                print(f"⚠️ Skipping {symbol} — Volume out of range.")
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
        print("Testing subscription formats...")

        for i, format_msg in enumerate(subscription_formats, 1):
            print(f"\n🧪 Testing format {i}: {format_msg}")
            ws.send(json.dumps(format_msg))
            time.sleep(2)  # Wait for response

        # Close after testing
        time.sleep(5)
        ws.close()

    # Connect to WebSocket
    websocket_url = "wss://pumpportal.fun/api/data"
    print(f"🔗 Connecting to: {websocket_url}")

    ws = websocket.WebSocketApp(
        websocket_url,
        on_open=on_open,
        on_message=on_message,
        on_error=on_error,
        on_close=on_close,
    )

    # Run in background thread
    wst = threading.Thread(target=ws.run_forever)
    wst.daemon = True
    wst.start()

    # Wait for completion
    wst.join(timeout=30)

    print("\n📊 Test completed")
    print("Check the responses above to see which format works")

if __name__ == "__main__":
    test_websocket_subscriptions()