# bot/scanner.py
import json, websocket, threading, time, os, requests, random
from utils.log_print import log_print

# Moralis API setup
MORALIS_KEY = os.getenv("MORALIS_KEY")
HEADERS = {"X-API-Key": MORALIS_KEY}

# IPFS gateways for fallback
GATEWAYS = [
    "https://ipfs.io/ipfs/",
    "https://cloudflare-ipfs.com/ipfs/",
    "https://gateway.pinata.cloud/ipfs/",
    "https://dweb.link/ipfs/"
]

def fetch_from_ipfs(cid, retries=2):
    for attempt in range(retries):
        random.shuffle(GATEWAYS)
        for gw in GATEWAYS:
            try:
                resp = requests.get(gw + cid, timeout=10)
                if resp.status_code == 200:
                    return resp.json()
            except requests.RequestException:
                continue
        time.sleep((2 ** attempt) + random.random())
    return None

def fetch_from_moralis(mint):
    try:
        resp = requests.get(
            f"https://solana-gateway.moralis.io/token/mainnet/metadata/{mint}",
            headers=HEADERS, timeout=10
        )
        if resp.ok:
            d = resp.json()
            return {
                "name": d.get("name"),
                "symbol": d.get("symbol"),
                "image": d.get("logo") or d.get("metaplex", {}).get("image"),
                "decimals": d.get("decimals"),
                "metaplex": d.get("metaplex")
            }
    except Exception:
        pass
    return None

def fetch_token_metadata(mint, uri):
    # First try Moralis
    meta = fetch_from_moralis(mint)
    if meta:
        return meta
    # Then IPFS fallback
    if uri:
        cid = uri.rstrip("/").split("/")[-1]
        return fetch_from_ipfs(cid)
    return None

def run_scanner(on_token_callback):
    def on_message(ws, message):
        data = json.loads(message)
        if "message" in data and not data.get("txType") and not data.get("type"):
            return

        tx = data.get("txType", data.get("type"))
        if tx == "create":
            mint = data["mint"]
            sym = data.get("symbol", mint[:6])
            uri = data.get("uri")
            log_print(f"🚀 New token: {sym} ({mint})")

            meta = fetch_token_metadata(mint, uri)
            if not meta:
                log_print(f"⛔ Metadata unavailable for {sym} ({mint})")
                return

            log_print(f"✅ Metadata fetched: {meta.get('name')}, Image: {meta.get('image')}")
            data["metadata"] = meta
            on_token_callback(data)

        elif tx == "buy":
            on_token_callback(data)

    def on_open(ws):
        ws.send(json.dumps({"method": "subscribeNewToken"}))
        if os.path.exists("manual_tokens.json"):
            try:
                ks = [t['mint'] for t in json.load(open("manual_tokens.json"))]
                if ks:
                    ws.send(json.dumps({"method": "subscribeTokenTrade", "keys": ks}))
            except Exception as e:
                log_print("❌ Error loading manual tokens:", e)

    ws = websocket.WebSocketApp(
        "wss://pumpportal.fun/api/data",
        on_open=on_open, on_message=on_message,
        on_error=lambda ws,e: ws.close(),
        on_close=lambda ws,c,m: None
    )
    threading.Thread(target=ws.run_forever, daemon=True).start()
    log_print("🔗 Scanner connected to WebSocket")
