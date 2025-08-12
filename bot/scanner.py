import websocket, json, threading, time
from bot.risk import is_token_safe
from bot.buyer import buy_token
from utils.log_print import log_print

# Single WebSocket endpoint for Pump.fun
# The previous `data/v1` endpoint no longer works; use the new `/api/ws` feed
# which emits `new_token` events.
WEBSOCKET_ENDPOINTS = [
    "wss://pumpportal.fun/api/ws",  # Global public endpoint
]

current_ws_index = 0
ws = None

def run_scanner(on_token_callback):
    global current_ws_index, ws

    def connect():
        global ws, current_ws_index
        while current_ws_index < len(WEBSOCKET_ENDPOINTS):
            ws_url = WEBSOCKET_ENDPOINTS[current_ws_index]
            log_print(f"🌐 Trying WebSocket endpoint: {ws_url}")
            try:
                ws = websocket.WebSocketApp(
                    ws_url,
                    on_message=on_message,
                    on_error=on_error,
                    on_open=on_open,
                    on_close=on_close
                )
                ws.run_forever()
            except Exception as e:
                log_print(f"❌ Connection failed for {ws_url}: {e}")
                current_ws_index += 1
                time.sleep(3)
        log_print("⚠️ All endpoints failed. Retrying from the first endpoint in 30 seconds...")
        current_ws_index = 0
        time.sleep(30)
        connect()

    def on_message(ws, message):
        """Handle incoming messages from the Pump.fun feed."""
        try:
            data = json.loads(message)

            # Debug log every message
            log_print(f"📥 Received message: {data}")

            # The new feed sends messages in the form:
            # {"type": "new_token", "data": { ... token fields ... }}
            if data.get("type") == "new_token":
                token_info = data.get("data", {})
                token = {
                    "mint": token_info.get("mint"),
                    "symbol": token_info.get("symbol", token_info.get("mint", "")[:5]),
                    "sol_raised": token_info.get("sol_raised", 0),
                }
                log_print(
                    f"🚀 New token detected: {token['symbol']} ({token['mint']}) — {token['sol_raised']} SOL"
                )
                if is_token_safe(token):
                    buy_token(token)

        except Exception as e:
            log_print(f"⚠️ Error parsing message: {e}")

    def on_open(ws):
        log_print("✅ WebSocket connected and listening for new tokens...")
        # The public feed immediately streams new tokens; no subscription needed.
        # Some endpoints return errors if a subscribe message is sent, so we
        # simply start listening without sending anything.

    def on_error(ws, error):
        log_print(f"❌ WebSocket Error: {error}")
        ws.close()  # Trigger on_close to rotate endpoint

    def on_close(ws, close_status_code, close_msg):
        global current_ws_index
        log_print(f"🔌 WebSocket closed: {close_status_code} {close_msg}")
        current_ws_index += 1
        connect()  # Move to the next endpoint

    # Start connection loop
    threading.Thread(target=connect, daemon=True).start()
