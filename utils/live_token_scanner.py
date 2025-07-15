
import asyncio
import websockets
import json
from utils.telegram_alerts import send_alert

# Pump.fun WebSocket for real-time new token events
PUMPFUN_WS = "wss://pumpportal.io/api/ws"

async def handle_new_token(data):
    symbol = data.get("symbol", "Unknown")
    mint = data.get("mint")
    sol_raised = data.get("sol_raised", 0)
    msg = f"🆕 New Token Detected: {symbol}\nMint: {mint}\nRaised: {sol_raised} SOL"
    print(msg)
    send_alert(msg)

async def scanner():
    async with websockets.connect(PUMPFUN_WS) as ws:
        while True:
            try:
                msg = await ws.recv()
                parsed = json.loads(msg)
                if parsed.get("type") == "new_token":
                    await handle_new_token(parsed.get("data", {}))
            except Exception as e:
                print(f"[Scanner Error] {e}")
                await asyncio.sleep(3)

def start_scanner():
    asyncio.run(scanner())

if __name__ == "__main__":
    start_scanner()
