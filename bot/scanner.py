import websocket, json, threading, time
from bot.risk import is_token_safe
from bot.buyer import buy_token
from utils.log_print import log_print

# Multiple WebSocket endpoints for Pump.fun
WEBSOCKET_ENDPOINTS = [
    "wss://pumpportal.fun/ws",  # Global public endpoint
    "wss://pump-frontend-mainnet.helius-rpc.com/ws",  # Helius fallback
    "wss://frontend-api.pump-mirror.fun/ws"  # Mirror (may need Google DNS or VPN)
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
        try:
            data = json.loads(message)
            tx_type = data.get("txType", data.get("type"))

            # Debug log every message
            log_print(f"📥 Received message: {data}")

            if tx_type == "create":
                token = {
                    "mint": data["mint"],
                    "symbol": data.get("symbol", data["mint"][:5]),
                    "sol_raised": data.get("sol_raised", 0)
                }
                log_print(f"🚀 New token detected: {token['symbol']} ({token['mint']}) — {token['sol_raised']} SOL")
                if is_token_safe(token):
                    buy_token(token)

        except Exception as e:
            log_print(f"⚠️ Error parsing message: {e}")

    def on_open(ws):
        log_print("✅ WebSocket connected and listening for new tokens...")

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
