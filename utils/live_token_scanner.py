
import asyncio
import websockets
import json
from utils.telegram_alerts import send_alert
from utils.log_print import log_print

# Pump.fun WebSocket for real-time new token events
# The new feed streams `new_token` events on the `/api/ws` endpoint.
PUMPFUN_WS = "wss://pumpportal.fun/api/ws"

async def handle_new_token(data):
    symbol = data.get("symbol", "Unknown")
    mint = data.get("mint")
    sol_raised = data.get("sol_raised", 0)
    msg = f"🆕 New Token Detected: {symbol}\nMint: {mint}\nRaised: {sol_raised} SOL"
    log_print(msg)
    send_alert(msg)

async def scanner():
    async with websockets.connect(PUMPFUN_WS) as ws:
        # The feed pushes events without any subscription message.
        # Sending a subscribe request results in an error response, so we just
        # listen immediately after connecting.
        while True:
            try:
                msg = await ws.recv()
                parsed = json.loads(msg)
                if parsed.get("type") == "new_token":
                    await handle_new_token(parsed.get("data", {}))
            except Exception as e:
                log_print(f"[Scanner Error] {e}")
                await asyncio.sleep(3)

def start_scanner():
    asyncio.run(scanner())

if __name__ == "__main__":
    start_scanner()
