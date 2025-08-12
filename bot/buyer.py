# bot/buyer.py

import os
from bot.trader import trade_local


def buy_token(token):
    private_key = os.getenv("PRIVATE_KEY")
    if not private_key:
        print("❌ PRIVATE_KEY is missing in .env")
        return False

    token_mint = token.get("address") or token.get("mint")
    if not token_mint:
        print("❌ No token mint address provided")
        return False

    try:
        response = trade_local(
            private_key=private_key,
            token_mint=token_mint,
            amount_sol=0.01,  # Reduced to 0.00001 SOL for extremely low liquidity tokens
            side="buy",
        )
        print(f"✅ Buy executed: {response}")
        return True
    except Exception as e:
        print(f"❌ Failed to buy {token.get('symbol', token_mint)}: {e}")
        return False

