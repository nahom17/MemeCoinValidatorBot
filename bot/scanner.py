import json, websocket, threading, time, os, requests, random
from utils.log_print import log_print
from bot.risk import is_token_safe
from bot.buyer import buy_token

def fetch_from_ipfs(cid, retries=2):
    gateways = [
        "https://ipfs.io/ipfs/",
        "https://cloudflare-ipfs.com/ipfs/",
        "https://gateway.pinata.cloud/ipfs/",
        "https://dweb.link/ipfs/"
    ]
    for attempt in range(retries):
        random.shuffle(gateways)
        for gw in gateways:
            try:
                resp = requests.get(gw + cid, timeout=10)
                if resp.status_code == 200:
                    return resp.json()
            except requests.RequestException:
                continue
        time.sleep((2 ** attempt) + random.random())
    return None

def fetch_token_metadata(mint, uri):
    try:
        r = requests.get(
            f"https://solana-gateway.moralis.io/token/mainnet/metadata/{mint}",
            headers={"X-API-Key": os.getenv("MORALIS_KEY")},
            timeout=10
        )
        if r.ok:
            d = r.json()
            return {
                "name": d.get("name"),
                "symbol": d.get("symbol"),
                "image": d.get("logo") or d.get("metaplex", {}).get("image"),
                "decimals": d.get("decimals"),
                "metaplex": d.get("metaplex")
            }
    except requests.RequestException:
        pass
    if uri:
        cid = uri.rstrip("/").split("/")[-1]
        return fetch_from_ipfs(cid)
    return None

def fetch_liquidity(mint, retries=10, interval=2):
    url = f"https://solana-gateway.moralis.io/token/mainnet/{mint}/pairs"
    headers = {"X-API-Key": os.getenv("MORALIS_KEY")}
    for attempt in range(retries):
        try:
            resp = requests.get(url, headers=headers, timeout=10)
            if resp.ok:
                pairs = resp.json()
                if pairs and isinstance(pairs, list) and len(pairs) > 0:
                    quote_reserve = pairs[0].get("liquidity", {}).get("quoteReserve")
                    if quote_reserve:
                        try:
                            liquidity_sol = int(quote_reserve) / 1_000_000_000
                            return liquidity_sol
                        except Exception:
                            return None
            log_print(f"🔄 No liquidity yet for {mint}. Retrying {attempt+1}/{retries}")
        except requests.RequestException as e:
            log_print(f"⚠️ Liquidity fetch error: {e}")
        time.sleep(interval)
    log_print(f"❌ No liquidity found after retries for {mint}")
    return None

def on_token_callback(token):
    if token.get("type") != "create":
        return
    if is_token_safe(token):
        buy_token(token)

def run_scanner(on_token_callback):
    def on_message(ws, message):
        try:
            data = json.loads(message)
            tx = data.get("txType", data.get("type"))
            mint = data.get("mint")
            symbol = data.get("symbol", "UNKNOWN")
            uri = data.get("uri")

            print("📩 Raw WS message:", message)

            if not mint or not symbol or not uri:
                log_print("⚠️ Ignored: missing mint/symbol/uri")
                return

            if tx == "create":
                log_print(f"🚀 New token detected: {symbol} ({mint})")

                meta = fetch_token_metadata(mint, uri)
                if not meta:
                    log_print(f"⛔ Metadata unavailable for {symbol} ({mint})")
                    return

                log_print(f"✅ Metadata: {meta.get('name')} | Image: {meta.get('image')}")

                liquidity = fetch_liquidity(mint)
                if liquidity is None:
                    log_print(f"❌ Liquidity info unavailable for {symbol} ({mint})")
                    return

                log_print(f"💧 Liquidity: {liquidity:.4f} SOL")

                LIQUIDITY_THRESHOLD = 0.1
                if liquidity >= LIQUIDITY_THRESHOLD:
                    data["metadata"] = meta
                    data["liquidity"] = liquidity
                    on_token_callback(data)
                else:
                    log_print(f"⚠️ Skipping {symbol} — liquidity too low: {liquidity:.4f} < {LIQUIDITY_THRESHOLD}")
        except Exception as e:
            log_print(f"❌ Error parsing token data: {e}")

    def on_open(ws):
        log_print("✅ WebSocket opened. Subscribing...")
        ws.send(json.dumps({
        "type": "subscribe",  # correct message format
        "channel": "new_tokens"  # or check if "new_tokens" or "token_stream" is correct
    }))

    def on_error(ws, error):
        log_print(f"❌ WebSocket error: {error}")

    def on_close(ws, *args):
        log_print("🔌 WebSocket closed")

    def keepalive():
        while True:
            log_print("🟢 Scanner running...")
            time.sleep(30)

    ws = websocket.WebSocketApp(
        "wss://frontend-api.pump-mirror.fun",
        on_message=on_message,
        on_open=on_open,
        on_error=on_error,
        on_close=on_close
    )

    threading.Thread(target=keepalive, daemon=True).start()
    threading.Thread(target=ws.run_forever, daemon=True).start()
