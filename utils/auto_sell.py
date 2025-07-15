
import time
import random

def evaluate_sell(token_data, trade_entry):
    # Placeholder logic — adjust for real wallet or API integration
    current_price = get_live_price(token_data['mint'])  # Stub
    entry_price = trade_entry.get('buy_price')
    time_held = time.time() - trade_entry.get('timestamp', time.time())

    profit_percent = ((current_price - entry_price) / entry_price) * 100 if entry_price else 0

    if profit_percent >= 30:
        return "Take profit"
    elif profit_percent <= -20:
        return "Cut loss"
    elif time_held > 1800:  # 30 minutes
        return "Timeout sell"
    else:
        return None

def get_live_price(mint):
    # Stub logic: Replace with actual DEX API call (e.g., Jupiter or Raydium)
    return random.uniform(0.8, 1.5)  # Simulate price fluctuation

def execute_sell(mint, amount):
    print(f"[AUTO-SELL] Selling {amount} of {mint}...")
    # Integrate actual sell function here (Raydium/Jupiter Swap API or SDK)
