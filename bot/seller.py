import os
import base58
from solders.keypair import Keypair
from solders.pubkey import Pubkey
from bot.trader import trade_local  # ✅ make sure this path is correct
from bot.price_tracker import fetch_token_price, calculate_profit  # optional, if you check price again

def should_sell(token, buy_price, current_price):
    profit = (current_price - buy_price) / buy_price

    if profit >= 1.0:
        return f"💰 {round(profit * 100)}% profit"
    elif profit <= -0.3:
        return f"🔻 {round(profit * 100)}% loss (stop-loss)"
    else:
        return None

def sell_token(token):
    try:
        private_key = os.getenv("PRIVATE_KEY")
        if not private_key:
            print("❌ No private key found.")
            return False

        keypair = Keypair.from_bytes(base58.b58decode(private_key))
        wallet = keypair.pubkey()
        token_address = token.get("address") or token.get("mint")
        if not token_address:
            print("❌ No token address provided.")
            return False
        token_address = Pubkey.from_string(token_address)

        txid = trade_local(
            buyer=wallet,
            mint=token_address,
            side="sell",
            amount=100  # sell 100% of tokens (adjust if needed)
        )

        print(f"✅ Sold {token['symbol']} | tx: {txid}")
        return True

    except Exception as e:
        print(f"❌ Sell failed for {token['symbol']}: {e}")
        return False
